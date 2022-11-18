#!/usr/bin/env python -B
import sys 
sys.dont_write_bytecode = True
#These two imports were updated from original which were deprecated by Flask
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField

class ContactForm(Form):
    name = StringField("Name")
    email = StringField("Email")
    subject = StringField("Subject")
    message = TextAreaField("Message")
    submit = SubmitField("Send")
