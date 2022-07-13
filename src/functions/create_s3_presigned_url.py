import boto3, os, json
from src.lib.wrapper import functionWrapper
from botocore.config import Config


KMEANED_IMAGE_BUCKET = os.getenv("KMEANED_IMAGE_BUCKET", "")
USER_TABLE = os.getenv('USER_TABLE', '')

# DynamoDBに新しく要素を追加
def put_item(
        item: dict,
        table_name: str
) -> None:
    dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
    table = dynamodb.Table(table_name)
    res = table.put_item(Item=item)


# S3のPresigned URLを発行する
def generate_upload_url(
    key: str,
    bucket_name: str,
    ExpiresIn=3600
) -> str:
    s3 = boto3.client(
        service_name='s3',
        config=Config(signature_version='s3v4'),
    )
    url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': bucket_name,
            'Key': key
        },
        ExpiresIn=ExpiresIn,
        HttpMethod='PUT')

    return url


@functionWrapper
def main(event, context):
    print(event)
    body_str = event["body"]
    print(body_str)

    body_dict = json.loads(body_str)
    print(body_dict["sessionID"])
    url = generate_upload_url(body_dict["sessionID"], KMEANED_IMAGE_BUCKET)
    print(url)

    db_row = {"id":body_dict["sessionID"], "upload_url":url}
    put_item(db_row, USER_TABLE)
    
    body = {"url" : url}
    response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "x-custom-header": "my custom header value"
        },
        "body": body
    }
    return response
