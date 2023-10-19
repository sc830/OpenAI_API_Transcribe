import os
import openai
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from intro_to_flask import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, Flask
from flask_mail import Message, Mail
from .forms import ContactForm
from .askmeform import AskmeForm
from .drawmeform import DrawmeForm


#The mail_user_name and mail_app_password values are in the .env file
#Google requires an App Password as of May, 2022: 
#https://support.google.com/accounts/answer/6010255?hl=en&visit_id=637896899107643254-869975220&p=less-secure-apps&rd=1#zippy=%2Cuse-an-app-password

mail_user_name = os.getenv('GMAIL_USER_NAME')
mail_app_password = os.getenv('GMAIL_APP_PASSWORD')
openai.api_key = os.getenv('OPENAI_API_KEY')

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

@app.route('/about',defaults={'route_with_name': None})
@app.route('/about/<route_with_name>')
def about(route_with_name):
  # Set default about me message and team member names.
  about_me = 'I like CS3398 allot!!!!!!!'
  team_names = ["Mike", "Sally", "Tom"]
  cleaned_name = ''

  # if a name was included in route, check to see if it uses (only) English alphabet characters.
  # This uses escape to 'sanitize' the route_with_name to remove characters that might cause a 
  # 'script injection attack':
  # https://www.stackhawk.com/blog/command-injection-python/
  # https://security.openstack.org/guidelines/dg_cross-site-scripting-xss.html
  # https://cwe.mitre.org/data/definitions/95.html
  if route_with_name:
    is_english_aphabetic = re.match("[a-zA-Z]+", escape(route_with_name))
     # If an English alpabet name, get it.
     # We are not reporting an error if the route_with_name is not English alphabetic 
    if is_english_aphabetic:                       
      cleaned_name = is_english_aphabetic.group(0)
    
    if cleaned_name in team_names:                  
      return render_template('about.html', about_name=cleaned_name, about_aboutMe=about_me, team_names=team_names)
    else:
      cleaned_name = "Us"
  else:
    cleaned_name = "Us"
  return render_template('about.html', about_name=cleaned_name, about_aboutMe="We like CS3398 allot!!!!", team_names=team_names)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
  # Flask 2.2.2 requires a parameter to a form object: request.form or other
	# See https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
  form = ContactForm(request.form) 

  if request.method == 'POST':
      if form.validate() == False:
        return render_template('contact.html', form=form)
      else:
        msg = Message(form.subject.data, sender=mail_user_name, recipients=[form.email.data])
        msg.body = """From: %s <%s> \n%s \n%s
        """ % (form.name.data, form.email.data, form.subject.data, form.message.data)
        mail.send(msg)

        return render_template('contact.html', success=True)

  elif request.method == 'GET':
      return render_template('contact.html', form=form)
    
@app.route('/askme',methods=['GET', 'POST'])
def askme():
  form = AskmeForm(request.form)
  
  if request.method == 'POST':
      if form.validate() == False:
        return render_template('askme.html', form=form)
      else:
        response = openai.Completion.create(
          engine="gpt-3.5-turbo-instruct",  # or another engine ID
          prompt=form.prompt.data,
          max_tokens=150
        )
        display_text = response.choices[0].text.strip()
        return render_template('askme.html', ask_me_prompt=form.prompt.data,ask_me_response=display_text,success=True)
      
  elif request.method == 'GET':
      return render_template('askme.html', form=form)
    
@app.route('/drawme',methods=['GET', 'POST'])
def drawme():
  form = DrawmeForm(request.form)
  
  if request.method == 'POST':
      if form.validate() == False:
        return render_template('drawme.html', form=form)
      else:
        # prompt=form.prompt.data,
        response = openai.Image.create(
          prompt="a white siamese cat",
          n=1,
          size="1024x1024"
        )
        display_image_url = response['data'][0]['url']
        return render_template('drawme.html', draw_me_prompt=form.prompt.data,draw_me_response=display_image_url,success=True)
      
  elif request.method == 'GET':
      return render_template('drawme.html', form=form)
    

  
  
