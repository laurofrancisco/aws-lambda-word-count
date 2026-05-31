import json
import boto3
import urllib.parse

s3 = boto3.client('s3')
sns = boto3.client('sns')

SNS_TOPIC_ARN = "YOUR_SNS_TOPIC_ARN"

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')

    word_count = len(content.split())

    message = f"The word count in the {key} file is {word_count}."

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject="Word Count Result"
    )

    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }