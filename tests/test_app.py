import pytest
from http import HTTPStatus

from chalice import BadRequestError
from chalice.app import Request

import app
from chalicelib.db import DynamoDBTodo

from tests.testdata.ddb_items import TESTDATA_DDB_ITEMS


class TestApp:

    @staticmethod
    def set_env(client, monkeypatch):
        client.get('/')


class TestGetIndex(TestApp):
    def test_Return_status_code_200_and_json(self, client):
        """root: ステータスコード200とJSONを返すことができる"""
        response = client.get('/')
        assert response.status_code == HTTPStatus.OK
        assert True if response.json else False == True


class TestGetAppDB(TestApp):

    def test_Return_DynamoDBTodo_class(self):
        """get_app_db: get_app_dbの返り値クラスと、元のクラスが一致する"""
        assert app.get_app_db().__class__ is DynamoDBTodo


class TestGetTodos(TestApp):

    def _monkeys(self, client, monkeypatch):
        super().set_env(client, monkeypatch)
        monkeypatch.setattr(DynamoDBTodo, 'list_items',
                            lambda *_, **__: TESTDATA_DDB_ITEMS)

    def test_Return_todos_list(self, client, monkeypatch):
        """get_todos: すべてのアイテムを取得することができる"""
        self._monkeys(client, monkeypatch)
        assert app.get_todos() == TESTDATA_DDB_ITEMS


class TestAddNewTodo(TestApp):

    def _monkeys(self, client, monkeypatch):
        super().set_env(client, monkeypatch)
        from uuid import uuid4
        monkeypatch.setattr(DynamoDBTodo, 'add_item',
                            lambda *_, **__: str(uuid4()))
        monkeypatch.setattr(app, 'get_authorized_username',
                            lambda *_, **__: 'default')

    @pytest.mark.parametrize('item', TESTDATA_DDB_ITEMS)
    def test_Return_uid_case_subject_and_description(self, client, monkeypatch, item):
        """add_new_todo: subjectとdescriptionがあるケース、uidを受け取ることができる"""
        self._monkeys(client, monkeypatch)
        json_body = {
            'subject': item['subject'],
            'description': item['description']}
        monkeypatch.setattr(Request, 'json_body', json_body)
        actual = app.add_new_todo()
        assert type(actual) == str
        assert len(actual) == 36

    @pytest.mark.parametrize('item', TESTDATA_DDB_ITEMS)
    def test_Return_uid_case_subject_only(self, client, monkeypatch, item):
        """add_new_todo: subjectのみのケース、uidを受け取ることができる"""
        self._monkeys(client, monkeypatch)
        json_body = {'subject': item['subject']}
        monkeypatch.setattr(Request, 'json_body', json_body)
        actual = app.add_new_todo()
        assert type(actual) == str
        assert len(actual) == 36

    def test_Raise_BadRequestError_case_None_subject(self, client, monkeypatch):
        """add_new_todo: subjectが無いケース、例外を発生させることができる"""
        self._monkeys(client, monkeypatch)
        json_body = {}
        monkeypatch.setattr(Request, 'json_body', json_body)
        with pytest.raises(BadRequestError):
            app.add_new_todo()

    @pytest.mark.parametrize('item', TESTDATA_DDB_ITEMS)
    def test_Raise_BadRequestError_case_without_subject(self, client, monkeypatch, item):
        """add_new_todo: descriptionのみのケース、例外を発生させることができる"""
        self._monkeys(client, monkeypatch)
        json_body = {'description': item['description']}
        monkeypatch.setattr(Request, 'json_body', json_body)
        with pytest.raises(BadRequestError):
            app.add_new_todo()

    def test_Raise_BadRequestError_case_None_json_body(self, client, monkeypatch):
        """add_new_todo: json_bodyがNoneのケース、例外を発生させることができる"""
        self._monkeys(client, monkeypatch)
        with pytest.raises(BadRequestError):
            app.add_new_todo()


