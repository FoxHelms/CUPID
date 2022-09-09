


def getDigs(orStr):
	smNum = int(orStr.replace('-',''))
	lastDigs = abs(smNum) % 100 
	return lastDigs


def createPerm():
	i = 0
	j = 0
	dateList = open('dateListFull.txt','r')
	dateListString = dateList.read()
	listOfDates = dateListString.splitlines()
	numDates = len(listOfDates)
	dateRanges = []
	min = -30
	max = 4
	while i <= numDates-1 and j <= numDates-1:
		startDate = listOfDates[i]
		endDate = listOfDates[j]
		startDateDigits = getDigs(startDate)
		endDateDigits = getDigs(endDate)
		#print(startDateDigits)
		#print(endDateDigits)
		distance = endDateDigits - startDateDigits
		#print(distance)
		if -30 <= distance <= -27 or 0 <= distance <= 3:
			dateRanges.append((startDate, endDate))
			j+=1
			#print(i)
			continue
		i+=1
		j=i
		#print(i)
	return dateRanges