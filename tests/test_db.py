from moto import mock_dynamodb2

import app
from tests.mock import mock_dynamodb as mock


@mock_dynamodb2
class TestAllItems:

    def monkeys(self, monkeypatch):
        monkeypatch.setenv('APP_TABLE_NAME', 'serverless-todos')

    def test_Return_all_items_list(self, monkeypatch):
        monkeypatch.setenv('APP_TABLE_NAME', 'serverless-todos')
        print(mock.test_data_01())
        assert app.get_app_db().list_all_items() == mock.test_data_01()
