import os
import openai
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from intro_to_flask import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, Flask, Blueprint
from .transcribe_form import TranscribemeForm

transcribe_blueprint = Blueprint('transcribeme', __name__)

@transcribe_blueprint.route('/transcribeme',methods=['GET', 'POST'])
@app.route('/transcribeme',methods=['GET', 'POST'])
def transcribeme():
  form = TranscribemeForm(request.form)
  
  if request.method == 'POST':
      if form.validate() == False:
        return render_template('transcribeme.html', form=form)
      else:
        # The following response code is an (older) from example on: 
        # https://platform.openai.com/docs/guides/speech-to-text
        audio_file= open(form.prompt.data, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return render_template('transcribeme.html', audio_file=form.prompt.data, transcription=transcription['text'], success=True)
      
  elif request.method == 'GET':
      return render_template('transcribeme.html', form=form)