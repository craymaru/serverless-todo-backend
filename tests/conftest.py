import pytest
from moto import mock_dynamodb2

from app import app as chalice_app
from tests.mock import dynamodb as mock


@pytest.fixture(scope='module')
def app():
    return chalice_app


def init_dynamodb_mock(func):
    @mock_dynamodb2
    def _wrapper(self, *args, monkeypatch, **kwargs):
        _MOCK_DB = mock.create_table()
        [_MOCK_DB.put_item(Item=data) for data in mock.test_data_01()]
        return func(self, *args, monkeypatch, **kwargs)
    return _wrapper
