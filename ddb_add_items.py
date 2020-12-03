from tests.mock.dynamo_db import MockDynamoDB as DynamoDB
from tests.testdata.ddb_items import TESTDATA_DDB_ITEMS


def main():
    ddb = DynamoDB()
    ddb.set_table('serverless-todo-backend-0a4ca86a-8983-46fe-af1a-96a5a1e5bb12')
    ddb.table.put_items(TESTDATA_DDB_ITEMS)


if __name__ == '__main__':
    main()
