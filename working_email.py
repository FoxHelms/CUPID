import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def sendMail(message):
	with open('doggo.gif', 'rb') as f:
		img_data = f.read()	

	msg = MIMEMultipart()
	msg['From'] = 'email@email.com'
	msg['To'] = 'email@email.com'
	msg['Subject'] = 'CUPID Found a Flight'
	msg.attach(MIMEText(message))
	image = MIMEImage(img_data,name=os.path.basename('doggo.gif'))
	msg.attach(image)

	mailserver = smtplib.SMTP('smtp.gmail.com',587)
	# identify ourselves to smtp gmail client
	mailserver.ehlo()
	# secure our email with tls encryption
	mailserver.starttls()
	# re-identify ourselves as an encrypted connection
	mailserver.ehlo()
	mailserver.login('email@email.com', 'passwordgoeshere')

	mailserver.sendmail('source@email.com','destination@email.com',msg.as_string())

	mailserver.quit()