from nltk.data import find
from bllipparser import RerankingParser
import freq

################## Forming a parse tree ##################
model_dir = find('models/bllip_wsj_no_aux').path
parser = RerankingParser.from_unified_model_dir(model_dir)
#{'language': 'En', 'case_insensitive': False, 'nbest': 5, 'small_corpus': True, 'overparsing': 21, 'debug': 0, 'smooth_pos': 0}
parser.set_parser_options(nbest=2,case_insensitive=True)
l = parser.parse("I bought, one red new bike.")
Trees=[]
for x in l:
	Trees+=x.ptb_parse
print(Trees)

def sortSecond(val):
	return val[1]

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
		if((STR[1]=='J' and STR[2]=='J') or (STR[1]=='C' and STR[2]=='D')):
			s=STR.split()
			s1=s[1]
			if(STR[1]=='J'):
				return [cnt+1,[[cnt,s1[:len(s1)-1]]]]
			else:
				return [cnt+1,[[cnt,s1[:len(s1)-1],0]]]
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
listadj.sort(key=sortSecond)
l=[]
diff=0
i=0
while i <len(listadj):
	if(len(listadj[i])==3):
		j=i
		temp=listadj[i][1]
		while(len(listadj[i+1])==3 and i+1<len(listadj) and listadj[i][0]+1==listadj[i+1][0]):
			i+=1
			temp=temp+" "+listadj[i][1]
		l=l+[[listadj[j][0]-diff,temp,1]]
		diff=diff+i-j
		i+=1
	else:
		l=l+[[listadj[i][0]-diff,listadj[i][1]]]
		i+=1
print(l)


i = 0
while i < len(l):
	x = i
	while x < len(l)-1 and l[x+1][0] == l[x][0]+1:
		x = x + 1
	if x-i == 1:
		if freq.phraseScore(l[i+1][1] + ' ' + l[i][1]):
			print(l[i][1] + ' ' + l[i+1][1] + ' -> ' + l[i+1][1] + ' ' + l[i][1])
	elif x-i == 2:
		origi = l[i][1] + ' ' + l[i+1][1] + ' ' + l[i+2][1]
		one = l[i][1] + ' ' + l[i+2][1] + ' ' + l[i+1][1]
		two = l[i+2][1] + ' ' + l[i][1] + ' ' + l[i+1][1]
		three = l[i+2][1] + ' ' + l[i+1][1] + ' ' + l[i][1]
		four = l[i+1][1] + ' ' + l[i][1] + ' ' + l[i+2][1]
		five = l[i+1][1] + ' ' + l[i+2][1] + ' ' + l[i][1]
		perms = []
		perms.append(origi)
		perms.append(one)
		perms.append(two)
		perms.append(three)
		perms.append(four)
		perms.append(five)
		scor = []
		for it in range(6):
			scor.append(freq.phraseScore(perms[it]))
		zipped = list(zip(perms,scor))
		zipped = sorted(zipped, key = lambda x: x[1], reverse = True)
		out = zipped[0][0]
		print(zipped)
	i = x + 1