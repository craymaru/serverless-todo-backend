from tests.mock.dynamo_db import MockDynamoDB as DynamoDB
from tests.testdata.ddb_items import TESTDATA_DDB_ITEMS
from tests.mock.ddb_schema import MOCK_DDB_SCHEMA

ddb = DynamoDB()
ddb.set_table('serverless-todo-backend-f71fb8af-5dc0-4c8f-bdaf-e7e2d7124b7f')
ddb.table.put_items(TESTDATA_DDB_ITEMS)