import os
import boto3
from chalice import Chalice
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


@app.route('/paper', methods=['POST'])
def paper():
    body = ast.literal_eval(app.current_request.raw_body.decode())
    table = get_paper_db()
    response = table.put_item(
        Item=body
    )
    put_response = get_notifier_topic().publish(
        TargetArn=os.environ["NOTIFIER_ARN"],
        Message=json.dumps({'default': json.dumps(body)}),
        MessageStructure='json'
    )
    print(put_response)
    return response


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
