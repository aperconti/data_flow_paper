import os
import requests
from chalice import Chalice
import sendgrid
import ast
from sendgrid.helpers.mail import Email, To, Content, Mail

app = Chalice(app_name='notifier')


def notify_on_create(student_email, event):
    try:
        sg = sendgrid.SendGridAPIClient(
            api_key=os.environ.get("SENDGRID_API_KEY"))
        from_email = Email(os.environ.get("SENDER_EMAIL"))
        to_email = To(student_email)
        subject = "We've received your paper!"
        content = Content(
            "text/plain", "Congrats on submitting your paper! We wanted to know that we've alerted all tutors and should have you matched with one shortly!")
        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        app.log.debug(
            f'Success sending message to sendgrid: {event.subject}, message: {event.message} response: {response}')
    except Exception as e:
        app.log.error(
            f'Error sending message to sendgrid: {event.subject}, message: {event.message} error: {e} type: {type(event.message)}')


def notify_student_on_assignement(teacher_email, event):
    try:
        sg = sendgrid.SendGridAPIClient(
            api_key=os.environ.get("SENDGRID_API_KEY"))
        from_email = Email(os.environ.get("SENDER_EMAIL"))
        to_email = To(teacher_email)
        subject = "Your paper is being reviewed!"
        content = Content(
            "text/plain", "A tutor has been assigned to your paper!")
        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        app.log.debug(
            f'Success sending message to sendgrid: {event.subject}, message: {event.message} response: {response}')
    except Exception as e:
        app.log.error(
            f'Error sending message to sendgrid: {event.subject}, message: {event.message} error: {e} type: {type(event.message)}')


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
