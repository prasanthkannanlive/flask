from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_cors import CORS

from email.message import EmailMessage
import ssl
import smtplib


app = Flask(__name__)
CORS(app)

emailPass = "oenvpuqwfdoqlrda"
email = "notificationemailtrigger@gmail.com"
emailReceiver = "notificationemailtrigger@gmail.com"
subject="New Notification"



@app.route('/streams', methods=["POST"])
def streams():

    if (request.json['confirmed']):
        return jsonify(success=True)


    details = request.json["txs"]

    for donation in details:

        amount = int(donation['value'])/1000000000000000000
        em = EmailMessage()
        em['From'] = email
        em['To'] = emailReceiver
        em['Subject'] = subject

        em.set_content(donation['fromAddress'] + " has just sent you " + str(amount) + " in ETH!")

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email, emailPass)
            smtp.sendmail(email, emailReceiver, em.as_string())
    
    print("Email Sent")

    return jsonify(success=True)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()