from nltk.data import find
from bllipparser import RerankingParser

################## Forming a parse tree ##################
model_dir = find('models/bllip_wsj_no_aux').path
parser = RerankingParser.from_unified_model_dir(model_dir)
#{'language': 'En', 'case_insensitive': False, 'nbest': 5, 'small_corpus': True, 'overparsing': 21, 'debug': 0, 'smooth_pos': 0}
parser.set_parser_options(nbest=2,case_insensitive=True)
l = parser.parse("i bought a red large bike")
Trees=[]
for x in l:
	Trees+=x.ptb_parse
################# finding all proper nouns in a sentence #################

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
def find_adj(tree,cnt):
	if(len(tree)==0):
		STR=str(tree)
		if(STR[1]=='J' and STR[2]=='J'):
			s=STR.split()
			s1=s[1]
			return [cnt+1,[[cnt,s1[:len(s1)-1]]]]
		return [cnt+1,[]]
	ans=[]
	for x in tree:
		l=find_adj(x,cnt)
		cnt=l[0]
		ans+=l[1]
	return [cnt,ans]
listadj=[]
try:
	for x in range(2):
		listadj+=find_adj(Trees[x],1)[1]
except:
	a=0
listadj=rem_dupl(listadj)