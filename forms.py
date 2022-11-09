#Need to do the following installs:
# pip install flask-wtf
# pip install email_validator
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, validators, ValidationError

class ContactForm(Form):
    name = StringField("Name",  [validators.InputRequired()])
    email = StringField("Email",  [validators.InputRequired(), validators.Email()])
    subject = StringField("Subject",  [validators.InputRequired()])
    message = TextAreaField("Message",  [validators.InputRequired()])
    submit = SubmitField("Send")
