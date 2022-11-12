from flask import Flask, flash, render_template, request
#Need to do the following install for mail to work:
#pip install Flask-Mail
from flask_mail import Mail, Message
#forms is our local forms.py
from forms import ContactForm
import os

app = Flask(__name__)

app.config['SECRET_KEY']='LongAndRandomSecretKey'
mail_user_name = os.getenv('GMAIL_USER_NAME')
mail_app_password = os.getenv('GMAIL_APP_PASSWORD')

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = mail_user_name
app.config['MAIL_PASSWORD'] = mail_app_password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

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
        msg = Message(form.subject.data, sender=mail_user_name, recipients=['t_l81@txstate.edu'])
        msg.body = """
        From: %s <%s>
        %s %s
        """ % (form.name.data, form.email.data, form.subject.data, form.message.data)
        mail.send(msg)
        return 'Form posted.'
    elif request.method == 'GET':
      return render_template('contact.html', form=form)
  
if __name__ == '__main__':
  app.run(debug=True)
