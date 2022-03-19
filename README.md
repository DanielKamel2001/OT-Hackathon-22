# WIT Webstore

Created for OT Hackathon 22

## Technology we used
* Flask
* mongoDB
* DigitalOcean
* HTML
* CSS
* Bootstrap 5.1

## Challenges we experienced
A major challenge we encountered during the development of our webstore was getting all team members to the same level of familiarity with mongoDB and Flask.

## What's next for the webstore
Future steps for our implementation of the webstore would be to store customer orders within our database and track those orders.

## Building the app
This webstore uses [mongoDB](https://www.mongodb.com/). Create a new mongoDB and AWS email and create a new file named `cfg.py`in the project root directory with the following:

```properties
CONNECTION_STRING = "mongodb://yourconnectionstring"
AWS_ID = "yourID"  
AWS_SECRET = "yourSecret"
```

