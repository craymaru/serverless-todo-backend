MOCK_DDB_SCHEMA = {
    "TableName": "serverless-todos",
    "KeySchema": [
        {"KeyType": "HASH", "AttributeName": "username"},
        {"KeyType": "RANGE", "AttributeName": "uid"}
    ],
    "AttributeDefinitions": [
        {"AttributeType": "S", "AttributeName": "username"},
        {"AttributeType": "S", "AttributeName": "uid"}
    ],
    "ProvisionedThroughput": {
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5,
    }
}