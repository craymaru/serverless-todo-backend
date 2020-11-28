from http import HTTPStatus

import pytest

from chalice import BadRequestError
from chalice.app import Request
from chalicelib.db import DynamoDBTodo
from chalicelib import validates
import app


DDB_RESPONSE_ITEMS = [
    {
        "description": "nyao",
        "state": "unstarted",
        "subject": "meow",
        "uid": "37dc42c4-a2df-4606-8b3c-eb6332ef9699",
        "username": "default"
    },
    {
        "description": "nyao",
        "state": "copleted",
        "subject": "meow",
        "uid": "49849666-b06a-479e-8d7d-bf96d9b3e7f8",
        "username": "default"
    },
    {
        "description": "nyao",
        "state": "completed",
        "subject": "meow",
        "uid": "a0baeb00-33f0-4c35-8ac3-6f9333a1de13",
        "username": "default"
    },
    {
        "description": "nyao",
        "state": "unstarted",
        "subject": "meow",
        "uid": "a8debdcd-afbb-4935-94f2-a541cf9c670a",
        "username": "default"
    },
    {
        "description": "nyao",
        "state": "unstarted",
        "subject": "meow",
        "uid": "b863c9c7-a61b-487e-9bdb-310cf8aa92cf",
        "username": "default"
    },
    {
        "description": "nyao",
        "state": "unstarted",
        "subject": "meow",
        "uid": "b8c2a8c9-eed9-41b8-8f99-32e7661e6693",
        "username": "default"
    },
    {
        "description": "nyao",
        "state": "unstarted",
        "subject": "meow",
        "uid": "eca373d1-81b4-48e8-abb2-27f82599c1c7",
        "username": "default"
    }
]

NOT_STR_TESTCASES = [True, False, -1, 0, 1, {'0'}, {'k': 'v'}, [0]]


class APPTest:

    @staticmethod
    def monkeys(monkeypatch):
        monkeypatch.setenv('APP_TABLE_NAME', 'serverless-todos')


class TestGetIndex:
    def test_Return_status_code_200_and_specific_json(self, client):
        response = client.get('/')
        assert response.status_code == HTTPStatus.OK
        assert response.json == {'message': 'serverless todo api'}


class TestGetAppDB(APPTest):

    def monkeys(self, monkeypatch):
        super().monkeys(monkeypatch)

    def test_Return_DynamoDBTodo_class(self, monkeypatch):
        self.monkeys(monkeypatch)
        assert app.get_app_db().__class__ == DynamoDBTodo("").__class__


class TestGetTodos(APPTest):
    expected_list = DDB_RESPONSE_ITEMS

    def monkeys(self, monkeypatch):
        super().monkeys(monkeypatch)

    def test_Return_todos_list(self, monkeypatch):
        self.monkeys(monkeypatch)
        monkeypatch.setattr(DynamoDBTodo, 'list_items',
                            lambda *args, **kwargs: self.expected_list)
        assert app.get_todos() == self.expected_list


class TestAddNewTodo(APPTest):
    expected_str = DDB_RESPONSE_ITEMS[0]['uid']

    def monkeys(self, monkeypatch):
        super().monkeys(monkeypatch)
        monkeypatch.setattr(DynamoDBTodo, 'add_item',
                            lambda *args, **kwargs: self.expected_str)

    def test_Return_uid_when_Post_subject_and_description(self, monkeypatch):
        self.monkeys(monkeypatch)
        json_body = {'subject': 'neko', 'description': 'meow'}
        monkeypatch.setattr(Request, 'json_body', json_body)
        assert app.add_new_todo() == self.expected_str

    def test_Return_uid_when_Post_subject_only(self, monkeypatch):
        self.monkeys(monkeypatch)
        json_body = {'subject': 'neko'}
        monkeypatch.setattr(Request, 'json_body', json_body)
        assert app.add_new_todo() == self.expected_str

    def test_Raise_BadRequestError_when_None_subject(self, monkeypatch):
        self.monkeys(monkeypatch)
        json_body = {}
        monkeypatch.setattr(Request, 'json_body', json_body)
        with pytest.raises(BadRequestError):
            app.add_new_todo() == self.expected_str

    def test_Raise_BadRequestError_when_Post_without_subject(self, monkeypatch):
        self.monkeys(monkeypatch)
        json_body = {'description': 'meow'}
        monkeypatch.setattr(Request, 'json_body', json_body)
        with pytest.raises(BadRequestError):
            app.add_new_todo() == self.expected_str


class TestGetTodo(APPTest):
    expected_dict = DDB_RESPONSE_ITEMS[0]

    def monkeys(self, monkeypatch):
        super().monkeys(monkeypatch)
        monkeypatch.setattr(DynamoDBTodo, 'get_item',
                            lambda *_: self.expected_dict)

    def test_Return_todo_dict(self, monkeypatch):
        self.monkeys(monkeypatch)
        uid = self.expected_dict['uid']
        actual = app.get_todo({uid})
        assert actual == self.expected_dict


class TestDeleteTodo(APPTest):
    expected_str = DDB_RESPONSE_ITEMS[0]['uid']

    def monkeys(self, monkeypatch):
        super().monkeys(monkeypatch)
        monkeypatch.setattr(DynamoDBTodo, 'delete_item',
                            lambda *_: self.expected_str)

    def test_Return_uid(self, monkeypatch):
        self.monkeys(monkeypatch)
        uid = self.expected_str
        actual = app.delete_todo({uid})
        assert actual == self.expected_str


