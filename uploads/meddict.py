import re, collections, sys

def words(text): return re.findall('[a-z]+', text.lower())

def train(features, x):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        if len(f)>x:
            model[f] += 1
    return model

normaldictionary = file('american-english').read()
medicaldictionary = file('refinemedterms').read()

def load_dict():
	NWORDS , MEDWORDS = [], []
	for i in range(25):
		NWORDS.append(train(words(normaldictionary),i))
		MEDWORDS.append(train(words(medicaldictionary),i))
	return NWORDS, MEDWORDS
