import os

f = open("admin_email.txt", 'w')
email = input("Please enter your email address:\n(this email address will receive system notifications)\n")
f.write(email)
print("System status: initializing...")
os.system("python3 surveillance_cam.py")
print("System status: OFFLINE")
