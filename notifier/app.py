import os
import requests
from chalice import Chalice
import sendgrid
import ast
from sendgrid.helpers.mail import Email, To, Content, Mail

app = Chalice(app_name='notifier')


@app.on_sns_message(topic='notifier')
def index(event):
    try:
        message = ast.literal_eval(event.message)
        student_email = message.get('student_email')
        sg = sendgrid.SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"])
        from_email = Email("autumlucille@gmail.com")
        to_email = To(student_email)
        subject = "We've received your paper!"
        content = Content(
            "text/plain", "Congrats on submitting your paper! We wanted to know that we've alerted all tutors and should have you matched with one shortly!")
        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        app.log.debug("Error sending message to sendgrid: %s, message: %s response: %s",
                      event.subject, event.message, response)
    except Exception as e:
        app.log.error("Error sending message to sendgrid: %s, message: %s error: %s type: %s",
                      event.subject, event.message, e, type(event.message))
