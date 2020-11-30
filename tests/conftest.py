import pytest
from moto import mock_dynamodb2

from app import app as chalice_app

from tests.mock.dynamo_db import MockDynamoDB
from tests.mock.ddb_schema import MOCK_DDB_SCHEMA


APP_TABLE_NAME = 'serverless-todos'


@pytest.fixture()
def app():
    return chalice_app


@pytest.fixture(autouse=True)
def set_envs(monkeypatch):
    monkeypatch.setenv('APP_TABLE_NAME', APP_TABLE_NAME)


@pytest.fixture(autouse=True)
def mock():
    with mock_dynamodb2():
        _ddb = MockDynamoDB()
        table = _ddb.create_table(**MOCK_DDB_SCHEMA)
        yield table
