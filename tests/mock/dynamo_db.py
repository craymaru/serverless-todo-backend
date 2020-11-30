import boto3


class MockDynamoDB():
    """moto.mock_dynamodb2で作成されたDynamoDBを操作"""

    def __init__(self):
        self.__ddb = None
        self.table = None

    def create_table(self, *, TableName, KeySchema, AttributeDefinitions, ProvisionedThroughput):
        """DynamoDBのテーブルを作成"""
        self.__ddb = boto3.resource("dynamodb")
        self.table = MockDynamoDBTable(
            self.__ddb.create_table(
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
        self.last_responses = []

    def put_items(self, items):
        """DynamoDBのテーブルに複数のアイテムを追加"""

        self.last_responses = [
            self._table.put_item(Item=data) for data in items
        ]
        return self
