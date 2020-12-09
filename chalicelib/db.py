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
    """特定の DynamoDB テーブルに CRUD を行います

    self.methods:
        list_all_items : すべての Todo オブジェクトをスキャンします
        list_items     : username と query に基づき、Todo オブジェクトのリストを取得します
        add_item       : Todo オブジェクトを新規に追加します
        get_item       : 特定の Todo オブジェクトを取得します
        delete_item    : 特定の Todo オブジェクトを削除します
        update_item    : 特定の Todo オブジェクトを更新します

    constructer: 
        Args: 
            table_resource (boto3.resource.Table): 
                リソースとエンドポイントとテーブルを指定済みの boto3.resource.Table インスタンス

    self:
        _table (boto3.resource.Table):
            特定の DynamoDB テーブルを指定済みの boto3.resource.Table インスタンスを格納します。

    """

    def __init__(self, table_resource):
        self._table = table_resource

    def get_pagenated_items(self, **kwargs):
        while True:
            response = self._table.scan(**kwargs)
            for item in response['Items']:
                yield item
            if 'LastEvaluatedKey' not in response:
                break
            kwargs.update(ExclusiveStartKey=response['LastEvaluatedKey'])

    @except_endpoint_connection_error
    def list_all_items(self):
        """すべての Todo オブジェクトをスキャンします(ページネーション試用)"""
        records = self.get_pagenated_items()
        return list(records)

    # @except_endpoint_connection_error
    # def list_all_items(self):
    #     """すべての Todo オブジェクトをスキャンします"""
    #     response = self._table.scan()
    #     return response['Items']

    @except_endpoint_connection_error
    def list_items(self, query='', username=DEFAULT_USERNAME):
        """username と query に基づき、Todo オブジェクトのリストを取得します

        DynamoDB テーブルに登録されている特定のユーザーの Todo オブジェクトから、
        subject、description いずれかに検索クエリを含む Todo オブジェクトのリストを取得します。

        Args:
            query (str): 検索クエリが渡ってきます クエリがない場合空文字を指定します
            username (str): Todo のユーザー名が渡ってきます

        Return:
            list: Todo オブジェクトのリストを返します

        """
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
        """Todo オブジェクトを新規に追加します

        DynamoDB テーブルに特定のユーザーの Todo オブジェクトを追加します。
        uid は uuid4 で新規に生成します。*1
        state は 初期値に 'unstarted' が設定されます。
        subject, description, state, username キーの値にバリデーションを行います。

        (*1 同一ユーザーの Todo オブジェクトにおける uuid4 の衝突は今回の仕様では考慮しません。)

        Args:
            subject (str): Todo のタイトルが渡ってきます
            description (str): Todo の説明 が渡ってきます 指定がない場合空文字を指定します
            username (str): Todo のユーザー名が渡ってきます

        Raises:
            BadRequestError: バリデーションに失敗したケースで例外が発生します

        Return:
            str: 登録に成功した Todo オブジェクトの uid を返します

        """
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
        """特定の Todo オブジェクトを取得します

        DynamoDB テーブルから特定のユーザー、uid の Todo オブジェクトを取得します。

        Args:
            uid (str): 取得する uid が渡ってきます
            username (str): 取得する Todo のユーザー名が渡ってきます

        Raises:
            NotFoundError: DynamoDB のレスポンスに Item キーがないケースで例外が発生します

        Return:
            dict: 特定の Todo オブジェクトを返します

        """
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
        """特定の Todo オブジェクトを削除します

        DynamoDB テーブルから特定のユーザー、uid の Todo オブジェクトを削除します。

        Args:
            uid (str): 削除する uid
            username (str): 削除する Todo のユーザー名

        Raises:
            NotFoundError: DynamoDB のレスポンスの Attributes の中に uid キーがないケースで例外が発生します

        Return:
            dict: 削除された Todo オブジェクトの uid を返します

        """
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
        """特定の Todo オブジェクトを更新します

        DynamoDB テーブルから特定のユーザー、uid の Todo オブジェクトを更新します。
        subject, description, state, username キーの値にバリデーションを行います。

        Args:
            subject (str): Todo のタイトルが渡ってきます
            description (str): Todo の説明が渡ってきます
            username (str): Todo のユーザー名が渡ってきます
            state (str): Todo のステータスが渡ってきます

        Raises:
            BadRequestError: バリデーションに失敗したケースで例外が発生します
            NotFoundError: DynamoDB のレスポンスの Attributes の中に uid キーがないケースで例外が発生します

        Return:
            str: 更新に成功した Todo オブジェクトの uid を返します

        """
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