class TestUpdateTodo(APPTest):
    expected_str = DDB_RESPONSE_ITEMS[0]['uid']

    def monkeys(self, monkeypatch):
        super().monkeys(monkeypatch)
        monkeypatch.setattr(DynamoDBTodo, 'update_item',
                            lambda *args, **kwargs: self.expected_str)

    def test_Return_uid_when_Update_subject_description_and_state(self, monkeypatch):
        self.monkeys(monkeypatch)
        json_body = {
            'subject': 'neko',
            'description': 'meow',
            'state': 'completed'
        }
        monkeypatch.setattr(Request, 'json_body', json_body)
        assert app.update_todo("_uid") == self.expected_str

    def test_Return_uid_when_Update_subject_only(self, monkeypatch):
        self.monkeys(monkeypatch)
        json_body = {'subject': 'neko'}
        monkeypatch.setattr(Request, 'json_body', json_body)
        assert app.update_todo("_uid") == self.expected_str

    def test_Return_uid_when_Update_discription_only(self, monkeypatch):
        self.monkeys(monkeypatch)
        json_body = {'discription': 'neko'}
        monkeypatch.setattr(Request, 'json_body', json_body)
        assert app.update_todo("_uid") == self.expected_str

    def test_Return_uid_when_Update_state_only(self, monkeypatch):
        self.monkeys(monkeypatch)
        json_body = {'state': 'completed'}
        monkeypatch.setattr(Request, 'json_body', json_body)
        assert app.update_todo("_uid") == self.expected_str


class TestSharedRaises:
    expected_str = DDB_RESPONSE_ITEMS[0]['uid']

    def monkeys(self, monkeypatch):
        monkeypatch.setenv('APP_TABLE_NAME', 'serverless-todos')
        monkeypatch.setattr(DynamoDBTodo, 'add_item',
                            lambda *args, **kwargs: self.expected_str)
        monkeypatch.setattr(DynamoDBTodo, 'update_item',
                            lambda *args, **kwargs: self.expected_str)

    def test_Raise_BadRequestError_when_None_json_body(self, monkeypatch):
        self.monkeys(monkeypatch)
        with pytest.raises(BadRequestError):
            app.add_new_todo() == self.expected_str
        with pytest.raises(BadRequestError):
            app.update_todo("_uid") == self.expected_str

    def test_Raise_BadRequestError_when_Bad_subject_length(self, monkeypatch):
        self.monkeys(monkeypatch)
        testcases = [
            '_' * (validates.SUBJECT_MIN_LEN - 1),
            '_' * (validates.SUBJECT_MAX_LEN + 1),
            '_' * (validates.SUBJECT_MAX_LEN * 10)
        ]
        for testcase in testcases:
            json_body = {'subject': testcase}
            monkeypatch.setattr(Request, 'json_body', json_body)
            with pytest.raises(BadRequestError):
                app.add_new_todo() == self.expected_str
            with pytest.raises(BadRequestError):
                app.update_todo("_uid") == self.expected_str

    def test_Raise_BadRequestError_when_Bad_subject_type(self, monkeypatch):
        self.monkeys(monkeypatch)
        for testcase in NOT_STR_TESTCASES:
            json_body = {'subject': testcase}
            monkeypatch.setattr(Request, 'json_body', json_body)
            with pytest.raises(BadRequestError):
                app.add_new_todo() == self.expected_str
            with pytest.raises(BadRequestError):
                app.update_todo("_uid") == self.expected_str

    def test_Raise_BadRequestError_when_Bad_discription_length(self, monkeypatch):
        self.monkeys(monkeypatch)
        testcases = [
            '_' * (validates.DESCRIPTION_MAX_LEN + 1),
            '_' * (validates.DESCRIPTION_MAX_LEN * 10)
        ]
        for testcase in testcases:
            json_body = {'description': testcase}
            monkeypatch.setattr(Request, 'json_body', json_body)
            with pytest.raises(BadRequestError):
                app.add_new_todo() == self.expected_str
            with pytest.raises(BadRequestError):
                app.update_todo("_uid") == self.expected_str

    def test_Raise_BadRequestError_when_Bad_description_type(self, monkeypatch):
        self.monkeys(monkeypatch)
        for testcase in NOT_STR_TESTCASES:
            json_body = {'description': testcase}
            monkeypatch.setattr(Request, 'json_body', json_body)
            with pytest.raises(BadRequestError):
                app.add_new_todo() == self.expected_str
            with pytest.raises(BadRequestError):
                app.update_todo("_uid") == self.expected_str

    def test_Raise_BadRequestError_when_Bad_state_name(self, monkeypatch):
        self.monkeys(monkeypatch)
        testcases = ["unknown_state"] \
            + [state + " " for state in validates.STATE_ENUM] \
            + [" " + state for state in validates.STATE_ENUM]
        for testcase in testcases:
            json_body = {'state': testcase}
            monkeypatch.setattr(Request, 'json_body', json_body)
            with pytest.raises(BadRequestError):
                app.add_new_todo() == self.expected_str
            with pytest.raises(BadRequestError):
                app.update_todo("_uid") == self.expected_str

    def test_Raise_BadRequestError_when_Bad_state_type(self, monkeypatch):
        self.monkeys(monkeypatch)
        for testcase in NOT_STR_TESTCASES:
            json_body = {'state': testcase}
            monkeypatch.setattr(Request, 'json_body', json_body)
            with pytest.raises(BadRequestError):
                app.add_new_todo() == self.expected_str
            with pytest.raises(BadRequestError):
                app.update_todo("_uid") == self.expected_str
