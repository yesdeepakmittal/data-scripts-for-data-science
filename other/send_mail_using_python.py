'''
Requires -> takes Gmail Id and Password
Sends a an email from Gmail account

Steps to follow:
1. Go to https://myaccount.google.com/u/1/security
2. ON "Less secure app access" option
3. Off the above option once you done with your task(s)

Reference - https://github.com/amrrs/build_tools_to_automate_python/blob/master/hn_news_scraper_no_cred.py
'''

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SERVER = 'smtp.gmail.com'
PORT = 587
FROM =  'sender email'
TO = 'list of receivers email'
PASS = '***Password***'

msg = MIMEMultipart()
msg['Subject'] = "Happy Birthday"
msg['From'] = FROM
msg['To'] = TO

content = """<b>Happy Birthday to you my dear brother</b><br>
             Please take care of yourself and your family.<br>
             We love you a lot.<br>"""

msg.attach(MIMEText(content, 'html'))
server = smtplib.SMTP(SERVER, PORT)

server.set_debuglevel(1)
server.ehlo()
server.starttls()
#server.ehlo
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent✅')

server.quit()