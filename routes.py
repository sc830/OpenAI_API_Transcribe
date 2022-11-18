#!/usr/bin/env python -B
import sys 
sys.dont_write_bytecode = True
from flask import Flask, render_template, request, flash
from forms import ContactForm

app = Flask(__name__)
app.config['SECRET_KEY']='LongAndRandomSecretKey'
# app.secret_key = 'development key'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  # Flask 2.2.2 requires a parameter to a form object: request.form or other
  # See https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
  form = ContactForm(request.form)
  
  if request.method == 'POST':
    if form.validate() == False:
      # This will print out any errors the form has to the user.  Used for debugging.
      flash(form.errors)
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      return 'Form posted.'
  
    elif request.method == 'GET':
        return render_template('contact.html', form=form)
  
if __name__ == '__main__':
    app.run(debug=True)
