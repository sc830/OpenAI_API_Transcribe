import os
import openai
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from intro_to_flask import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, Flask, Blueprint
from .ask_form import AskmeForm

ask_blueprint = Blueprint('askme', __name__)

@ask_blueprint.route('/askme',methods=['GET', 'POST'])
@app.route('/askme',methods=['GET', 'POST'])
def askme():
  form = AskmeForm(request.form)
  
  if request.method == 'POST':
      if form.validate() == False:
        return render_template('askme.html', form=form)
      else:
        # The following response code adapted from example on: 
        # https://platform.openai.com/docs/quickstart?context=python
        response = openai.Completion.create(
          engine="gpt-3.5-turbo-instruct",  # or another engine ID
          prompt=form.prompt.data,
          max_tokens=150
        )
        display_text = response.choices[0].text.strip()
        return render_template('askme.html', ask_me_prompt=form.prompt.data,ask_me_response=display_text,success=True)
      
  elif request.method == 'GET':
      return render_template('askme.html', form=form)