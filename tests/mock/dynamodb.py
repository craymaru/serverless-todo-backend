import boto3


def create_table():
    """DynamoDBのテーブル作成"""

    mock_dynamodb = boto3.resource("dynamodb")
    mock_table = mock_dynamodb.create_table(
        TableName="serverless-todos",
        KeySchema=[
            {"KeyType": "HASH", "AttributeName": "username"},
            {"KeyType": "RANGE", "AttributeName": "uid"}
        ],
        AttributeDefinitions=[
            {"AttributeType": "S", "AttributeName": "username"},
            {"AttributeType": "S", "AttributeName": "uid"}
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5,
        },
    )
    return mock_table


def test_data_01():
    """テストデータ"""
    items = [
        {
            "uid": "37dc42c4-a2df-4606-8b3c-eb6332ef9699",
            "subject": "Make cat tower 🐈",
            "description": "Buy materials home improvement store 🔨",
            "state": "completed",
            "username": "default"
        },
        {
            "uid": "49849666-b06a-479e-8d7d-bf96d9b3e7f8",
            "subject": "友達とハンバーガーを食べに行く🍔🍟",
            "description": "友達の家に車で迎えに行く🚗",
            "state": "unstarted",
            "username": "default"
        },
        {
            "uid": "a0baeb00-33f0-4c35-8ac3-6f9333a1de13",
            "subject": "새우칠리 를 만드는🍤",
            "description": "친구와 함께 만들기🐣",
            "state": "unstarted",
            "username": "default"
        },
        {
            "uid": "a8debdcd-afbb-4935-94f2-a541cf9c670a",
            "subject": "поехать на море🚢",
            "description": "Иди посмотреть на дельфинов🐬",
            "state": "started",
            "username": "default"
        },
        {
            "uid": "b863c9c7-a61b-487e-9bdb-310cf8aa92cf",
            "subject": "前往南部島嶼🌴",
            "description": "見媽媽👩",
            "state": "completed",
            "username": "default"
        },
        {
            "uid": "b8c2a8c9-eed9-41b8-8f99-32e7661e6693",
            "subject": "ابحث عن برسيم رباعي الأوراق 🍀",
            "description": "للهدايا 🎁",
            "state": "started",
            "username": "default"
        },
        {
            "uid": "eca373d1-81b4-48e8-abb2-27f82599c1c7",
            "subject": "ดูดาวตก🌠",
            "description": "👩‍❤️‍👩เดทคู่👨‍❤️‍👨",
            "state": "completed",
            "username": "default"
        }
    ]

    return items
