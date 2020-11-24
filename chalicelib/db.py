from typing import DefaultDict
from uuid import uuid4

from boto3.dynamodb.conditions import Key, Attr

from chalicelib import validates

DEFAULT_USERNAME = 'default'


class DynamoDBTodo():
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self):
        response = self._table.scan()
        return response['Items']

    def list_items(self, query=None, username=DEFAULT_USERNAME):
        response = self._table.query(
            KeyConditionExpression=Key('username').eq(username),
            FilterExpression=(
                Attr('subject').contains(query) |
                Attr('description').contains(query)
            )
        )
        return response['Items']

    def add_item(self, subject, description=None, username=DEFAULT_USERNAME):
        uid = str(uuid4())
        subject = subject
        description = description if description is not None else ""
        state = 'unstarted'
        username = username

        validates.subject(subject)
        validates.description(description)
        validates.state(state)
        validates.username(username)

        self._table.put_item(
            Item={
                'uid': uid,
                'subject': subject,
                'description': description,
                'state': state,
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
        validates.username(username)
        self._table.delete_item(
            Key={
                'username': username,
                'uid': uid,
            }
        )

    def update_item(self, uid, subject=None, description=None,
                    state=None, username=DEFAULT_USERNAME):
        validates.username(username)
        item = self.get_item(uid, username)
        if subject is not None:
            validates.subject(subject)
            item['subject'] = subject
        if description is not None:
            validates.subject(description)
            item['description'] = description
        if state is not None:
            validates.subject(state)
            item['state'] = state
        self._table.put_item(Item=item)
