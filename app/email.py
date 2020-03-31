from app import mail, app
import smtplib as smtp
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import quopri

def QuoHead(String):
    s = quopri.encodestring(String.encode('UTF-8'), 1, 0)
    return "=?utf-8?Q?" + s.decode('UTF-8') + "?="

def send_yandex(subject, email_body):
    password = app.config['MAIL_PASSWORD']
    
    msg = MIMEMultipart()
    msg['Subject'] = QuoHead(subject).replace('=\n', '')
    msg['From'] = app.config['MAIL_USERNAME']
    msg['To'] = app.config['MAIL_ADMIN']
    msg.attach(MIMEText(email_body.encode('utf-8'), 'plain', 'UTF-8'))

    server = smtp.SMTP_SSL('smtp.yandex.com')
    server.set_debuglevel(1)
    server.ehlo(msg['From'])
    server.login(msg['From'], password)
    server.auth_plain()
    server.sendmail(msg['From'], [msg['To']], msg.as_string())
    server.quit()
