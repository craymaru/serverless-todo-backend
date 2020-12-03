# serverless-todo API

(このドキュメントは現在作成中です🐈)

serverless-todo API は Todo を登録、取得(検索)、更新、削除 することができるシンプルな REST API です。

この API は AWS Lambda と Amazon DynamoDB を基盤としたサーバーレスアーキテクチャで設計しました。

>このドキュメントでは AWS の各名称について Amazon, AWS などのプリフィックスを省略し、`Amazon Cognito` → `Cognito`、`AWS CloudFormation` → `CloudFormation` のように表現することがありますので予めご留意ください。

### References
API の仕様についてはこちらを参照してください
[serverless-todo API: Reference](https://serverlesstodo.docs.apiary.io/)
[serverless-todo API: Cognito UserPool Auth Reference](https://cognitouserpoolauth.docs.apiary.io/)

デプロイ手順はこちらを参照してください
[serverless-todo API: Deploy](https://hackmd.io/@craymaru/BJ3Wixq9P)

---
# 構成

## ローカル環境

* pyenv
* pipenv

## API 開発

### アプリケーション
* chalice
* boto3


### ユニットテスト
* pytest
* pytest-chalice
* moto


## アーキテクチャ

### サーバレス
* Amazon API Gateway
* AWS Lambda
* Amazon DynamoDB

### 認証
* Amazon Cognito
* AWS CloudFormation

### CI/CD
* AWS CloudFormation
* AWS CodeBuild
* AWS CodePipeline
* Amazon S3

### その他
* Amazon CloudWatch
* AWS IAM


# テストケース