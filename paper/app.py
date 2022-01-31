import os
import boto3
from chalice import Chalice, Response
import ast
import json

app = Chalice(app_name='paper')
_PAPER_DB = None

_NOTIFIER_TOPIC = None


def get_notifier_topic():
    global _NOTIFIER_TOPIC
    if _NOTIFIER_TOPIC is None:
        _NOTIFIER_TOPIC = boto3.client('sns')
    return _NOTIFIER_TOPIC


def get_paper_db():
    global _PAPER_DB
    if _PAPER_DB is None:
        _PAPER_DB = boto3.resource('dynamodb').Table(
            os.environ['PAPER_TABLE_NAME'])
    return _PAPER_DB


def publish_to_sns(body):
    response = get_notifier_topic().publish(
        TargetArn=os.environ["NOTIFIER_ARN"],
        Message=json.dumps({'default': json.dumps(body)}),
        MessageStructure='json'
    )
    app.log.debug(f'publishing to SNS topic: {body} response: {response}')


@app.route('/paper', methods=['POST'])
def create_paper():
    body = ast.literal_eval(app.current_request.raw_body.decode())
    body['paper_status'] = 'created'
    table = get_paper_db()
    response = table.put_item(
        Item=body
    )
    publish_to_sns(body)
    return response


@app.route('/paper', methods=['PATCH'])
def update_paper():
    body = ast.literal_eval(app.current_request.raw_body.decode())
    table = get_paper_db()
    body['paper_status'] = 'assigned'
    try:
        response = table.update_item(
            Key={
                'id': body.get('id')
            },
            UpdateExpression="set teacher_email=:r, paper_status=:p",
            ExpressionAttributeValues={
                ':r': body.get('teacher_email'),
                ':p': body.get('paper_status')
            },
            ReturnValues="UPDATED_NEW"
        )
    except Exception as e:
        app.log.error(
            f'Error updating: {body.get("id")} body: {body} error: {e} key: {body.get("id")}')
        return Response(body='Oh no! We weren\'t able to update your paper!',
                        status_code=500,
                        headers={'Content-Type': 'text/plain'})
    publish_to_sns(body)
    return response
