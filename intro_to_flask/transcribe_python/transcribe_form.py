import sys 
sys.dont_write_bytecode = True
#Need to do the following installs:
# pip install flask-wtf
# pip install email_validator
from flask_wtf import Form
from wtforms import TextAreaField, SubmitField, validators, ValidationError

class TranscribemeForm(Form):
    prompt = TextAreaField("What would you like to transcribe?",  [validators.InputRequired("Please enter the absolute path to your audio file.")])
    submit = SubmitField("Send") 