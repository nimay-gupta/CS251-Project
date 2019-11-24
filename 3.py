import urllib
from nltk.corpus import wordnet
import sys
import requests
import re
from nltk.data import find
from bllipparser import RerankingParser
import freq

sentence = "I bought a red new bike, Machax!"

################## Forming a parse tree ##################
model_dir = find('models/bllip_wsj_no_aux').path
parser = RerankingParser.from_unified_model_dir(model_dir)
#{'language': 'En', 'case_insensitive': False, 'nbest': 5, 'small_corpus': True, 'overparsing': 21, 'debug': 0, 'smooth_pos': 0}
parser.set_parser_options(nbest=2,case_insensitive=True)
l = parser.parse(sentence)
Trees=[]
for x in l:
	Trees+=x.ptb_parse
print(Trees)

def rem_dupl(l):
	ans=[]
	for x in l:
		a=0
		for y in ans:
			if(y[0]==x[0]):
				a=1
				break
		if(a==0):
			ans+=[x]
	return ans

def find_syn(tree,cnt):
	if(len(tree)==0):
		STR=str(tree)
		if((STR[1]=='J' and STR[2]=='J') or (STR[1]=='N' and STR[2]=='N') or True):
			s=STR.split()
			s1=s[1]
			if(STR[1]=='J'):
				return [cnt+1,[[cnt,s1[:len(s1)-1]]]]
			else:
				return [cnt+1,[[cnt,s1[:len(s1)-1]]]]
		return [cnt+1,[]]
	ans=[]
	for x in tree:
		l=find_syn(x,cnt)
		cnt=l[0]
		ans+=l[1]
	return [cnt,ans]
synlist=[]
try:
	for x in range(2):
		synlist+=find_syn(Trees[x],1)[1]
except:
	a=0
synlist=rem_dupl(synlist)
synlist = list(map(lambda x: x[1], synlist))

print(synlist)

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

# s = open(sys.argv[1]).read()

#done to split puncts separately
for i in puncts:
	sentence = sentence.replace(i, ' '+i+' ')
# sentence = sentence.replace('\n', ' ')

WORDS = sentence.split()
# WORDS = list(map(lambda x: x.lower(), WORDS))

#now WORDS = list of puncts and lower-cased words in arg text

print(WORDS)

it = 1
for w in synlist:

	while(WORDS[it-1] != w):
		it = it + 1

	if w in puncts:
		continue

	if w.lower() in iitb_lingo:
		print([it, w, [iitb_lingo[w.lower()]]])

	else:

		synonyms = []

		q = "https://api.datamuse.com/words?ml=" + w

		#building trigram such that adjacent words shouldn't be iitb lingo or punctuation
		if it > 1 and not(WORDS[it-2] in iitb_lingo) and not(WORDS[it-2] in puncts):
			q = q + '&lc=' + WORDS[it-2]
		if it < len(WORDS) and not(WORDS[it] in iitb_lingo) and not(WORDS[it] in puncts):
			q = q + '&rc=' + WORDS[it]

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
		print([it, w, synonyms[:3]])