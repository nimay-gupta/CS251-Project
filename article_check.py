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
arti = ["a", "an", "the"]

s = open(sys.argv[1]).read()

#done to split puncts separately
for i in puncts:
	s = s.replace(i, ' '+i+' ')
s = s.replace('\n', ' ')

WORDS = s.split()

for w in range(len(WORDS)):

	if WORDS[w] in arti:

		freq = []

		for art in arti:

			q = "https://api.datamuse.com/words?sp="+art

			if w > 0 and not(WORDS[w-1] in iitb_lingo) and not(WORDS[w-1] in puncts):
				q = q + '&lc=' + WORDS[w-1]
			if w < len(WORDS)-1 and not(WORDS[w+1] in iitb_lingo) and not(WORDS[w+1] in puncts):
				q = q + '&rc=' + WORDS[w+1]

			response = requests.get(q)
			l = response.json()

			freq.append(l[0]["score"])

		zipped = list(zip(arti, freq))
		zipped = sorted(zipped, key = lambda x: x[1], reverse = True)
		res = []
		for i in zipped:
			res.append(i[0])
		
		print(res, WORDS[w+1])