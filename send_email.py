import sys
import smtplib
import config_email
from email.message import EmailMessage

def send_email(f):
	
	admin_file = open("admin_email.txt", 'r')
	send_to = admin_file.read()
	
	msg = EmailMessage()
	msg['From'] = "eecs488surveillancesystem@gmail.com"
	msg['To'] = send_to
	msg['Subject'] = "[ALERT] Surveillance System: Possible Intruder"
	
	body = "A possible intruder has been spotted by the surveillance system.\n\nPlease inspect the attached video and refer to the web-interface for more information."
	msg.set_content(body)
	msg.add_alternative("""\
	<!DOCTYPE html>
	<html>
		<body>
			<h2 style="font-family: Courier New; font-size:120%">ALERT:</h2>
			<p style="font-family: Courier New; font-size:120%">
				A possible intruder has been spotted by the surveillance system.<br>
				Please inspect the attached video and refer to the web-interface for more information.
			</p>
			<h3>
				<a href="http://10.0.0.5">Web Interface</a>
			</h3>
		</body>
	</html>
	""", subtype='html')
	
	with open(f, 'rb') as fil:
		file_data = fil.read()
		file_name = "intruder_video.avi"
	
	msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
	
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(config_email.EMAIL_ADDRESS, config_email.PASSWORD)
	server.sendmail(config_email.EMAIL_ADDRESS, send_to, msg.as_string())
	server.quit()
	
	print("Email alert nofication sent.")

video_name = sys.argv[1]
send_email(video_name)
