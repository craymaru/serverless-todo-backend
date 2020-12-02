import os
import uuid
import json
import argparse

import boto3


TABLE = {
        'prefix': 'serverless-todo-backend',
        'env_var': 'APP_TABLE_NAME',
        'hash_key': 'username',
        'range_key': 'uid'
}


def create_table(table_name_prefix, hash_key, range_key=None):
    client = boto3.client('dynamodb')
    table_name = '%s-%s' % (table_name_prefix, str(uuid.uuid4()))
    key_schema = [
        {
            'AttributeName': hash_key,
            'KeyType': 'HASH',
        }
    ]
    attribute_definitions = [
        {
            'AttributeName': hash_key,
            'AttributeType': 'S',
        }
    ]
    provisioned_throughput = {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        }
    if range_key is not None:
        key_schema.append({'AttributeName': range_key, 'KeyType': 'RANGE'})
        attribute_definitions.append(
            {'AttributeName': range_key, 'AttributeType': 'S'})
    client.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput=provisioned_throughput
    )
    waiter = client.get_waiter('table_exists')
    waiter.wait(TableName=table_name, WaiterConfig={'Delay': 1})
    return table_name


def record_as_env_var(key, value, stage):
    with open(os.path.join('.chalice', 'config.json')) as f:
        data = json.load(f)
        data['stages'].setdefault(stage, {}).setdefault(
            'environment_variables', {}
        )[key] = value
    with open(os.path.join('.chalice', 'config.json'), 'w') as f:
        serialized = json.dumps(data, indent=2, separators=(',', ': '))
        f.write(serialized + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--stage', default='dev')
    args = parser.parse_args()
    table_config = TABLE
    table_name = create_table(
        table_config['prefix'],
        table_config['hash_key'],
        table_config.get('range_key')
    )
    record_as_env_var(table_config['env_var'], table_name, args.stage)


if __name__ == '__main__':
    main()
