#flight message creator


def makeMess(lst,destination):
	message = 'I found a flight for ${} that lands at {}\nLeave date: {} \nReturn date: {} \n\n {}'.format(str(lst[0]),destination,lst[1],lst[2],lst[3])
	return message