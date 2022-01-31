import os
import requests
from chalice import Chalice
import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail

app = Chalice(app_name='notifier')


@app.on_sns_message(topic='notifier')
def index(event):
    app.log.error("Received message with subject: %s, message: %s",
                  event.subject, event.message)
    sg = sendgrid.SendGridAPIClient(api_key="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")
    from_email = Email("test@example.com")
    to_email = To("autumlucille@gmail.com")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
