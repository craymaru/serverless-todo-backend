import operator

import pytest
from chalice import NotFoundError

import app

from tests.testdata.ddb_items import TESTDATA_DDB_ITEMS


class TestDB:
    pass


class TestListAllItems(TestDB):
    def test_Return_all_items_list(self, mock):
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        assert app.get_app_db().list_all_items() == TESTDATA_DDB_ITEMS


class TestListItems(TestDB):

    def test_Return_items_list(self, mock):
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        query = ''
        username = 'default'

        actual = app.get_app_db().list_items(query=query, username=username)
        actual = sorted(actual, key=operator.itemgetter('uid'))
        expected = sorted(TESTDATA_DDB_ITEMS,
                          key=operator.itemgetter('uid'))
        assert actual == expected

    @pytest.mark.parametrize('query', ['🐈', '🍆'])
    def test_Return_items_list_With_query(self, query, mock):
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        actual = app.get_app_db().list_items(query=query, username='default')
        actual.sort(key=operator.itemgetter('uid'))
        expected = []
        for d in TESTDATA_DDB_ITEMS:
            if query in d['subject'] or query in d['description']:
                expected.append(d)
        expected = sorted(expected, key=operator.itemgetter('uid'))

        assert actual == expected


class TestAddItem(TestDB):

    @pytest.mark.parametrize('item', [item for item in TESTDATA_DDB_ITEMS])
    def test_Return_uid_str(self, mock, item):
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        actual = app.get_app_db().add_item(
            subject=item['subject'],
            description=item['description'],
            username='default')
        assert type(actual) == str
        assert len(actual) == 36


class TestGetItem(TestDB):

    @pytest.mark.parametrize("item", [
        item for item in TESTDATA_DDB_ITEMS])
    def test_Return_get_item(self, mock, item):
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        uid = item['uid']
        assert app.get_app_db().get_item(uid=uid, username='default') == item

    def test_Raise_NotFoundError_when_without_item(self, mock):
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        uid = TESTDATA_DDB_ITEMS[0]['uid']
        with pytest.raises(NotFoundError):
            app.get_app_db().get_item("_", username='default')


class TestDeleteItem(TestDB):

    @pytest.mark.parametrize("item", [
        item for item in TESTDATA_DDB_ITEMS])
    def test_Return_delete_item(self, mock, item):
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        assert app.get_app_db().delete_item(
            item['uid'], username='default') == item['uid']

    def test_Raise_NotFoundError_when(self, mock):
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        with pytest.raises(NotFoundError):
            app.get_app_db().delete_item("NOT-EXIST-UID", username='default')


class TestUpdateItem(TestDB):

    @pytest.mark.parametrize("item", [
        item for item in TESTDATA_DDB_ITEMS])
    def test_Return_update_item(self, mock, item):
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        actual = app.get_app_db().update_item(
            uid=item['uid'],
            subject=item['subject'],
            description=item['description'],
            state=item['state'],
            username='default')
        assert actual == item['uid']

    def test_Raise_NotFoundError_when(self, mock):
        mock.table.put_items(TESTDATA_DDB_ITEMS)
        with pytest.raises(NotFoundError):
            app.get_app_db().update_item("NOT-EXIST-UID", username='default')
