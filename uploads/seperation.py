import meddict, sys, re, collections

NWORDS, MEDWORDS = meddict.load_dict() 

def change_word(word,k):
	if len(word)-1 < k:
		if word in NWORDS[len(word)-1] or word in MEDWORDS[len(word)-1]:
			return [word]
	substitution = []
	j = len(word)
	for i in range(len(word),-1,-1):
		if word[i:j] in NWORDS[k] or word[i:j] in MEDWORDS[k]:
			substitution.append(word[i:j])
			if i < 25: 
				if word[:i] in NWORDS[i-1] or word[:i] in MEDWORDS[i-1]:
					substitution = [word[:i]] + substitution
					return substitution
			while k > 0:	
				reduced = change_word(word[:i],k) 
				if len(reduced) > 0:
					substitution = reduced + substitution
					return substitution
				k -= 1
			if len(substitution) == 1:
				return []
	return substitution


def processsymbol(wordList, symbol):
	refinedWordList = []
	newsymbol = symbol+' '
	for i in range(len(wordList)):
		r = wordList[i].find(symbol)
		if r+1 == len(wordList[i]) or r == -1:
			refinedWordList.append(wordList[i])
		elif r > 0 and r+1 < len(wordList[i]) and wordList[i][r+1].isalpha() or wordList[i][r-1].isalpha():
			wordList[i] = wordList[i].replace(symbol, newsymbol)
			change = wordList[i].split()
			for x in change:
				refinedWordList.append(x)
	return refinedWordList

def replace(filename):
	data = str()
	old_file = open(filename)
	
	for line in old_file:
		wordList = re.sub("[^\w:\d,'></%.()-]", " ",  line).split()
		wordList = processsymbol(wordList, '.')
		wordList = processsymbol(wordList, ',')
		wordList = processsymbol(wordList, ':')
		wordList = processsymbol(wordList, '-')
		list_of_suggestions = []
		best = 1000000000000000000000000000
		best_index = -1
		count = 0
		for word in wordList:
			if re.match('[\d]',word):
				data += word + " "
				continue
			r1 = word.find('.')
			r2 = word.find(',')
			r3 = word.find(':')
			r4 = word.find('-')
			present = False
			symbol = ''
			if (r1 > -1) or (r2 > -1) or (r3 > -1) or (r4 > -1):
				symbol = word[len(word)-1:]
				word = word[:len(word)-1]
				present = True
			if word.lower() not in NWORDS[1] and word.lower() not in MEDWORDS[1]:
				for t in range(10,0,-1):
					suggest = change_word(word.lower(), t)
					if len(suggest) > 0:
						list_of_suggestions.append(suggest)
						count += 1
					if count > 5:
						break
				if count == 0:				
					if present: data += word + symbol + " "
					else: data += word + " "
					continue

				for p in range(len(list_of_suggestions)):
					if len(list_of_suggestions[p]) < best:
						best = len(list_of_suggestions[p])
						best_index = p
				c = 0
				for n in list_of_suggestions[best_index]:
					if c+len(n) == len(word):
						data += word[c:c+len(n)]
					else:
						data += word[c:c+len(n)] + " "
					c = c+len(n)
				if present: data += symbol + " "
				else: data += " "
				
				best = 100000000000000000000000000
				best_index = -1
				count = 0
				list_of_suggestions = []
			
			else:	
				if present: data += word + symbol + " "
				else: data += word + " "

	old_file.close()
	return data
