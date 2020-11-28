import pytest
from moto import mock_dynamodb2

from app import app as chalice_app
from tests.mock import mock_dynamodb as mock


@pytest.fixture(scope='module')
def app():
    return chalice_app


@mock_dynamodb2
def init_mock():
    _DB = mock.create_dynamo_table()
    [_DB.put_item(Item=data) for data in mock.test_data_01()]
init_mock()