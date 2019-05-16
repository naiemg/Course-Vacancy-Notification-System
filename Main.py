import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from time import clock
import timeit
import sys
import re

# Course code for the classes that I am tracking	
classes = ["50541","50517","50485","50489","50469","50470","50549","50495"]	#50467 is the test one
# Places to send a reminder to (emails, mobile-numbers)
devices = ["naiem.gafar@gmail.com","9174360541@tmomail.net"]

# Function that checks if a class is available
def isAvailable(section, list):
	# Looks through the entire text of the page for that classes' course code
	if section in onlyNumbers:
		# If it IS there, create a message
		sectionNumberIsAvail = section + " is available"
		for recipient in list:
			# Send a reminder to each email/ phone number
			subject = "A Class is Available!"
			message = "NOTICE: " + sectionNumberIsAvail + "\n\nVisit: bit.do/ePGPV \n Thank you!-"
			sendNotification(recipient,subject,message)
	else:
		print(section + " is unavailable")

# Function that sends an email to notify when a class has become available
# Is called below . . . 
def sendNotification(recipient, subjectLine, notification):  
	email = "naiememailbot@gmail.com"
	password = "%?k3?nu?bgk3em!&%@fntm!=njtfs=rh"
	send_to_email = recipient
	subject = subjectLine
	message = notification

	msg = MIMEMultipart()
	msg['From'] = email
	msg['To'] = send_to_email
	msg['Subject'] = subject

	msg.attach(MIMEText(message, 'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo() 
	server.starttls()
	server.login(email, password)
	text = msg.as_string()
	server.sendmail(email, send_to_email, text)
	server.quit()

try:
	# Starts a timer that tracks the execution's duration time
	start = timeit.default_timer()

	# Opens CUNYFirst GLobal Search Website
	options = webdriver.ChromeOptions()
	options.headless = True
	driver = webdriver.Chrome(executable_path=r'C:\webdrivers\chromedriver.exe', options=options)
	driver.get("https://globalsearch.cuny.edu/CFGlobalSearchTool/search.jsp")

	# Fills out the form fields by looking for HTML elements
	login_form = driver.find_element_by_xpath("//input[@id='QNS01']").click()	# Queens College
	login_form = driver.find_element_by_xpath("//option[@value='1199']").click()	# Fall 2019
	login_form = driver.find_element_by_xpath("//input[@class='SSSBUTTON_CONFIRMLINK']").click()	# Click "NEXT"

	time.sleep(1)	# Wait for it to get to the next page (form continues)
	login_form = driver.find_element_by_xpath("//option[@value='CMSC']").click()	# Computer Science
	login_form = driver.find_element_by_xpath("//input[@id='btnGetAjax']").click()	# Click "SEARCH"

	time.sleep(1)	# Wait for it to get to the next page (lists all the results)
	login_form = driver.find_element_by_xpath("//a[@id='imageDivLink_inst0']").click()	# Expands the page


	# Expands all available courses
	c = 0;
	try:
		while(c < 50):
			# Looks for the expand icons and clicks on them until all of the courses are expanded
			login_form = driver.find_element_by_xpath("//a[@id='imageDivLink" + str(c)+ "']").click()
			c += 1
	except:
		pass	
		# When you get to the end of the page and there is nothing more to expand
		# This exception will catch the error

	# Gathers the entire body of the page (ie. all of the text on the page and stores it into 'body'
	body = driver.find_element_by_xpath("//div[@id='contentDivImg_inst0']")
	# Filters the page to only get the numbers with 5 digits
	onlyNumbers = re.findall("\d{5}", body.text)
	
	# Looks for each course
	# Calling the function above
	for section in classes:
		isAvailable(section, devices)

	driver.close()	# Close the browser
	stop = timeit.default_timer()	# End timer
	elapsed = stop-start	# Calculate the elapsed time

	# Timestamp of the current time and date
	current = str(datetime.datetime.now())

	# Logs the timestamp and elapsed run-time in a log file
	import csv
	b=open(r"C:\Users\Naiem\Desktop\Side Projects\Class Notifier\Log.csv", 'a',newline='')
	a=csv.writer(b)
	a.writerow([current,elapsed])
	b.close()
	
except Exception as e:
	for recipient in devices:
		sendNotification(recipient,
						"ERROR 999: Technical Difficulties",
						"Class Notifier is experiencing technical difficulties at this time!-")
	print(e)
	sys.exit(0)