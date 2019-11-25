from nltk.data import find
from bllipparser import RerankingParser
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
S1=sentence
S1=S1.split()
sentence=textToWords(sentence)
################# finding all proper nouns in a sentence #################
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
def find_pronoun(tree,cnt):
	if(len(tree)==0):
		STR=str(tree)
		if(STR[1]=='D' and STR[2]=='T'):
			s=STR.split()
			s1=s[1]
			return [cnt+1,[[s1[:len(s1)-1].lower(),cnt]]]
		return [cnt+1,[]]
	ans=[]
	for x in tree:
		l=find_pronoun(x,cnt)
		cnt=l[0]
		ans+=l[1]
	return [cnt,ans]
listpronoun=[]
try:
	for x in range(2):
		listpronoun+=find_pronoun(Trees[x],1)[1]
except:
	a=0
listpronoun=rem_dupl(listpronoun)
listpronoun.sort(key = sortSecond)
dempronoun1=set(["this","these"])
dempronoun2=set(["that","those"])
ANS={}
tempans=[]
for x in listpronoun:
	ans=[]
	ans1=[]
	if x[0] in dempronoun1:
		for y in dempronoun1:
			score=0
			if(y==x[0]):
				score=freq.phraseScore(get_phrase(x[1]-1,y))*3
			else:
				score=freq.phraseScore(get_phrase(x[1]-1,y))	
			if(score>0):
				ans=ans+[[score,y]]
		if(len(ans)==0):
			for y in dempronoun1:
				score=0
				if(y==x[0]):
					score=freq.phraseScore(get_phrase1(x[1]-1,y))*3
				else:
					score=freq.phraseScore(get_phrase1(x[1]-1,y))
				if(score>0):
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
		#tempans=tempans+[[x[1]-1,ans1]]
		print([x[1],x[0],ans1])
	if x[0] in dempronoun2:
		for y in dempronoun2:
			score=0
			if(y==x[0]):
				score=freq.phraseScore(get_phrase(x[1]-1,y))*3
			else:
				score=freq.phraseScore(get_phrase(x[1]-1,y))	
			if(score>0):
				ans=ans+[[score,y]]
		if(len(ans)==0):
			for y in dempronoun2:
				score=0
				if(y==x[0]):
					score=freq.phraseScore(get_phrase1(x[1]-1,y))*3
				else:
					score=freq.phraseScore(get_phrase1(x[1]-1,y))
				if(score>0):
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
		#tempans=tempans+[[x[1]-1,ans1]]
		print([x[1],x[0],ans1])
# tempans.sort()
# j=0
# i=0
# while(i<len(S1)):
# 	if(j==len(tempans) or i!=tempans[j][0]):
# 		ANS[S1[i]]=[]
# 		i+=1
# 		continue
# 	ANS[S1[i]]=tempans[j][1]
# 	j+=1
# 	i+=1
# print(ANS)