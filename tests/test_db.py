import pytest
from chalice import NotFoundError

import app

from tests.conftest import APP_TABLE_NAME
from tests.conftest import init_dynamodb_mock
from tests.testcases.ddb_response_items import TESTCASE_DDB_RESPONSE_ITEMS


class DBTest:

    @staticmethod
    def monkeys(monkeypatch):
        monkeypatch.setenv('APP_TABLE_NAME', APP_TABLE_NAME)


class TestListAllItems(DBTest):

    @init_dynamodb_mock
    def test_Return_all_items_list(self, monkeypatch):
        self.monkeys(monkeypatch)
        assert app.get_app_db().list_all_items() == TESTCASE_DDB_RESPONSE_ITEMS


class TestListItems(DBTest):

    @init_dynamodb_mock
    def test_Return_items_list(self, monkeypatch):
        self.monkeys(monkeypatch)
        query = ''
        username = 'default'
        assert app.get_app_db().list_items(
            query=query, username=username) == TESTCASE_DDB_RESPONSE_ITEMS

    @init_dynamodb_mock
    def test_Return_items_list_With_query(self, monkeypatch):
        self.monkeys(monkeypatch)
        query = '🐈'
        username = 'default'
        expected_list = []
        for d in TESTCASE_DDB_RESPONSE_ITEMS:
            if query in d['subject'] or query in d['description']:
                expected_list.append(d)
        assert app.get_app_db().list_items(query=query, username=username) == expected_list


class TestAddItem(DBTest):

    def test_Return_add_item(self):
        pass


class TestGetItem(DBTest):

    @init_dynamodb_mock
    def test_Return_get_item(self, monkeypatch):
        self.monkeys(monkeypatch)
        items = TESTCASE_DDB_RESPONSE_ITEMS
        for i, _ in enumerate(items):
            uid = items[i]['uid']
            username = 'default'
            assert app.get_app_db().get_item(
                uid, username=username) == items[i]

    @init_dynamodb_mock
    def test_Raise_NotFoundError_when_without_item(self, monkeypatch):
        self.monkeys(monkeypatch)
        items = TESTCASE_DDB_RESPONSE_ITEMS
        uid = items[0]['uid']
        username = 'default'
        with pytest.raises(NotFoundError):
            app.get_app_db().get_item("_", username=username)


class TestDeleteItem(DBTest):

    @init_dynamodb_mock
    def test_Return_delete_item(self, monkeypatch):
        self.monkeys(monkeypatch)
        items = TESTCASE_DDB_RESPONSE_ITEMS
        uid = items[0]['uid']
        username = 'default'
        assert app.get_app_db().delete_item(uid, username=username) == uid


class TestUpdateItem(DBTest):

    def test_Return_update_item(self):
        pass

    @init_dynamodb_mock
    def test_Return_delete2_item(self, monkeypatch):
        self.monkeys(monkeypatch)
        items = TESTCASE_DDB_RESPONSE_ITEMS
        uid = items[0]['uid']
        username = 'default'
        assert app.get_app_db().delete_item(uid, username=username) == uid
