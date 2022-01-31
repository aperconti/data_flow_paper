# Paper Data Pipeline

![Basic Architectural Diagram](/docs/paper.png)

## Overview:
This is a basic data flow implementation for a theoretical product where students submit papers for writing feedback. Once a student submits a paper to receive edits, the information will be retrieved via a lambda and will then be recorded in the database. The submission will then be published to an SNS topic that will alert subscribers (tudors, teach, student) that the paper has been submitted.

## Assumptions:

* There would eventually be a website or client that would connect into this API
* A POST to the endpoint implies the creation or submission of a "paper"
* A PATCH is an indication for the status of the paper to be assigned to a particular tutor or teacher

Upon both a POST and PATCH, the creator's email with be notified through this minimalist pub/sub data pipeline created in AWS.

## Environment requirements:

#### Installation and Setup

For the most part, sendgrid, boto, and chalice are the frameworks that are used.

```bash
pip install -r requirements.txt

-- NOTE: the directories paper & notifier are AWS chalice apps. The majority of the chalice configuration files are in the .gitignore. For further information, please visit https://github.com/aws/chalice
```

## Tooling

| Tool      | Description |
| ----------- | ----------- |
|AWS chalice    |    due to time constrants I choose this tool. AWS chalice is an open source project mantained by AWS that makes it easy to create data driven acritecture compondents.  |
|AWS lambda    |    cheapest and easiest way to run python scripts in the cloud. AWS Lambdas let you run code for virtually any type of application or backend service without provisioning or managing servers. |
|AWS dynamo DB    |    cost effective, easy to set up database designed to run high-performance applications at any scale.  |
|PostMan    |    For easy interaction with the API. Postman is an API platform for building and using APIs. Postman simplifies each step of the API lifecycle and streamlines collaboration so you can create better APIs—faster. |
|AWS SNS (PubSub)    |    Its in the AWS eco system, its straightforward and worked well with the other tools I was using.  |
|Python    |    Best tool for the job
|sendGrid    |    for senting transactional emails. SendGrid is a cloud-based SMTP (Simple Mail Transfer Protocol) provider that allows you to send email without having to maintain email servers. |
|AWS API gateway    |    Its in the AWS eco system, cost efficent and makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale. |
|AWS CloudWatch    |    Its in the AWS eco system, CloudWatch makes it easy to detect anomalous behavior in your environments, visualize logs and metrics, troubleshoot issues, and discover insights to keep your applications running smoothly.

## Areas to improve:
* Change DB from a non-relational DB to a relational DB. The data in this project would be more highly utilized if relationships were drawn.

* The flow is very fragmented currently, which could make troubleshooting difficult. Orchestration tools such as Apache Airflow, or Dagster would allow increased visibility in troubleshooting.
