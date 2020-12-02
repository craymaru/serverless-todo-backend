from typing import DefaultDict
from uuid import uuid4

from botocore.exceptions import EndpointConnectionError
from boto3.dynamodb.conditions import Key, Attr
from chalice import NotFoundError

from chalicelib.validates import Validates
from chalicelib.exceptions import DatabaseConnectionError


DEFAULT_USERNAME = 'default'


def except_endpoint_connection_error(func):
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except EndpointConnectionError:
            raise DatabaseConnectionError('Failed to connect to database.')
    return _wrapper


class DynamoDBTodo():
    def __init__(self, table_resource):
        self._table = table_resource

    @except_endpoint_connection_error
    def list_all_items(self):
        response = self._table.scan()
        return response['Items']

    @except_endpoint_connection_error
    def list_items(self, query='', username=DEFAULT_USERNAME):
        response = self._table.query(
            KeyConditionExpression=Key('username').eq(username),
            FilterExpression=(
                Attr('subject').contains(query) |
                Attr('description').contains(query)
            )
        )
        return response['Items']

    @except_endpoint_connection_error
    def add_item(self, subject, description='', username=DEFAULT_USERNAME):
        item = {
            'uid': str(uuid4()),
            'subject': subject,
            'description': description,
            'state': 'unstarted',
            'username': username
        }
        Validates.subject(item['subject'])
        Validates.description(item['description'])
        Validates.state(item['state'])
        Validates.username(item['username'])

        self._table.put_item(Item=item, ReturnValues='ALL_OLD')
        return item['uid']

    @except_endpoint_connection_error
    def get_item(self, uid, username=DEFAULT_USERNAME):
        response = self._table.get_item(
            Key={
                'username': username,
                'uid': uid
            })
        try:
            res = response['Item']
        except KeyError:
            raise NotFoundError(f"Todo not found. (id: {uid})")
        return res

    @except_endpoint_connection_error
    def delete_item(self, uid, username=DEFAULT_USERNAME):
        Validates.username(username)
        response = self._table.delete_item(
            Key={
                'username': username,
                'uid': uid,
            },
            ReturnValues='ALL_OLD')
        try:
            res = response['Attributes']['uid']
        except KeyError:
            raise NotFoundError(f"Todo not found. (id: {uid})")
        return res

    @except_endpoint_connection_error
    def update_item(self, uid, subject=None, description=None,
                    state=None, username=DEFAULT_USERNAME):
        Validates.username(username)
        item = self.get_item(uid, username)
        if subject is not None:
            Validates.subject(subject)
            item['subject'] = subject
        if description is not None:
            Validates.description(description)
            item['description'] = description
        if state is not None:
            Validates.state(state)
            item['state'] = state
        response = self._table.put_item(Item=item, ReturnValues='ALL_OLD')
        try:
            res = response['Attributes']['uid']
        except KeyError:
            raise NotFoundError(f"Todo not found. (id: {uid})")
        return res
