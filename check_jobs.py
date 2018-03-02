#!/usr/bin/env python

import subprocess
import time
from sys import exit
import os
import paramiko
import argparse
import smtplib
import getpass

#bits and pieces obtained from SO

def launch_command(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out = out.strip().split()
    return out

def send_email(user, pwd, recipient, subject, body):

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"

def email_content(job_started, check):
    if check == 'pending':
        subject = "started this job " + str(job_started)
        body    = "started this job " + str(job_started) + "\n"
    if check == 'running':
        subject = "finished/running job " + str(job_started)
        body    = "finished/running (depending on poll interval) job " + str(job_started) + "\n"
    body    = body + "This is an automated email from a Python mail client."
    return subject, body

def main(args, gmail_pass):
    if str(args.check[0]) == 'pending':
        command = ["ssh", "-n", "bsc15755@mn1.bsc.es" , "-CY", "'./pendingjobs.bash'"]
    if str(args.check[0]) == 'running':
        command = ["ssh", "-n", "bsc15755@mn1.bsc.es" , "-CY", "'./runningjobs.bash'"]
    OLD_P_JOBS = launch_command(command)


    gmail_user = str(args.guser[0])
    email      = str(args.email[0])

    while True:
        if OLD_P_JOBS: NEW_P_JOBS = launch_command(command)
        if not NEW_P_JOBS: exit('all jobs did something')
        JOB_STARTED = list(set(OLD_P_JOBS).symmetric_difference(set(NEW_P_JOBS)))
        if JOB_STARTED:
            OLD_P_JOBS = NEW_P_JOBS
            subject, body = email_content(JOB_STARTED, str(args.check[0]))
            send_email(gmail_user, gmail_pass, email, subject, body)
        time.sleep(60*5) # poll every fiveminutes

if __name__ == '__main__':
    gmail_pass = getpass.getpass('Password:')
    parser = argparse.ArgumentParser(description="To check if file exists and send email")
    parser.add_argument('-g', '--guser', nargs=1,help='gmail user')
    parser.add_argument('-e','--email', nargs=1, help='email to send')
    parser.add_argument('-c','--check', nargs=1, help='check pending or running')
    args = parser.parse_args()
    main(args, gmail_pass)

