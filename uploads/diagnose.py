import meddict, sys, re, collections, seperation

def verify_sentence(data):
	newdata =str()
	wordList = data.split('.')
	termFile =  open('terms')
	termList = { }
	diagnose = { }
	match_term = [ ]
	symptom = []
	present = False;
	for line in termFile:
		terms = line.split(':')
		termList[terms[0].lower().strip()] = terms[1].strip()
		match_term.append(terms[0].lower().strip())

	for sentence in wordList:
		for words in match_term:
			present = False
			if re.search(words, sentence.lower().strip()):
				present = True
				negate = ['no .', 'negative for .', 'negative .', 'no evidence .', 'without .']
				for each in negate:
					if re.search(each+'*'+words, sentence.lower().strip()):
						present = False
						break
			if present:
				new_sentence = str()
				i = 0
				for m in re.finditer(words, sentence.lower().strip()):
					 new_sentence += sentence[i:m.start()] + "<span class=\"name\">" + sentence[m.start():m.end()+1] + "</span>"
					 i = m.end()+1
				new_sentence += sentence[i:]
				if words not in symptom:
					print words
					symptom.append(words)
				if termList[words] in diagnose:
					newdata = diagnose[termList[words]] + new_sentence + ". "
				else:
					newdata = new_sentence + ". "
				diagnose[termList[words]] = newdata
	return diagnose, termList, symptom

data = seperation.replace('message.txt')
diagnose, terms, symptom = verify_sentence(data)
diagnose_data = str()
symptom_data = str()
for each in symptom:
	diagnose_data += terms[each] + ".\n"
	symptom_data += "<span class=\"big\">" + diagnose[terms[each]] + "</span>\n"
new_file = open('result.txt', 'w')
new_file.write(symptom_data)
new_file.close()
new_file = open('diagnose.txt', 'w')
new_file.write(diagnose_data)
new_file.close()
