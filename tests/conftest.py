import pytest
from moto import mock_dynamodb2

from app import app as chalice_app

from tests.mock.dynamo_db import MockDynamoDB
from tests.mock.ddb_schema import MOCK_DDB_SCHEMA
from tests.testcases.ddb_response_items import TESTCASE_DDB_RESPONSE_ITEMS


APP_TABLE_NAME = 'serverless-todos'


@pytest.fixture(scope='module')
def app():
    return chalice_app


def init_dynamodb_mock(func):
    @mock_dynamodb2
    def _wrapper(self, *args, monkeypatch, **kwargs):
        _MOCK_DDB = MockDynamoDB()
        _MOCK_DDB.create_table(**MOCK_DDB_SCHEMA).add_items(TESTCASE_DDB_RESPONSE_ITEMS)
        return func(self, *args, monkeypatch, **kwargs)
    return _wrapper
