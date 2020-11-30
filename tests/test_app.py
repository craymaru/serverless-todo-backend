import pytest
from http import HTTPStatus

from chalice import BadRequestError
from chalice.app import Request

import app
from chalicelib.validates import Validates
from chalicelib.db import DynamoDBTodo

from tests.testdata.ddb_items import TESTDATA_DDB_ITEMS
from tests.testdata.non_str_types import TESTDATA_NON_STR_TYPES


class TestApp:

    @staticmethod
    def set_env(client):
        client.get('/')


class TestGetIndex:
    def test_Return_status_code_200_and_json(self, client):
        response = client.get('/')
        assert response.status_code == HTTPStatus.OK
        assert True if response.json else False == True


class TestGetAppDB(TestApp):

    def test_Return_DynamoDBTodo_class(self):
        assert app.get_app_db().__class__ == DynamoDBTodo


class TestGetTodos(TestApp):

    def _monkeys(self, client, monkeypatch):
        super().set_env(client)
        monkeypatch.setattr(DynamoDBTodo, 'list_items',
                            lambda *args, **kwargs: TESTDATA_DDB_ITEMS)

    def test_Return_todos_list(self, client, monkeypatch):
        self._monkeys(client, monkeypatch)
        assert app.get_todos() == TESTDATA_DDB_ITEMS


class TestAddNewTodo(TestApp):

    def _monkeys(self, client, monkeypatch, item):
        super().set_env(client)
        from uuid import uuid4
        monkeypatch.setattr(DynamoDBTodo, 'add_item',
                            lambda *args, **kwargs: str(uuid4()))

    @pytest.mark.parametrize('item', [item for item in TESTDATA_DDB_ITEMS])
    def test_Return_uid_when_Post_subject_and_description(self, client, monkeypatch, item):
        self._monkeys(client, monkeypatch, item)
        json_body = {'subject': 'neko', 'description': 'meow'}
        monkeypatch.setattr(Request, 'json_body', json_body)
        actual = app.add_new_todo()
        assert type(actual) == str
        assert len(actual) == 36

    @pytest.mark.parametrize('item', [item for item in TESTDATA_DDB_ITEMS])
    def test_Return_uid_when_Post_subject_only(self, client, monkeypatch, item):
        self._monkeys(client, monkeypatch, item)
        json_body = {'subject': 'neko'}
        monkeypatch.setattr(Request, 'json_body', json_body)
        actual = app.add_new_todo()
        assert type(actual) == str
        assert len(actual) == 36

    @pytest.mark.parametrize('item', [item for item in TESTDATA_DDB_ITEMS])
    def test_Raise_BadRequestError_when_None_subject(self, client, monkeypatch, item):
        self._monkeys(client, monkeypatch, item)
        json_body = {}
        monkeypatch.setattr(Request, 'json_body', json_body)
        with pytest.raises(BadRequestError):
            app.add_new_todo()

    @pytest.mark.parametrize('item', [item for item in TESTDATA_DDB_ITEMS])
    def test_Raise_BadRequestError_when_Post_without_subject(self, client, monkeypatch, item):
        self._monkeys(client, monkeypatch, item)
        json_body = {'description': 'meow'}
        monkeypatch.setattr(Request, 'json_body', json_body)
        with pytest.raises(BadRequestError):
            app.add_new_todo()


class TestGetTodo(TestApp):

    def _monkeys(self, monkeypatch):
        def _get_item(self, uid):
            for item in TESTDATA_DDB_ITEMS:
                if item['uid'] == uid:
                    return item
        monkeypatch.setattr(DynamoDBTodo, 'get_item', _get_item)

    @pytest.mark.parametrize('item', [item for item in TESTDATA_DDB_ITEMS])
    def test_Return_todo_dict(self, monkeypatch, item):
        self._monkeys(monkeypatch)
        assert app.get_todo(uid=item['uid']) == item


class TestDeleteTodo(TestApp):

    def _monkeys(self, monkeypatch):
        def _delete_item(self, uid):
            for item in TESTDATA_DDB_ITEMS:
                if item['uid'] == uid:
                    return item['uid']
        monkeypatch.setattr(DynamoDBTodo, 'delete_item', _delete_item)

    @pytest.mark.parametrize('item', [item for item in TESTDATA_DDB_ITEMS])
    def test_Return_uid(self, monkeypatch, item):
        self._monkeys(monkeypatch)
        assert app.delete_todo(uid=item['uid']) == item['uid']


