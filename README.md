## Overview: 
This is a basic implementation of a data flow for a theoretical product where students submit papers for writing feedback. Once a Student submits a paper to receive edits, the information will be retrieved via a lambda and will then be recorded in the database. The submission will them be published to an SNS topic that will alert subscribers (tudors, teach, student) that the paper has been submitted. The record of the alerts will be recorded in the database as well under a table titled **alerts**. Once the tutor picks up the paper to begin reviewing it the action will be published to SNS which alerts the student that the review is in process.  Data of this action will be recorded in the **events** and **alerts** table. 

## Assumptions: 
 
* There would eventually be a website or client that would connect into this API
* A POST to the endpoint implies the creation or submission of a "paper"
* A PATCH where a tutor is not associated to a given project, is updated to having a teacher associated, implies that a tutor has been assigned to the students paper. 
* A PATCH to the API that does not qualify as a behavior above, implies, either the student has made edits to the paper, or the tutor has commented or returned the paper for reevaluation
* Finally, a PATCH to the API where a grade or score is associated with the paper, implies that the paper has been returned to the student and the exchange is complete.  



## Environment requirements:

#### Installation and Setup

## Areas to improve:
* Change DB from a non-relational DB to a relational DB. The data in this project would be more highly utilized if relationships were drawn.
 
* The flow is very fragmented currently which could make trouble shooting difficult. Orchestration tools such as Apache Airflow, or Dagster would allow for increased visibility in trouble shooting.
