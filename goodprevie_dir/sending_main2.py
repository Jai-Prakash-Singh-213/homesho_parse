#! /usr/bin/python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os
from email.Utils import COMMASPACE, formatdate



MAIL_SERVER = 'smtp.gmail.com'
SENDER_EMAIL = 'jaiprakashsingh213@gmail.com'
SENDER_USER = 'jaiprakashsingh213@gmail.com'
SENDER_PASSWORD = '6Tresxcvbhy6'

def send_mail(to_email, subject, text, file_path_list):
	msg = MIMEMultipart()
	
	msg['From'] = SENDER_EMAIL
	#msg['To'] = to_email
        msg["To"] = COMMASPACE.join(to_email)
	msg['Subject'] = subject
	
	msg.attach(MIMEText(text))
	
	for f in file_path_list:
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(open(f, 'rb').read())
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"'\
											% os.path.basename(f))
		msg.attach(part)
	
	#mail_server = smtplib.SMTP(MAIL_SERVER)
        #mail_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        mail_server = smtplib.SMTP('smtp.gmail.com:587')
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()

        #mail_server = smtplib.SMTP_SSL("smtp.gmail.com")
	mail_server.login(SENDER_USER, SENDER_PASSWORD)
	mail_server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
	mail_server.close()


def supermain(file_path_list):
    to_email = ["santosh.kumar@wisepromo.com", "ajaykochhar79@gmail.com"]
    #to_email = ["jaiprakash@wisepromo.com", "kayakashyap213@gmail.com"]

    subject = 'Send email with attachment'
    text = 'This is an email with attachment'
    #file_path_list = ["clicktohit30032014.csv"]

    send_mail(to_email, subject, text, file_path_list)


if __name__ == "__main__":
    #to_email = "santosh.kumar@wisepromo.com"

    file_path_list = ["clicktohit29032014.csv",   "clicktohit31032014.csv", 
                      "clicktohit30032014.csv", "goodpreview29032014.csv", 
                      "goodpreview31032014.csv"]

    supermain(file_path_list)