class TestGetTodo(TestApp):

    def _monkeys(self, monkeypatch):
        def _get_item(self, uid, username):
            for item in TESTDATA_DDB_ITEMS:
                if item['uid'] == uid and item['username'] == username:
                    return item
        monkeypatch.setattr(DynamoDBTodo, 'get_item', _get_item)

    @pytest.mark.parametrize('item', TESTDATA_DDB_ITEMS)
    def test_Return_todo_dict(self, monkeypatch, item):
        """get_todo: 取得に指定したuid、usernameのTodoを受け取ることができる"""
        self._monkeys(monkeypatch)
        monkeypatch.setattr(app, 'get_authorized_username',
                            lambda *_, **__: item['username'])
        assert app.get_todo(uid=item['uid']) == item


class TestDeleteTodo(TestApp):

    def _monkeys(self, monkeypatch):
        def _delete_item(self, uid, username):
            for item in TESTDATA_DDB_ITEMS:
                if item['uid'] == uid and item['username'] == username:
                    return item['uid']
        monkeypatch.setattr(DynamoDBTodo, 'delete_item', _delete_item)

    @pytest.mark.parametrize('item', TESTDATA_DDB_ITEMS)
    def test_Return_uid(self, monkeypatch, item):
        """delete_todo: 削除に指定したuid、usernameのTodoのuidを受け取ることができる"""
        self._monkeys(monkeypatch)
        monkeypatch.setattr(app, 'get_authorized_username',
                            lambda *_, **__: item['username'])
        assert app.delete_todo(uid=item['uid']) == item['uid']


class TestUpdateTodo(TestApp):

    def _monkeys(self, client, monkeypatch, item=None):
        super().set_env(client, monkeypatch)

        def _update_item(self, uid, username, **__):
            for item in TESTDATA_DDB_ITEMS:
                if item['uid'] == uid and item['username'] == username:
                    return item['uid']
        monkeypatch.setattr(DynamoDBTodo, 'update_item', _update_item)
        monkeypatch.setattr(app, 'get_authorized_username',
                            lambda *_, **__: item['username'])

    @pytest.mark.parametrize('item', TESTDATA_DDB_ITEMS)
    def test_Return_uid_case_subject_description_state(self, client, monkeypatch, item):
        """update_todo: すべての属性のケース、特定のTodoのuidを受け取ることができる"""
        self._monkeys(client, monkeypatch, item)
        json_body = {
            'subject': item['subject']+"_updated",
            'description': item['description']+"_updated",
            'state': item['state']}
        monkeypatch.setattr(Request, 'json_body', json_body)
        assert app.update_todo(item['uid']) == item['uid']

    @pytest.mark.parametrize('item', TESTDATA_DDB_ITEMS)
    def test_Return_uid_case_subject_only(self, client, monkeypatch, item):
        """update_todo: subjectのみのケース、特定のTodoのuidを受け取ることができる"""
        self._monkeys(client, monkeypatch, item)
        json_body = {'subject': item['subject']+"_updated"}
        monkeypatch.setattr(Request, 'json_body', json_body)
        assert app.update_todo(item['uid']) == item['uid']

    @pytest.mark.parametrize('item', TESTDATA_DDB_ITEMS)
    def test_Return_uid_case_discription_only(self, client, monkeypatch, item):
        """update_todo: discriptionのみのケース、特定のTodoのuidを受け取ることができる"""
        self._monkeys(client, monkeypatch, item)
        json_body = {'discription': item['description']+"_updated"}
        monkeypatch.setattr(Request, 'json_body', json_body)
        assert app.update_todo(item['uid']) == item['uid']

    @pytest.mark.parametrize('item', TESTDATA_DDB_ITEMS)
    def test_Return_uid_case_state_only(self, client, monkeypatch, item):
        """update_todo: stateのみのケース、特定のTodoのuidを受け取ることができる"""
        self._monkeys(client, monkeypatch, item)
        json_body = {'state': item['state']}
        monkeypatch.setattr(Request, 'json_body', json_body)
        assert app.update_todo(item['uid']) == item['uid']

    def test_Raise_BadRequestError_case_None_json_body(self, client, monkeypatch):
        """update_todo: json_bodyがNoneのケース、例外を発生させることができる"""
        self._monkeys(client, monkeypatch)
        with pytest.raises(BadRequestError):
            app.update_todo("_uid")
