#!/usr/bin/env python3
import smtplib
from email.message import EmailMessage
import os
import time
import subprocess as sp
from dotenv import load_dotenv

#Programmer: Mario Martinez
#date: 01/21/2022
#Purpose: To curb spam by sabotage

load_dotenv() 	#You will need to create a .env file with 
				#export USER="username"
				#export PASSWORD="password"
password = os.environ.get('PASSWORD')

#start local mail relay
os.system('echo ' + password + ' | sudo -S postfix start')

print()
#set up variables
textfile = 'messages.dat'
mailServer = 'localhost'
sender = 'ericashaffer733@tina.squitemaili.info'
recipient = 'ericashaffer733@tina.squitemaili.info'
messageTitle = 'I want to meet now'
numOfMessages = 10

text = open('messages.dat', 'r')
messages = text.readlines()

# Create message from text file line j
fileLine = 1
msg = EmailMessage()
msg.set_content(messages[fileLine])
	
# create the header
msg['Subject'] = messageTitle
msg['From'] = sender
msg['To'] = recipient

# Send the message via localhost
messageCount = 0
for count in range(numOfMessages):
	s = smtplib.SMTP(mailServer)
	s.send_message(msg)
	s.quit()
	messageCount += 1
print(messageCount, 'Messages sent')
	
# Wait for messages to finish sending then stop mail relay 
# In production program return to command and leave in queue
# TODO: 
#		1. add a check queue option (sudo mailq)
#		2. add a flush option (sudo postfix flush)
#		3. add a delete all queue (sudo postsuper -d ALL)
# 		4. check if queue is empty before quiting
timeElapsed = 0
while(sp.getoutput('mailq') != 'Mail queue is empty'):
	print('Waiting for queue to empty', timeElapsed, 'seconds elapsed.')
	time.sleep(1)
	timeElapsed += 1

print('Closing postfix')
os.system('sudo postfix stop')
print('Done')

###
### TODO:
### 1. Figure proxychains and add it to the os.system command
### 2. Develop UI 
### 	a. ask oreborus (self replicating) or spiderweb (list to list)
###		b. ask for contagious oreborus (send 10 from previous to new, and 10 from new to new
###		c. ask how may to send
### 3. Read messages, titles, and recipients from files