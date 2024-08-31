import smtplib
from email.mime.text import MIMEText
myEmail = 'projectzx619@gmail.com'
toEmail = 'kabilkabilan02@gmail.com'

smtp_server = 'smtp.gmail.com'
smtp_port = 587

msg = MIMEText('Dai ethachum work panra')
msg['Subject'] = 'The subject of the email'
msg['From'] = myEmail
msg['To'] = toEmail

server = smtplib.SMTP(smtp_server,smtp_port)
server.starttls()
server.login(myEmail,'hmkbinifahsvpcuq')

server.send_message(msg)
server.quit()