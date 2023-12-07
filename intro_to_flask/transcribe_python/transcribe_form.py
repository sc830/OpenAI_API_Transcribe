import sys 
sys.dont_write_bytecode = True
#Need to do the following installs:
# pip install flask-wtf
# pip install email_validator
from flask_wtf import Form
from wtforms import FileField, SubmitField, validators, ValidationError
from wtforms.validators import InputRequired

class TranscribemeForm(Form):
    audio_file = FileField("Your Audio File", validators=[InputRequired("Please upload an audio file.")])
    submit = SubmitField("Send")