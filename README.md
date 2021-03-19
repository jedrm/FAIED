# FAiED

It is a computer vision program that is made in Python dealing with recommending songs based on current user emotion.

## Description

It uses computer vision to do two things: to recognize and identify the user in front of the camera and to identify and detect the user's emotions. The information is sent to the program and pulls up songs the user usually listens to when they are feeling a certain emotion. If the user is not known, the program will pull up songs that known users usually listen to when they feel the same emotion.
Check out the [demo](https://youtu.be/q1TP3IaOYyg) and [presentation](https://www.youtube.com/watch?v=61_mN5Mh6GE)!

![Example](https://user-images.githubusercontent.com/45746064/111519609-a7988200-872d-11eb-957e-88ec18adb931.png)

## Setup

Use the packge manager [pip](https://pip.pypa.io/en/stable/) to install `virtualenv` and `requirements.txt` to install the following dependencies.

```pip install virtualenv
virtualenv faied
source faied/bin/activate
pip install -r requirements.txt
```

## Usage

Run the following code on the console to run the program.

`flask run --host=localhost`

The command runs the Flask app locally and you can try out the computer vision program.

## Members

Mentor:
- [Purvesh Sharma](https://www.linkedin.com/in/sharmapurvesh/)

Members:
- [Jed Rendo Magracia](https://www.linkedin.com/in/jedrendomagracia/)
- [Neelima Jyothiraj](https://www.linkedin.com/in/neelima-jyothiraj/)
- [Alexa Urrea](https://www.linkedin.com/in/alexa-urrea-45b0961b8/)
