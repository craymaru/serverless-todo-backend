import operator

import pytest
from chalice import NotFoundError

import app

from tests.testdata.ddb_items import TESTDATA_DDB_ITEMS


DEFAULT_USERNAME = 'default'


class TestDB:
    pass


class TestListAllItems(TestDB):
    def test_Return_all_items(self, mock):
        """list_all_items: すべてのアイテムを取得することができる"""
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        assert app.get_app_db().list_all_items() == TESTDATA_DDB_ITEMS


class TestListItems(TestDB):

    def test_Return_items_by_username(self, mock):
        """list_items: ユーザーdefaultのアイテムをすべて取得することができる"""
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        query = ''
        actual = app.get_app_db().list_items(query=query, username=DEFAULT_USERNAME)
        actual = sorted(actual, key=operator.itemgetter('uid'))
        expected = [item for item in TESTDATA_DDB_ITEMS
                    if item['username'] == DEFAULT_USERNAME]
        expected = sorted(expected, key=operator.itemgetter('uid'))
        assert actual == expected

    @pytest.mark.parametrize('query', ['🐈', '🍆'])
    def test_Return_items_by_query(self, query, mock):
        """list_items: ユーザーdefaultのアイテムからクエリを満たすものをすべて取得することができる"""
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        actual = app.get_app_db().list_items(query=query, username=DEFAULT_USERNAME)
        actual.sort(key=operator.itemgetter('uid'))
        expected = [item for item in TESTDATA_DDB_ITEMS
                    if item['username'] == DEFAULT_USERNAME]
        expected = [item for item in expected
                    if query in item['subject'] or query in item['description']]
        expected = sorted(expected, key=operator.itemgetter('uid'))
        assert actual == expected


class TestAddItem(TestDB):

    @pytest.mark.parametrize('item', TESTDATA_DDB_ITEMS)
    def test_Return_uid_str_cace_subject_description(self, item):
        """add_item: subjectとdescriptionがあるケース、正常にクエリを投げuidを受け取ることができる"""
        actual = app.get_app_db().add_item(
            subject=item['subject'],
            description=item['description'],
            username=DEFAULT_USERNAME)
        assert type(actual) == str
        assert len(actual) == 36

    # 以下の状況によりこのテストケースは現時点において実施しない (2020-11-30)
    #
    # [状況] Amazon DynamoDB 2020-05-18 以降の仕様では、
    # 文字列型/バイナリ型の項目について空の文字列「''」を許すようになっている
    # 本テストに使用している moto による DynamoDB のモックの仕様は現時点においてまだ追従していないため、
    # 空の文字列の登録許さないため、このテストケースを実行するとエラーが発生してしまう
    # この状況があてはまらなくなったら、適宜コメントアウトを外し以下のテストケースを実施する
    #
    # @pytest.mark.parametrize('item', TESTDATA_DDB_ITEMS)
    # def test_Return_uid_str_cace_subject_only(self, item):
    #     """add_item: subjectのみのケース、正常にクエリを投げuidを受け取ることができる"""
    #     actual = app.get_app_db().add_item(
    #         subject=item['subject'],
    #         username=DEFAULT_USERNAME)
    #     assert type(actual) == str
    #     assert len(actual) == 36

    def test_Raise_case_description_only(self):
        """add_item: descriptionのみのケース、例外を発生させることができる"""
        with pytest.raises(TypeError):
            app.get_app_db().add_item(
                description='',
                username=DEFAULT_USERNAME)


class TestGetItem(TestDB):

    @pytest.mark.parametrize("item", TESTDATA_DDB_ITEMS)
    def test_Return_item(self, mock, item):
        """get_item: uidが存在するケース、itemを正常に返すことができる"""
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        assert app.get_app_db().get_item(
            uid=item['uid'], username=item['username']) == item

    def test_Raise_NotFoundError_case_uid_not_exist(self, mock):
        """get_item: uidが存在しないケース、例外を発生させることができる"""
        with pytest.raises(NotFoundError):
            app.get_app_db().get_item("_NOT_EXIST_UID", username=DEFAULT_USERNAME)


class TestDeleteItem(TestDB):

    @pytest.mark.parametrize("item", TESTDATA_DDB_ITEMS)
    def test_Return_uid_str(self, mock, item):
        """delete_item: uidが存在するケース、削除したitemのuidを正常に返すことができる"""
        mock.table.put_items([item])
        assert app.get_app_db().delete_item(
            item['uid'], username=item['username']) == item['uid']

    def test_Raise_NotFoundError_case_uid_not_exist(self, mock):
        """delete_item: uidが存在しないケース、例外を発生させることができる"""
        with pytest.raises(NotFoundError):
            app.get_app_db().delete_item("_NOT_EXIST_UID", username=DEFAULT_USERNAME)


class TestUpdateItem(TestDB):

    @pytest.mark.parametrize("item", TESTDATA_DDB_ITEMS)
    def test_Return_uid_case_all_attributes(self, mock, item):
        """update_item: すべての属性を更新するケース、更新したitemのuidを正常に返すことができる"""
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        actual = app.get_app_db().update_item(
            uid=item['uid'],
            subject=item['subject']+"_updated",
            description=item['description']+"_updated",
            state=item['state'],
            username=item['username'])
        assert actual == item['uid']

    @pytest.mark.parametrize("item", TESTDATA_DDB_ITEMS)
    def test_Return_uid_case_subject_only(self, mock, item):
        """update_item: subjectを更新するケース、更新したitemのuidを正常に返すことができる"""
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        actual = app.get_app_db().update_item(
            uid=item['uid'],
            subject=item['subject']+"_updated",
            username=item['username'])
        assert actual == item['uid']

    @pytest.mark.parametrize("item", TESTDATA_DDB_ITEMS)
    def test_Return_uid_case_description_only(self, mock, item):
        """update_item: descriptionを更新するケース、更新したitemのuidを正常に返すことができる"""
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        actual = app.get_app_db().update_item(
            uid=item['uid'],
            description=item['description']+"_updated",
            username=item['username'])
        assert actual == item['uid']

    @pytest.mark.parametrize("item", TESTDATA_DDB_ITEMS)
    def test_Return_uid_case_state_only(self, mock, item):
        """update_item: stateを更新するケース、更新したitemのuidを正常に返すことができる"""
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        actual = app.get_app_db().update_item(
            uid=item['uid'],
            state=item['state'],
            username=item['username'])
        assert actual == item['uid']

    def test_Raise_NotFoundError_case_uid_not_exist(self, mock):
        """update_item: uidが存在しないケース、例外を発生させることができる"""
        with pytest.raises(NotFoundError):
            app.get_app_db().update_item("_NOT_EXIST_UID", username=DEFAULT_USERNAME)
