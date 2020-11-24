from typing import DefaultDict
from uuid import uuid4

from boto3.dynamodb.conditions import Key, Attr

DEFAULT_USERNAME = 'default'


class DynamoDBTodo():
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self):
        response = self._table.scan()
        return response['Items']

    def list_items(self, username=DEFAULT_USERNAME):
        response = self._table.query(
            KeyConditionExpression=Key('username').eq(username)
        )
        return response['Items']

    def add_item(self, subject, description=None, metadata=None, username=DEFAULT_USERNAME):
        uid = str(uuid4())
        self._table.put_item(
            Item={
                'uid': uid,
                'subject': subject,
                'description': description if description is not None else "",
                'state': 'unstarted',
                'metadata': metadata if metadata is not None else {},
                'username': username,
            }
        )
        return uid

    def get_item(self, uid, username=DEFAULT_USERNAME):
        response = self._table.get_item(
            Key={
                'username': username,
                'uid': uid,
            },
        )
        return response['Item']

    def delete_item(self, uid, username=DEFAULT_USERNAME):
        self._table.delete_item(
            Key={
                'username': username,
                'uid': uid,
            }
        )

    def update_item(self, uid, subject=None, description=None, state=None,
                    metadata=None, username=DEFAULT_USERNAME):
        item = self.get_item(uid, username)
        if subject is not None:
            item['subject'] = subject
        if description is not None:
            item['description'] = description
        if state is not None:
            item['state'] = state
        if metadata is not None:
            item['metadata'] = metadata
        self._table.put_item(Item=item)
