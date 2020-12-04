# serverless-todo API

(このドキュメントは現在作成中です🐈)

serverless-todo API は Todo を登録、取得(検索)、更新、削除することができるシンプルな REST API です。

この API は AWS Lambda と Amazon DynamoDB を基盤としたサーバーレスアーキテクチャで設計しました。

>このドキュメントでは AWS の各名称について Amazon, AWS などのプリフィックスを省略し、`Amazon Cognito` → `Cognito`、`AWS CloudFormation` → `CloudFormation` のように表現することがありますので予めご留意ください。

### References
API の仕様についてはこちらを参照してください

[serverless-todo API: Reference](https://serverlesstodo.docs.apiary.io/)

[serverless-todo API: Cognito UserPool Auth Reference](https://cognitouserpoolauth.docs.apiary.io/)


デプロイ手順はこちらを参照してください

[serverless-todo API: Deploy](https://hackmd.io/@craymaru/BJ3Wixq9P)


---
# 使用技術

## ローカル環境

| Name          | Version                | Note                    |
| ------------- | ---------------------- | ----------------------- |
| macOS Big Sur | 11.2 Beta（20C5048l）  |                         |
| Xcode         | 12.2 beta 3 (12B5035g) |                         |
| pyenv         | 3.8.6                  |                         |
| pip           | 20.3.1                 |                         |
| pipenv        | 2020.11.15             | 仮想環境/パッケージ管理 |



## API 開発

### アプリケーション

| Name    | Version | Note |
| ------- | ------- | ---- |
| Python  | 3.8.6   |      |
| chalice | 1.21.4  | API Gateway と Lambda の管理、デプロイ |
| boto3   | 1.16.25 | AWS SDK for Python     |
 
 > 依存ライブラリは省略。詳細は /Pipfile.lock から確認可能。


### ユニットテスト

| Name           | Version | Note                                         |
| -------------- | ------- | -------------------------------------------- |
| pytest         | 6.1.2   | Python のテストフレームワーク                |
| pytest-chalice | 0.0.5   | インターフェイスの公開、応答のモック         |
| moto           | 1.3.16  | AWS サービスをモック DynamoDB のテストに使用 |


## アーキテクチャ

### サーバレスアプリケーション
![](https://i.imgur.com/ltn85q8.jpg)
* Amazon API Gateway
* AWS Lambda
* Amazon DynamoDB

### 認証
![](https://i.imgur.com/XVBXFJT.jpg)

* Amazon Cognito
* AWS CloudFormation

### CI/CD パイプライン
![](https://i.imgur.com/wGxQgHU.jpg)

* AWS CloudFormation
* AWS CodePipeline
* AWS CodeBuild
* AWS CodeCommit
* Amazon S3

### その他
* Amazon CloudWatch
* AWS IAM


# アプリの設計

---
<br>

# テストの設計



今回はユニットテストのみ実施しています。
`app.py` のテストでは `current_response.json_body` を差し替える必要があったため、pytest-chalice を使用しています。

`chalicelib/db.py` のテストではAWS サービスをモックすることのできるライブラリ moto を使用し、DynamoDB をモックしています。

## テストの実施
テストは `./tests` に格納されています。
以下のコマンドにて、すべてのテストを詳細表示で実行できます。
```
pytest -vvs --durations=10
```
## テストデータ
共通で使用するテストデータは `tests/testdata` に格納されています。
個別のテストケースへの関連が強いテストデータは、`@pytest.mark.parametrize` デコレータ、またはテストケース内に内包しています。

## テストケース

現在実装されている、テストケースは以下の通りです。(2020-12-04 15:28)

|テスト対象のメソッド|
|-|
|テストケース|

### app のテスト
path: `tests/test_app.py` ▶ `app.py`

|`get_index`|
|-|
|ステータスコード `200` と `JSON` を返すことができる|

|`get_app_db`|
|-|
|`get_app_db` の返り値クラスと、元のクラスが一致する|

|`get_todos`|
|-|
|すべてのアイテムを取得することができる|

|`add_new_todo`|
|-|
|`subject` と `description` があるケース、`uid` を受け取ることができる|
|`subject` のみのケース、`uid` を受け取ることができる|
|`subject` がないケース、例外を発生させることができる|
|`description` のみのケース、例外を発生させることができる|
|`json_body` が `None` のケース、例外を発生させることができる|

|`get_todo`|
|-|
|取得に指定した `uid`、`username` の Todo を受け取ることができる|

|`delete_todo`|
|-|
|削除に指定した `uid`、`username` の Todo の `uid` を受け取ることができる|

|`update_todo`|
|-|
|すべての属性のケース、特定の Todo の `uid` を受け取ることができる|
|`subject` のみのケース、特定の Todo の `uid` を受け取ることができる|
|`discription` のみのケース、特定の Todo の `uid` を受け取ることができる|
|`state` のみのケース、特定の Todoの `uid` を受け取ることができる|
|`json_body` が None のケース、例外を発生させることができる|

### `DynamoDBTodo` クラスのテスト
path: `tests/test_db.py` ▶ `chalicelib/db.py`

|`DynamoDBTodo.list_all_items`|
|-|
|すべてのアイテムを取得することができる|

|`DynamoDBTodo.list_items`|
|-|
|ユーザー `default` のアイテムをすべて取得することができる|
|ユーザー `default` のアイテムからクエリを満たすものをすべて取得することができる|

|`DynamoDBTodo.add_item`|
|-|
|`subject` と `description` があるケース、正常にクエリを投げ `uid` を受け取ることができる|
|`description` のみのケース、例外を発生させることができる|

|`DynamoDBTodo.get_item`|
|-|
|`uid` が存在するケース、item を正常に返すことができる|
|`uid` が存在しないケース、例外を発生させることができる|

|`DynamoDBTodo.delete_item`|
|-|
|`uid` が存在するケース、削除した item の `uid` を正常に返すことができる|
|`uid` が存在しないケース、例外を発生させることができる|

|`DynamoDBTodo.update_item`|
|-|
|すべての属性を更新するケース、更新した item の `uid` を正常に返すことができる|
|`subject` を更新するケース、更新した item の `uid` を正常に返すことができる|
|`description` を更新するケース、更新した item の `uid` を正常に返すことができる|
|`state` を更新するケース、更新した item の `uid` を正常に返すことができる|
|`uid` が存在しないケース、例外を発生させることができる|

### バリデーションのテスト
path: `tests/test_validates.py` ▶ `chalicelib/validates.py`

|`Validates.subject`|
|-|
|通常のケース、例外をパスできる|
|`None` のケース、例外を発生させることができる|
|`str` 以外の型のケース、例外を発生させることができる|
|文字の長さが境界値の限界のケース、例外をパスできる|
|文字の長さが境界値を超過しているケース、例外を発生させることができる|

|`Validates.description`|
|-|
|通常のケース、例外をパスできる|
|`None` のケース、例外をパスできる|
|`str` 以外の型のケース、例外を発生させることができる|
|文字の長さが境界値の限界のケース、例外をパスできる|
|文字の長さが境界値を超過しているケース、例外を発生させることができる|

|`Validates.state`|
|-|
|通常のケース、例外をパスできる|
|`None` のケース、例外を発生させることができる|
|`str` 以外の型のケース、例外を発生させることができる|
|`Validates.STATE_ENUM` に含まれる場合、例外をパスできる|
|`Validates.STATE_ENUM` に含まれない場合、例外を発生させることができる|

|`Validates.username`|
|-|
|通常のケース、例外をパスできる|
|`None` のケース、例外を発生させることができる|
|`str` 以外の型のケース、例外を発生させることができる|
|文字の長さが境界値の限界のケース、例外をパスできる|
|文字の長さが境界値を超過しているケース、例外を発生させることができる|
