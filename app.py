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
    """トークンから cognito:username を取得
    
    Return:
        str: cognito:username を返します
        None: cognito:username がない場合 None を返します
    """
    try:
        username = current_request.context['authorizer']['claims']["cognito:username"]
    except KeyError:
        username = None
    return username


def get_app_db():
    """DynamoDBTodo インスタンスを取得します

    Todo の DynamoDB テーブルを取得し、グローバル変数 _DB に格納します。
    このとき環境変数 APP_TABLE_NAME を参照し接続先のテーブル名を決定するため、
    デプロイのステージごとに DynamoDB テーブルを変更することができます。
    環境変数の定義は .chalice/config.json を参照してください。

    envs:
        DYNAMO_DB_ENDPOINT:
            接続する DynamoDB のエンドポイント
            この環境変数が存在しない場合は、「呼び出し環境のcredentialsと同一の
            AWSアカウント/リージョンに属するDynamoDB」がエンドポイントとなります。
        APP_TABLE_NAME: 接続する DynamoDB のテーブル名

    Return:
        DynamoDBTodo(instance):
            DynamoDB のエンドポイントとテーブルへのアクセスを内包した DynamoDBTodo インスタンスを返します

    Examples:
        get_app_db().list_items()   username と query に基づいて Todo を取得します
        get_app_db().get_item()    特定の Todo を取得します
        get_app_db().add_item()    Todo を新規登録します
        get_app_db().update_item() Todo を更新します
        get_app_db().delete_item() Todo を削除します

    """
    global _DB
    if _DB is None:
        endpoint = os.environ.get('DYNAMO_DB_ENDPOINT')
        tablename = os.environ['APP_TABLE_NAME']
        _DB = db.DynamoDBTodo(
            boto3.resource('dynamodb', endpoint_url=endpoint).Table(tablename)
        )
    return _DB


@app.route('/todos', methods=['GET'], cors=True, authorizer=authorizer)
def get_todos():
    """クエリに基づき、Todo のリストを取得する DynamoDBTodo.list_items をコールします

    リクエストに含まれる Amazon Cognito の トークンを参照し、
    username ごとに DynamoDB テーブルから Todo オブジェクトを取得し、リストを返します。

    このとき検索クエリが指定されている場合は、
    Todo の subject, description キーの値に、検索クエリが含まれているものを取得します。

    取得のため、DynamoDBTodo.list_items をコールします。

    Query Params:
        ?q, ?s, ?search (str): 検索クエリ
        上記の 3 つの params はすべて検索クエリです。
        先頭から順に検索クエリの存在を確認し、見つかった場合は残りの検索クエリは無視します。
    
        クエリの指定のサンプル
        `$ http POST <ENDPOINT_URI>/todos?q=<QUERY>`
        (* 上記のコマンドは httpie パッケージを使用しています)

    Return:
        list: Todo オブジェクトのリストを返します

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


@app.route('/todos', methods=['POST'], cors=True, authorizer=authorizer)
def add_new_todo():
    """Todo を新規追加する DynamoDBTodo.add_item をコールします

    リクエストの json_body に含まれているパラメータをバリデーションし、
    DynamoDB テーブルに特定のユーザーの Todo オブジェクトを追加するため、
    DynamoDBTodo.add_item をコールします。

    Raises:
        BadRequestError:
            json_body が存在しないケースで例外が発生します。
            バリデーションに失敗したケースで例外が発生します。

    Return:
        str: 登録に成功した Todo の uid を返します

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


@app.route('/todos/{uid}', methods=['GET'], cors=True, authorizer=authorizer)
def get_todo(uid):
    """特定の Todo オブジェクトを取得する DynamoDBTodo.get_item をコールします

    DynamoDB テーブルから特定のユーザー、uid の Todo オブジェクトを取得するため、
    DynamoDBTodo.get_item をコールします。

    Args:
        uid (str): 取得する uid を指定します

    Return:
        dict: 特定の Todo オブジェクトを返します

    """
    username = get_authorized_username(app.current_request)
    return get_app_db().get_item(uid=uid, username=username)


@app.route('/todos/{uid}', methods=['DELETE'], cors=True, authorizer=authorizer)
def delete_todo(uid):
    """特定の Todo オブジェクトを削除する DynamoDBTodo.delete_item をコールします

    DynamoDB テーブルから特定のユーザー、uid の Todo オブジェクトを削除するため、
    DynamoDBTodo.delete_item をコールします。

    Args:
        uid (str): 削除する Todo の uid を指定します

    Return:
        uid: (str): 正常に削除された Todo の uid を返します

    """
    username = get_authorized_username(app.current_request)
    return get_app_db().delete_item(uid=uid, username=username)


@app.route('/todos/{uid}', methods=['PUT'], cors=True, authorizer=authorizer)
def update_todo(uid):
    """特定の Todo オブジェクトを更新する DynamoDBTodo.update_item をコールします

    リクエストに含まれる json_body に格納されているパラメータをバリデーションします。

    DynamoDB テーブルから特定のユーザー、uid の Todo オブジェクトを更新するため、
    DynamoDBTodo.update_item をコールします。

    Raises:
        BadRequestError:
            json_body が存在しないケースで例外が発生します。
            バリデーションに失敗したケースで例外が発生します。

    Return:
        uid: (str): 正常に更新された Todo の uid を返す

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


@app.route('/', cors=True)
def get_index():
    """ウェルカムメッセージを返します"""
    return {'message': 'Welcome to serverless-todo api!'}


@app.route('/all_todos', methods=['GET'], cors=True)
def get_index():
    """ページネーションの試用"""
    return get_app_db().list_all_items()