from nltk.data import find
from bllipparser import RerankingParser

################## Forming a parse tree ##################
model_dir = find('models/bllip_wsj_no_aux').path
parser = RerankingParser.from_unified_model_dir(model_dir)
#{'language': 'En', 'case_insensitive': False, 'nbest': 5, 'small_corpus': True, 'overparsing': 21, 'debug': 0, 'smooth_pos': 0}
parser.set_parser_options(nbest=2,case_insensitive=True)
l = parser.parse("this is a ball")
Trees=[]
for x in l:
	Trees+=x.ptb_parse
for x in Trees:
	print(x)

################# finding all proper nouns in a sentence #################
def find_pronoun(tree):
	if(len(tree)==0):
		STR=str(tree)
		if(STR[1]=='D' and STR[2]=='T'):
			s=STR.split()
			s1=s[1]
			return [s1[:len(s1)-1]]
	ans=[]
	for x in tree:
		ans+=find_pronoun(x)
	return ans
listpronoun=[]
try:
	for x in range(2):
		listpronoun+=find_pronoun(Trees[x])
except:
	a=0
listpronoun=list(set(listpronoun))
dempronoun=set(["this","these","that","those"])
for x in listpronoun:
	if x in dempronoun:
		print(x)
