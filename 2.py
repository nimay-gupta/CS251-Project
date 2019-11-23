from nltk.data import find
from bllipparser import RerankingParser
import os

################## Forming a parse tree ##################
model_dir = find('models/bllip_wsj_no_aux').path
parser = RerankingParser.from_unified_model_dir(model_dir)
#{'language': 'En', 'case_insensitive': False, 'nbest': 5, 'small_corpus': True, 'overparsing': 21, 'debug': 0, 'smooth_pos': 0}
parser.set_parser_options(nbest=3,case_insensitive=True)
l = parser.parse("i am going home")
Trees=[]
for x in l:
	Trees+=x.ptb_parse
print(Trees)
################# Tense correction for all types of verbs ###############
def find_verb(tree):
	if(len(tree)==0):
		STR=str(tree)
		if(STR[1]=='V'):
			s=STR.split()
			s1=s[1]
			return [s1[:len(s1)-1]]
	ans=[]
	for x in tree:
		ans+=find_verb(x)
	return ans

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
try:
	listverb=find_verb(Trees[0])
	listverb+=find_verb(Trees[1])
	listverb+=find_verb(Trees[2])
except:
	a=0
listverb=list(set(listverb))
for x in listverb:
	try:
		v=verbs_inf[x]
		print(verbs[v])
	except:
		a=0