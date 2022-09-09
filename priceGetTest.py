
import re



mainList = '''6:30 AM
	 – 
	1:52 PM
	United
	6 hr 22 min
	DSM–LGA
	1 stop
	2 hr 47 min ORD
	180 kg CO2
	Avg emissions
	$422
	round trip'''



prices = []

flightPrice = mainList.find('$')
print(flightPrice)



