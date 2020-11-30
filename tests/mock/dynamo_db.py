import boto3


class MockDynamoDB():
    """moto.mock_dynamodb2で作成されたDynamoDBを操作"""

    def __init__(self):
        self.table = None
        self._ddb = None
        self._last_responses = []

    def create_table(self, *, TableName, KeySchema, AttributeDefinitions, ProvisionedThroughput):
        """DynamoDBのテーブルを作成"""
        self._ddb = boto3.resource("dynamodb")
        self.table = MockDynamoDBTable(
            self._ddb.create_table(
                TableName=TableName,
                KeySchema=KeySchema,
                AttributeDefinitions=AttributeDefinitions,
                ProvisionedThroughput=ProvisionedThroughput)
        )
        return self

    def set_table(self, table):
        self.table = MockDynamoDBTable(table)


class MockDynamoDBTable:

    def __init__(self, table):
        self._table = table

    def put_items(self, items):
        """DynamoDBのテーブルに複数のアイテムを追加"""

        self._last_responses = [
            self._table.put_item(Item=data) for data in items
        ]
        return self
