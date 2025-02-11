#!user/bin/env python3

import subprocess, smtplib

def sendEmail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "echo hello"
# subprocess.Popen(command, shell=True)
result = subprocess.check_output(command, shell=True)
sendEmail("andy.karandikar@gmail.com", "shqd jzee bfkg isut", result) #gmail "app password"
