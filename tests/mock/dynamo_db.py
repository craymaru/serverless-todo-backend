import boto3


class MockDynamoDB():
    """moto.mock_dynamodb2で作成されたDynamoDBを操作"""

    def __init__(self):
        self._mock_dynamodb = None
        self._mock_table = None
        self._last_responses = []

    def create_table(self, *, TableName, KeySchema, AttributeDefinitions, ProvisionedThroughput):
        """DynamoDBのテーブルを作成"""

        _mock_dynamodb = boto3.resource("dynamodb")
        self._mock_table = _mock_dynamodb.create_table(
            TableName=TableName,
            KeySchema=KeySchema,
            AttributeDefinitions=AttributeDefinitions,
            ProvisionedThroughput=ProvisionedThroughput,
        )
        return self

    def add_items(self, add_items, *args):
        """DynamoDBのテーブルに複数のアイテムを追加"""

        self._responses = [
            self._mock_table.put_item(Item=data) for data in add_items
        ]
        return self

    def mock_dynamodb(self):
        """Return: mock_dynamodb"""
        return self._mock_dynamodb

    def mock_table(self):
        """Return: mock_table"""
        return self._mock_table

    def last_responses(self):
        """Return: last_responses"""
        return self._last_responses
