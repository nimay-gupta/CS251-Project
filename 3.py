import urllib
from nltk.corpus import wordnet
import sys
import requests
import re

#dictionary of iitb lingo
iitb_lingo = {
	"bc": "branch change",
	"machax": "great",
	"crax": "cracked",
	"insti": "institute",
	"RG": "closed door tactics",
	"arbit": "arbitrary",
	"furra": "fail grade",
	"lukha": "free",
	"Poltu": "politics enthusiast",
	"enthu": "enthusiasm",
	"junta": "people",
	"maggu": "book worm",
	"machaya": "did an awesome job"
}

#list of common launguage punctuations and symbols
puncts = ['.', '!', ',', ';', '"', "'", '(', ')', '-', '[', ']', '{', '}', '?', '/', ':', '@', '&']

s = open(sys.argv[1]).read()

#done to split puncts separately
for i in puncts:
	s = s.replace(i, ' '+i+' ')
s = s.replace('\n', ' ')

WORDS = s.split()
WORDS = list(map(lambda x: x.lower(), WORDS))

#now WORDS = list of puncts and lower-cased words in arg text

print(WORDS)

for w in range(len(WORDS)):

	if WORDS[w] in puncts:
		continue

	print(WORDS[w], end=": ")

	if WORDS[w] in iitb_lingo:
		print(iitb_lingo[WORDS[w]])

	else:

		synonyms = []

		q = "https://api.datamuse.com/words?ml="+WORDS[w]

		#building trigram such that adjacent words shouldn't be iitb lingo or punctuation
		if w > 0 and not(WORDS[w-1] in iitb_lingo) and not(WORDS[w-1] in puncts):
			q = q + '&lc=' + WORDS[w-1]
		if w < len(WORDS)-1 and not(WORDS[w+1] in iitb_lingo) and not(WORDS[w+1] in puncts):
			q = q + '&rc=' + WORDS[w+1]

		response = requests.get(q)
		l = response.json()

		for i in l:
			synonyms.append(i["word"])


		#phrase finder
		# freq = []

		# for i in synonyms:

		# 	phrase = i
		# 	if w > 0 and not(WORDS[w-1] in iitb_lingo) and not(WORDS[w-1] in puncts):
		# 		phrase = WORDS[w-1] + ' ' + phrase
		# 	if w < len(WORDS)-1 and not(WORDS[w+1] in iitb_lingo) and not(WORDS[w+1] in puncts):
		# 		phrase = phrase + ' ' + WORDS[w+1]

		# 	encoded_query = urllib.parse.quote(phrase)
		# 	params = {'corpus': 'eng-gb', 'query': encoded_query}
		# 	params = '&'.join('{}={}'.format(name, value) for name, value in params.items())

		# 	response = requests.get('https://api.phrasefinder.io/search?' + params)
		# 	assert response.status_code == 200

		# 	if len(response.json()["phrases"]) > 0:
		# 		freq.append(response.json()["phrases"][0]["mc"])
		# 	else:
		# 		freq.append(0)

		# zipped = list(zip(synonyms, freq))
		# zipped = sorted(zipped, key = lambda x: x[1], reverse = True)
		# res = []
		# for i in range(min(3,len(zipped))):
		# 	res.append(zipped[i][0])
		# print(res)


		#top 5 synonyms
		print(synonyms[:5])