class TestUpdateTodo(TestApp):

    def _monkeys(self, client, monkeypatch):

        super().set_env(client)

        def _update_item(self, uid, **kwargs):
            for item in TESTDATA_DDB_ITEMS:
                if item['uid'] == uid:
                    return item['uid']
        monkeypatch.setattr(DynamoDBTodo, 'update_item', _update_item)

    @pytest.mark.parametrize('item', [item for item in TESTDATA_DDB_ITEMS])
    def test_Return_uid_when_Update_subject_description_and_state(self, client, monkeypatch, item):
        self._monkeys(client, monkeypatch)
        json_body = {
            'subject': 'neko',
            'description': 'meow',
            'state': 'completed'
        }
        monkeypatch.setattr(Request, 'json_body', json_body)
        assert app.update_todo(item['uid']) == item['uid']

    @pytest.mark.parametrize('item', [item for item in TESTDATA_DDB_ITEMS])
    def test_Return_uid_when_Update_subject_only(self, client, monkeypatch, item):
        self._monkeys(client, monkeypatch)
        json_body = {'subject': 'neko'}
        monkeypatch.setattr(Request, 'json_body', json_body)
        assert app.update_todo(item['uid']) == item['uid']

    @pytest.mark.parametrize('item', [item for item in TESTDATA_DDB_ITEMS])
    def test_Return_uid_when_Update_discription_only(self, client, monkeypatch, item):
        self._monkeys(client, monkeypatch)
        json_body = {'discription': 'neko'}
        monkeypatch.setattr(Request, 'json_body', json_body)
        assert app.update_todo(item['uid']) == item['uid']

    @pytest.mark.parametrize('item', [item for item in TESTDATA_DDB_ITEMS])
    def test_Return_uid_when_Update_state_only(self, client, monkeypatch, item):
        self._monkeys(client, monkeypatch)
        json_body = {'state': 'completed'}
        monkeypatch.setattr(Request, 'json_body', json_body)
        assert app.update_todo(item['uid']) == item['uid']


class TestSharedRaises(TestApp):
    expected_str = TESTDATA_DDB_ITEMS[0]['uid']

    def _monkeys(self, client, monkeypatch):
        super().set_env(client)
        monkeypatch.setattr(DynamoDBTodo, 'add_item',
                            lambda *args, **kwargs: self.expected_str)
        monkeypatch.setattr(DynamoDBTodo, 'update_item',
                            lambda *args, **kwargs: self.expected_str)

    def test_Raise_BadRequestError_when_None_json_body(self, client, monkeypatch):
        self._monkeys(client, monkeypatch)
        with pytest.raises(BadRequestError):
            app.add_new_todo() == self.expected_str
        with pytest.raises(BadRequestError):
            app.update_todo("_uid") == self.expected_str

    def test_Raise_BadRequestError_when_Bad_subject_length(self, client, monkeypatch):
        self._monkeys(client, monkeypatch)
        testcases = [
            '_' * (Validates.SUBJECT_MIN_LEN - 1),
            '_' * (Validates.SUBJECT_MAX_LEN + 1),
            '_' * (Validates.SUBJECT_MAX_LEN * 10)
        ]
        for testcase in testcases:
            json_body = {'subject': testcase}
            monkeypatch.setattr(Request, 'json_body', json_body)
            with pytest.raises(BadRequestError):
                app.add_new_todo() == self.expected_str
            with pytest.raises(BadRequestError):
                app.update_todo("_uid") == self.expected_str

    def test_Raise_BadRequestError_when_Bad_subject_type(self, client, monkeypatch):
        self._monkeys(client, monkeypatch)
        for testcase in TESTDATA_NON_STR_TYPES:
            json_body = {'subject': testcase}
            monkeypatch.setattr(Request, 'json_body', json_body)
            with pytest.raises(BadRequestError):
                app.add_new_todo() == self.expected_str
            with pytest.raises(BadRequestError):
                app.update_todo("_uid") == self.expected_str

    def test_Raise_BadRequestError_when_Bad_discription_length(self, client, monkeypatch):
        self._monkeys(client, monkeypatch)
        testcases = [
            '_' * (Validates.DESCRIPTION_MAX_LEN + 1),
            '_' * (Validates.DESCRIPTION_MAX_LEN * 10)
        ]
        for testcase in testcases:
            json_body = {'description': testcase}
            monkeypatch.setattr(Request, 'json_body', json_body)
            with pytest.raises(BadRequestError):
                app.add_new_todo() == self.expected_str
            with pytest.raises(BadRequestError):
                app.update_todo("_uid") == self.expected_str

    def test_Raise_BadRequestError_when_Bad_description_type(self, client, monkeypatch):
        self._monkeys(client, monkeypatch)
        for testcase in TESTDATA_NON_STR_TYPES:
            json_body = {'description': testcase}
            monkeypatch.setattr(Request, 'json_body', json_body)
            with pytest.raises(BadRequestError):
                app.add_new_todo() == self.expected_str
            with pytest.raises(BadRequestError):
                app.update_todo("_uid") == self.expected_str

    def test_Raise_BadRequestError_when_Bad_state_name(self, client, monkeypatch):
        self._monkeys(client, monkeypatch)
        testcases = ["unknown_state"] \
            + [state + " " for state in Validates.STATE_ENUM] \
            + [" " + state for state in Validates.STATE_ENUM]
        for testcase in testcases:
            json_body = {'state': testcase}
            monkeypatch.setattr(Request, 'json_body', json_body)
            with pytest.raises(BadRequestError):
                app.add_new_todo() == self.expected_str
            with pytest.raises(BadRequestError):
                app.update_todo("_uid") == self.expected_str

    def test_Raise_BadRequestError_when_Bad_state_type(self, client, monkeypatch):
        self._monkeys(client, monkeypatch)
        for testcase in TESTDATA_NON_STR_TYPES:
            json_body = {'state': testcase}
            monkeypatch.setattr(Request, 'json_body', json_body)
            with pytest.raises(BadRequestError):
                app.add_new_todo() == self.expected_str
            with pytest.raises(BadRequestError):
                app.update_todo("_uid") == self.expected_str
