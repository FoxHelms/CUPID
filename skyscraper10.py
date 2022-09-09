#!/usr/bin/python3
from selenium import webdriver
from time import time, sleep
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
from permute_dates import createPerm
from messagemaker1 import makeMess
from working_email import sendMail

#config headless mode
options = Options()
options.headless = True
options.add_argument('--window-size=1920,1200')

#Give path to chrome driver using service argument so it doesn't throw the path deprecation warning
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
chromedriver_path = '/usr/bin/chromedriver'
abs_chromedriver_path = os.path.join(script_dir, chromedriver_path)

driver_service = Service(executable_path = abs_chromedriver_path)
browser = webdriver.Chrome(options=options,service = driver_service)
#browser = webdriver.Chrome(service = driver_service)

#Call function that creates permutations from date ranges and puts this tuple into a list
permList = createPerm()
numPerms = len(permList)

#Global variables
origin = 'DSM'
destinationList = ['LGA','JFK','EWR']
dateIndex = 0
url = 'https://www.google.com/travel/flights'
cheapFlightList = []
thresholdPrice = 100


#Click function
def browserClick(xPath):
	browser.find_element(By.XPATH, xPath).click()

#Enter function
def browserEnter(xPath):
	WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, xPath))).send_keys(Keys.ENTER)

#Type function
def browserType(xPath,phrase):
	browserClick(xPath)
	WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, xPath))).send_keys(phrase)
	browserEnter(xPath)

#Minimum Index function
def getMinInd(lst):
	index_min = min(range(len(lst)), key=lst.__getitem__)
	return index_min

#Backup Function
def backupItem(item):
	now = datetime.now()
	dt_string = now.strftime('%d/%m/%Y %H:%M')
	#script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
	rel_path_backup = 'backups/BackupFile.txt'
	abs_backup_path = os.path.join(script_dir, rel_path_backup)
	backupFile = open(abs_backup_path,'a')
	backupFile.write('\nBelow data scraped at: ' + dt_string + '\n')
	for i in item:
		backupFile.write('\n' + i + '\n')
	backupFile.close()

#Add price to external list file
def addToList(destination, minPrice):
	rel_path_prices = '{}Prices.txt'.format(destination)
	priceFile = open(rel_path_prices,'a')
	priceFile.write(str(minPrice) + '\n')
	priceFile.close()

#Get running averages
def runningAvg(destination):
	priceFile = open('{}Prices.txt'.format(destination),'r')
	priceStr = priceFile.read()
	priceStrLs = priceStr.splitlines()
	if '' in priceStrLs:
		priceStrLs.remove('')
	priceInts = []
	for str in priceStrLs:
		priceInts.append(int(str))		
	if len(priceInts) > 0:
		return sum(priceInts) / len(priceInts)

#check price against threshold
def checkPriceAgainstThresh(price):
	if price <= thresholdPrice:
		return True

#check current price against average price
def checkCurrentAgainstAvg(currentPrice,avgPrice):
	if currentPrice <= (avgPrice*0.53):
		return True

#Add flight data to already emailed list
def addToMailList(flightData):
	rel_path_mail_list = 'AlreadyMailed.txt'
	mailFile = open(rel_path_mail_list,'a')
	mailFile.write(flightData.replace('\n','') + '\n')
	mailFile.close()

#Check emailed list	
def checkMailList(flightData):
	rel_path_mail_list = 'AlreadyMailed.txt'
	otherMailFile = open(rel_path_mail_list,'r')
	mailedList = otherMailFile.read().splitlines()
	flightData = flightData.replace('\n','')
	if flightData in mailedList:
		return True
	

#Big boy function
def run(destination, leaveDate, returnDate):
	mainList = []
	prices = []
	clickList = 	[
		"//input[@aria-label='Departure']",
		"//div[@data-iso='{}']//div[@role='button']".format(leaveDate),
		"//div[@data-iso='{}']//div[@role='button']".format(returnDate),
		"//div[@class='WXaAwc']//button"
		]


	browser.get(url)
	browserType("//div[@aria-label='Enter your origin']//preceding-sibling::div[1]//input", origin)
	browserType("//div[@aria-label='Enter your destination']//preceding-sibling::div[1]//input", destination)

	for click in clickList:
		browserClick(click)
		sleep(0.5)

	sleep(3)

	htmlList = browser.find_elements(By.XPATH, '//ul[@class="Rk10dc"]//li')

	htmlList.pop()
	
	#Move data to list
	for element in htmlList: 
		item = element.text
		mainList.append(item)

	backupItem(mainList)

	#create a list of prices with the same index as mainList
	for flight in mainList:
		#segment price data by new line
		tempList = flight.splitlines()
		#Check list for price
		for item in tempList:
			if item.find('$') > -1:
				item = item.replace('$','')
				if ',' in item:
					item = item.replace(',','')
				priceInt = int(item)
				prices.append(priceInt)


	#Calculate min price and get min price flight data
	minPriceInd = getMinInd(prices)
	lowestPrice = prices[minPriceInd]
	flightData = mainList[minPriceInd]

	cheapFlight = (lowestPrice, leaveDate, returnDate, flightData)
	return cheapFlight
	

startTime = time()
#Loop through all permutations in the list and run program for the three airports
while dateIndex < numPerms:
	permTup = permList[dateIndex]
	leaveDate = permTup[0]
	returnDate = permTup[1]
	for destination in destinationList:
		tempFlightVar = run(destination, leaveDate, returnDate)
		cheapFlightList.append(tempFlightVar)
		addToList(destination, tempFlightVar[0])
		runAvg = runningAvg(destination)
		print(runAvg)
		if checkPriceAgainstThresh(tempFlightVar[0]) or checkCurrentAgainstAvg(tempFlightVar[0],runAvg):
			if checkMailList(tempFlightVar[3]):
				break
			msg = makeMess(tempFlightVar,destination)
			print(msg)
			sendMail(msg)
			addToMailList(tempFlightVar[3])
		sleep(1)
	dateIndex += 1

browser.close()
browser.quit()
endTime = time()
totTime = endTime - startTime
print(totTime)