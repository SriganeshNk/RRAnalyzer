import meddict, sys, re, collections, seperation

def verify_sentence(data):
	newdata =str()
	wordList = data.split('.')
	termFile =  open('terms')
	termList = []
	diagnose = str()
	not_present = True
	negative = False
	for line in termFile:
		terms = line.split(',')
		termList.append(terms)

	for words in wordList:
		i = 0

		while i < len(termList):
			j = 0
			negative = False
			not_present = True
			while j < len(termList[i]):

				if re.search(termList[i][j].lower().strip(), words.lower().strip()):
					newdata += words + '.'
					negate = ['no', 'negative for', 'negative', 'no evidence', 'without']
					not_present = False
					for each in negate:
						if re.search(each+".*"+termList[i][j].lower().strip(), words.lower().strip()):
							negative = True
							break
					if negative:
						not_present = True
						break
				j = j+1

			if not not_present:
				for x in termList[i+1]:
					if x == termList[i+1][len(termList[i+1])-1]:
						diagnose += x.strip() + '.'
					else:
						diagnose += x.strip() + ', '
				break
			if negative:
				diagnose += 'NONE.'
				break
			i = i+2
	return newdata, diagnose

data = seperation.replace('message.txt')
data, diagnose = verify_sentence(data)
new_file = open('result.txt', 'w')
new_file.write(data)
new_file.close()
new_file = open('diagnose.txt', 'w')
new_file.write(diagnose)
new_file.close()
