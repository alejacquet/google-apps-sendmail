#!/usr/bin/python

import smtplib
import argparse
from email.MIMEText import MIMEText
from email import Utils
from time import strftime


def main():
	parser = argparse.ArgumentParser(description='SendMail Python v.02')
	parser.add_argument('--sender',help='Select the Sender', required=False)
	parser.add_argument('--to',help='Select the Recipient', required=True)
	#parser.add_argument('--replyTo',help='Reply-To Recipient ', required=False)
	parser.add_argument('--server',help='Host Server', required=True)
	parser.add_argument('--port',help='Server Port', required=True)
	parser.add_argument('--ssl',help='SSL ON/OFF', required=False)
	parser.add_argument('--auth',help='Authentication username:password', required=False)
	args = parser.parse_args()
	
	if args.sender:
		fromaddr = args.sender
	else:
		fromaddr = 'no-reply@domain.com'
	subject = "SendMail Test " + strftime("%Y-%m-%d %H:%M:%S")
	content = "Hello World! \n This is an automated test.\n\n" + strftime("%Y-%m-%d %H:%M:%S")

	msg = MIMEText(content)
	msg['From'] = fromaddr
	msg['To'] = args.to
	msg['Subject'] = subject 	
	msg['Message-ID'] = Utils.make_msgid()
# 	msg.add_header('Reply-To', args.replyTo) NOT WORKING

	try:	
		if args.ssl == 'on':
			server = smtplib.SMTP_SSL(args.server, args.port)
			server.set_debuglevel(True)
			server.ehlo()
		else:
			server = smtplib.SMTP(args.server, args.port)
			server.set_debuglevel(True)
			server.ehlo()
			server.starttls()
	
		if args.auth:
			username = args.auth.split(':')[0]
			password = args.auth.split(':')[1]
			server.ehlo()
			server.login(username, password)
			
		server.sendmail(msg['From'], [msg['To']], msg.as_string())
		server.quit()
		print msg

	except SMTPException:
	   print "Error: unable to send email"

	
if __name__ == "__main__":
    main()