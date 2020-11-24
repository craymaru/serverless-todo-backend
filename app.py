import os
from re import search

import boto3
from chalice import Chalice
from chalice.app import BadRequestError

from chalicelib import db
from chalicelib import validates


app = Chalice(app_name='serverless-todo-backend')
app.debug = True

_DB = None


def get_app_db():
    global _DB
    if _DB is None:
        _DB = db.DynamoDBTodo(
            boto3.resource('dynamodb').Table(
                os.environ['APP_TABLE_NAME']
            )
        )
    return _DB


@app.route('/todos', methods=['GET'])
def get_todos():
    query = ''
    query_params = app.current_request.query_params
    if query_params is not None:
        q = query_params.get('q')
        s = query_params.get('s')
        search = query_params.get('search')
        query = q if q else s if s else search if search else ""
    return get_app_db().list_items(query=query)


@app.route('/todos', methods=['POST'])
def add_new_todo():
    body = app.current_request.json_body
    if body is None:
        raise BadRequestError('current_request.json_body is None.')

    subject = body.get('subject')
    description = body.get('description')
    metadata = body.get('metadata')
    
    validates.subject(subject)
    validates.description(description)
    validates.metadata(metadata) if metadata is not None else None
    # validates.username(username)

    return get_app_db().add_item(
        subject=subject,
        description=description,
        metadata=metadata,
    )


@app.route('/todos/{uid}', methods=['GET'])
def get_todo(uid):
    return get_app_db().get_item(uid)


@app.route('/todos/{uid}', methods=['DELETE'])
def delete_todo(uid):
    return get_app_db().delete_item(uid)


@app.route('/todos/{uid}', methods=['PUT'])
def update_todo(uid):
    body = app.current_request.json_body
    if body is None:
        BadRequestError("json_body is None.")

    subject = body.get('subject')
    description = body.get('description')
    state = body.get('state')
    metadata = body.get('metadata')

    validates.subject(subject)
    validates.description(description)
    validates.state(state)
    validates.metadata(metadata)
    # validates.username(username)

    get_app_db().update_item(
        uid,
        subject=subject,
        description=description,
        state=state,
        metadata=metadata
    )