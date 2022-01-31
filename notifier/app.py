import os
import requests
from chalice import Chalice
from mailjet_rest import Client
import ast

app = Chalice(app_name='notifier')


def notify_on_create(student_email, event):
    try:
        response = send_email(
            student_email,
            "We've received your paper!",
            "Congrats on submitting your paper! We wanted to know that we've alerted all tutors and should have you matched with one shortly!",
            "Congrats on submitting your paper! We wanted to know that we've alerted all tutors and should have you matched with one shortly!"
        )
        app.log.debug(
            f'Success sending message to mailjet: {response}')
    except Exception as e:
        app.log.error(
            f'Error sending message to mailjet: {event.subject}, message: {event.message} error: {e} type: {type(event.message)}')


def notify_student_on_assignement(teacher_email, event):
    try:
        response = send_email(
            teacher_email,
            "Your paper is being reviewed!",
            "A tutor has been assigned to your paper!",
            "A tutor has been assigned to your paper!"
        )
        app.log.debug(
            f'Success sending message to mailjet: {response}')
    except Exception as e:
        app.log.error(
            f'Error sending message to mailjet: {event.subject}, message: {event.message} error: {e} type: {type(event.message)}')


def send_email(to_email, subject, text, content):
    mailjet = Client(
        auth=(
            os.environ.get("MAILJET_API_KEY"),
            os.environ.get("MAILJET_API_SECRET")
        ),
        version='v3.1'
    )
    data = {
        'Messages': [
            {
                "From": {
                    "Email": os.environ.get("SENDER_EMAIL"),
                    "Name": "Autum Perconti"
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": ""
                    }
                ],
                "Subject": subject,
                "TextPart": text,
                "HTMLPart": content
            }
        ]
    }
    result = mailjet.send.create(data=data)
    app.log.debug(
        f'sending message to mailjet: {result}')
    return result


@app.on_sns_message(topic='notifier')
def index(event):
    message = ast.literal_eval(event.message)
    student_email = message.get('student_email')
    teacher_email = message.get('teacher_email')
    paper_status = message.get('paper_status')
    if paper_status == 'created':
        notify_on_create(student_email, event)
    elif paper_status == 'assigned':
        notify_student_on_assignement(teacher_email, event)
