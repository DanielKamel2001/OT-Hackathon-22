# WIT Webstore

Created for OT Hackathon 22

Ivan Bisol, Daniel Gohara Kamel, Emily Larionov, Jessica Leishman

## Technology we used
* Flask
* mongoDB
* DigitalOcean (hosting)
* HTML
* CSS
* Bootstrap 5.1

## Building the application
This webstore uses [mongoDB](https://www.mongodb.com/). Create a new mongoDB and AWS email and create a new file named `cfg.py`in the project root directory with the following:

```properties
CONNECTION_STRING = "mongodb://yourconnectionstring"
AWS_ID = "yourID"  
AWS_SECRET = "yourSecret"
```
Should you wish to run the application locally, simply execute the command ` python -m flask run ` from within the project folder and click on the IP address provided in the terminal.

## Accessing the application
The application can also be accessed at [http://ocean.emily.engineer](http://ocean.emily.engineer).
