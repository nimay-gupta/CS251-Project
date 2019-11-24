from nltk.data import find
from bllipparser import RerankingParser
import os
import freq
import sys
import re
################## Forming a parse tree ##################
def textToWords(text):
	return re.findall(r'\w+', text.lower())
sentence=open(sys.argv[1]).read()
model_dir = find('models/bllip_wsj_no_aux').path
parser = RerankingParser.from_unified_model_dir(model_dir)
#{'language': 'En', 'case_insensitive': False, 'nbest': 5, 'small_corpus': True, 'overparsing': 21, 'debug': 0, 'smooth_pos': 0}
parser.set_parser_options(case_insensitive=True)
l = parser.parse(sentence)
Trees=[1,2]
Trees[0]=l.get_reranker_best().ptb_parse
Trees[1]=l.get_parser_best().ptb_parse
sentence=textToWords(sentence)
################# Tense correction for all types of verbs ###############
def sortSecond(val): 
    return val[1]
def get_phrase(index,word):
	ans=word
	if(index!=0):
		ans=sentence[index-1]+" "+ans
	if(index!=len(sentence)-1):
		ans=ans+" "+sentence[index+1]
	return ans
def get_phrase1(index,word):
	ans=word
	if(index!=len(sentence)-1):
		ans=ans+" "+sentence[index+1]
	return ans
def get_phrase2(index,word):
	ans=word
	if(index!=0):
		ans=sentence[index-1]+" "+ans
	return ans
def rem_dupl(l):
	ans=[]
	for x in l:
		a=0
		for y in ans:
			if(y[1]==x[1]):
				a=1
				break
		if(a==0):
			ans+=[x]
	return ans
def find_verb(tree,cnt):
	if(len(tree)==0):
		STR=str(tree)
		if(STR[1]=='V'):
			s=STR.split()
			s1=s[1]
			return [cnt+1,[[s1[:len(s1)-1].lower(),cnt]]]
		return [cnt+1,[]]
	ans=[]
	for x in tree:
		l=find_verb(x,cnt)
		cnt=l[0]
		ans+=l[1]
	return [cnt,ans]

path = os.path.join(os.path.dirname(__file__), "verb.txt")
data = open(path).readlines()
verbs={}
verbs_inf={}
for i in range(len(data)):
    a = data[i].strip().split(",")
    a = a[:12]
    l1=[]
    for x in a:
    	if(x==""):
    		continue
    	verbs_inf[x]=a[0]
    	l1+=[x]
    l1=list(set(l1))
    verbs[a[0]]=l1
listverb=[]
try:
	listverb+=find_verb(Trees[0],1)[1]
	listverb+=find_verb(Trees[1],1)[1]
except:
	a=0
listverb=rem_dupl(listverb)
listverb.sort(key = sortSecond)
for x in listverb:
	try:
		v=verbs_inf[x[0]]
	except:
		continue
	ans=[]
	ans1=[]
	for y in verbs[v]:
		score=0
		if(y==x[0]):
			score=freq.phraseScore(get_phrase(x[1]-1,y))*3
		else:
			score=freq.phraseScore(get_phrase(x[1]-1,y))
		if(score!=0):
			ans=ans+[[score,y]]
	if(len(ans)==0):
		for y in verbs[v]:
			score=0
			if(y==x[0]):
				score=freq.phraseScore(get_phrase1(x[1]-1,y))*3+freq.phraseScore(get_phrase2(x[1]-1,y))*3
			else:
				score=freq.phraseScore(get_phrase1(x[1]-1,y))+freq.phraseScore(get_phrase2(x[1]-1,y))
			if(score!=0):
				ans=ans+[[score,y]]
	ans.sort(reverse=True)
	i=0
	while(i<3):
		if(i==len(ans)):
				break
		if(ans[i][1]==x[0]):
			break
		ans1=ans1+[ans[i][1]]
		i+=1
	if(len(ans1)==0):
		continue
	print([x[1],x[0],ans1])

	