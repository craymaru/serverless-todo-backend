from http import HTTPStatus

from chalicelib.db import DynamoDBTodo
import app


def test_test_pipeline(client):
    response = client.get('/test-pipeline')
    assert response.status_code == HTTPStatus.OK
    assert response.json == {'pipeline': 'route'}


class TestGetTodo:
    expected_dict = {
        "description": "meow",
        "state": "unstarted",
        "subject": "wanwan",
        "uid": "519cc5de-b244-45d9-844c-412040bc79a1",
        "username": "default"
    }
    
    def monkeypatch_dynamodb(self, monkeypatch):
            monkeypatch.setattr('app.get_app_db', lambda: DynamoDBTodo("_DB") )
            monkeypatch.setattr(DynamoDBTodo, 'get_item', lambda *_: self.expected_dict)

    def test_Can_get_todo_dict(self, monkeypatch):
        self.monkeypatch_dynamodb(monkeypatch)
        uid = self.expected_dict['uid']
        actual = app.get_todo({uid})
        assert actual == self.expected_dict

