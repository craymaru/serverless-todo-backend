import os

import boto3
from chalice import Chalice
from chalice import CognitoUserPoolAuthorizer
from chalice.app import BadRequestError

from chalicelib import db
from chalicelib.validates import Validates


_DB = None


app = Chalice(app_name='serverless-todo-backend')
app.debug = True
authorizer = CognitoUserPoolAuthorizer(
    'ToDoAppUserPool', provider_arns=[os.environ.get('USER_POOL_ARN')]
)


def get_authorized_username(current_request):
    """ Auth時のトークンからcognito:usernameを取得"""
    try:
        username = current_request.context['authorizer']['claims']["cognito:username"]
    except KeyError:
        username = None
    return username


def get_app_db():
    """ TodoのDynamoDBテーブルを取得

    Todo の DynamoDB テーブルを取得し、グローバル変数 _DB に格納します
    このとき環境変数 APP_TABLE_NAME を参照し接続先のテーブル名を決定するため、
    デプロイのステージごとに DynamoDB テーブルを変更することができます
    環境変数の定義は .chalice/config.json を参照してください

    envs:
        APP_TABLE_NAME: 接続するDynamoDB上のテーブル名
        DYNAMO_DB_ENDPOINT:
            接続するDynamoDBのエンドポイント
            この環境変数が存在しない場合は、「呼び出し環境のcredentialsと同一の
            AWSアカウント/リージョンに属するDynamoDB」にアクセスします

    Return:
        DynamoDBTodo(class):
            DynamoDBへのアクセス情報を内包したDynamoDBTodoインスタンスを返します

    Examples:
        get_app_db().list_items()
        get_app_db().add_item()
        get_app_db().update_item()
        get_app_db().delete_item()

    """
    global _DB
    if _DB is None:
        endpoint = os.environ.get('DYNAMO_DB_ENDPOINT')
        tablename = os.environ['APP_TABLE_NAME']
        _DB = db.DynamoDBTodo(
            boto3.resource('dynamodb', endpoint_url=endpoint).Table(tablename)
        )
    return _DB


@app.route('/todos', methods=['GET'], authorizer=authorizer)
def get_todos():
    """ Todoのリストを取得

    app.current_request.query_params に格納されたURLクエリから、
    DynamoDB を参照し Todo のリストを取得します
    この時、Amazon Cognito の Auth 情報を参照し、
    username ごとのリストを取得します

    Query Params:
        ?q, ?s, ?search (str): Todo検索用のパラメータです
        上記の3つのparamsは同一の検索クエリです
        このURLクエリは Todo の subject, description を検索対象とします

    Return:
        list: Todoオブジェクトのリストを返します

    Example:
        http POST <ENDPOINT_URI>/todos?q=<QUERY>
        (* 上記のコマンドは httpie パッケージを使用しています)

    """
    username = get_authorized_username(app.current_request)
    query = ''
    params = app.current_request.query_params
    if params is not None:
        for key in 'q', 's', 'search':
            if key in params:
                query = params[key]
                break
    return get_app_db().list_items(query=query, username=username)


@app.route('/todos', methods=['POST'], authorizer=authorizer)
def add_new_todo():
    """ 新しいTodoを登録

    app.current_request.json_body に格納されているパラメータを検証し、
    DynamoDB にレコードを新規追加します

    Raises:
        BadRequestError:
            json_bodyが存在しないケース
            各種varidatesに失敗したケース

    Return:
        str: 登録に成功したuidを返す
    """
    body = app.current_request.json_body
    if body is None:
        raise BadRequestError('current_request.json_body is None.')

    subject = body.get('subject')
    description = body.get('description')
    username = get_authorized_username(app.current_request)

    Validates.subject(subject)
    Validates.description(description) if description is not None else None
    Validates.username(username)

    return get_app_db().add_item(
        subject=subject,
        description=description,
        username=username
    )


@app.route('/todos/{uid}', methods=['GET'], authorizer=authorizer)
def get_todo(uid):
    """ 特定のTodoを取得

    DynamoDB から固有の uid を持つ Todo を取得します

    Args:
        uid (str): 取得する uid を指定する

    Return:
        dict: 特定のTodoを返す

    """
    username = get_authorized_username(app.current_request)
    return get_app_db().get_item(uid=uid, username=username)


@app.route('/todos/{uid}', methods=['DELETE'], authorizer=authorizer)
def delete_todo(uid):
    """ 特定のTodoを削除

    DynamoDB から固有の uid を持つ Todo を削除します

    Args:
        uid (str): 削除するTodoのuidを指定する

    Return:
        uid: (str): 正常に削除されたTodoのuidを返す

    """
    username = get_authorized_username(app.current_request)
    return get_app_db().delete_item(uid=uid, username=username)


@app.route('/todos/{uid}', methods=['PUT'], authorizer=authorizer)
def update_todo(uid):
    """ 特定のTodoを更新

    DynamoDB から固有の uid を持つ Todo を取得し、
    app.current_request.json_body に格納されている更新用パラメータを検証し、
    DynamoDB のレコードを更新します

    Raises:
        BadRequestError:
            json_bodyが存在しないケース
            各種varidatesに失敗したケース

    Return:
        uid: (str): 正常に更新されたTodoのuidを返す

    """
    body = app.current_request.json_body
    if body is None:
        raise BadRequestError("json_body is None.")

    subject = body.get('subject')
    description = body.get('description')
    state = body.get('state')
    username = get_authorized_username(app.current_request)

    Validates.subject(subject) if subject is not None else None
    Validates.description(description) if description is not None else None
    Validates.state(state) if state is not None else None
    Validates.username(username)

    return get_app_db().update_item(
        uid=uid,
        subject=subject,
        description=description,
        state=state,
        username=username
    )


@app.route('/')
def get_index():
    return {'message': 'Welcome to serverless-todo api!'}
