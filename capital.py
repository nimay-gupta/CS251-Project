from nltk.data import find
from bllipparser import RerankingParser
import sys
import re
################## Forming a parse tree ##################
def textToWords(text):
	return re.findall(r'\w+',text)
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
################# finding all proper nouns in a sentence #################
def lowercase(s):
	for x in s:
		if(x>='0' and x<'9'):
			return True
		if(x<'a' or x>'z'):
			return False
	return True
def lowercase1(s):
	if(s[0]>='a' and s[0]<='z'):
		return False
	return lowercase(s[1:])
def getlowercase(s):
	ans=""
	for x in s:
		ans=ans+x.lower()
	return ans
def getlowercase1(s):
	return s[0].upper()+getlowercase(s[1:])
def sortSecond(val): 
    return val[1]
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
def find_proper_noun(tree,cnt):
	if(len(tree)==0):
		STR=str(tree)
		if(STR[1]=='N' and STR[2]=='N' and STR[3]=='P'):
			s=STR.split()
			s1=s[1]
			return [cnt+1,[[s1[:len(s1)-1].lower(),cnt]]]
		return [cnt+1,[]]
	ans=[]
	for x in tree:
		l=find_proper_noun(x,cnt)
		cnt=l[0]
		ans+=l[1]
	return [cnt,ans]
listnoun=[]
try:
	for x in range(2):
		listnoun+=find_proper_noun(Trees[x],1)[1]
except:
	a=0
listnoun=rem_dupl(listnoun)
listnoun.sort(key = sortSecond)
index=0
ans=[]
i=0
while(i<len(sentence)):
	if(i==0):
		if(lowercase1(sentence[i])):
			if(i+1==listnoun[index][1]):
				index+=1
			i+=1
			continue
		ans=ans+[[i+1,sentence[i],[getlowercase1(sentence[i])]]]
		i+=1
		continue
	if(index<len(listnoun) and i+1==listnoun[index][1]):
		index+=1
		if(lowercase1(sentence[i])):
			i+=1
			continue
		ans=ans+[[i+1,sentence[i],[getlowercase1(sentence[i])]]]
		i+=1
		continue
	else:
		if(lowercase(sentence[i])):
			i+=1
			continue
		ans=ans+[[i+1,sentence[i],[getlowercase(sentence[i])]]]
		i+=1
		continue
print(ans)
