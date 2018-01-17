#!/usr/bin/env python

#17-1-2018
#rajiv.nishtala@bsc.es
#send emails while on vacation

#Credits to SO for a large part of the code

import os
import paramiko
import argparse
import smtplib
from time import sleep

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

def email_content(FILE_NAME, remote_path):
    subject = 'Results for ' + FILE_NAME
    body    = "Hi Paul,\n"
    body    = body + "Please find attached the results for " + FILE_NAME + ' in ' + remote_path + "\n"
    body    = body + "Best wishes,\n"
    body    = body + "Rajiv\n"
    body    = body + "This is an automated email from a Python mail client."
    return subject, body

def main(args):
    server   = str(args.server[0])
    username = str(args.user[0])
    password = str(args.passw[0])
    gmail_user = str(args.guser[0])
    gmail_pass = str(args.gpass[0])
    email      = str(args.email[0])
    BASEPATH   = '/home/bsc15/bsc15755/automate_scripts_single_trace/'
    FILENAMES  = [BASEPATH + 'HYDRO_S.out', BASEPATH + 'ALYA_EXAHEX.out']

    transport=paramiko.Transport(server)
    transport.connect(username=username,password=password)
    sftp=paramiko.SFTPClient.from_transport(transport)

    while True:
        sleep(60*30) #30minutes sleep interval
        for filename in FILENAMES:
            try:
                filestat=sftp.stat(remotepath)
                subject, body = email_content(filename, remotepath)
                send_email(gmail_user, gmail_pass, email, subject, body)
                FILENAMES.remove(filename)
            except IOError as IE:
                pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="To check if file exists and send email")
    parser.add_argument('-s', '--server'   , nargs=1, help='server')
    parser.add_argument('-u', '--user'   , nargs=1, help='username')
    parser.add_argument('-p', '--passw', nargs=1, help='not safe at all...')
    parser.add_argument('-g', '--guser', nargs=1,help='gmail user')
    parser.add_argument('-gp','--gpass', nargs=1, help='gmail pass')
    parser.add_argument('-e','--email', nargs=1, help='email to send')
    args = parser.parse_args()
    main(args)
