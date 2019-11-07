import sys
from nltk.corpus import words
import re
from collections import Counter
import math

# numIncorr represents how many incorrected strings are to be shown
numIncorr=3

# It extracts all the words from the parameter text
def textToWords(text):
	return re.findall(r'\w+', text.lower())

# It basically maintains a counter, i.e., each entry is a word and frequency of the word
# from the text file 'big.txt' 
WORDS = Counter(textToWords(open('big.txt').read()))

# DIC is basically my english dictionary. It is a list of all english words. 
DIC = set(words.words())
DIC = DIC.union(set(textToWords(open('big.txt').read())))

N=sum(WORDS.values())

# It returns all edits that are one edit away from the parameter word
def edits1(word):
	letters    = 'abcdefghijklmnopqrstuvwxyz'
	splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
	deletes    = [L + R[1:]               for L, R in splits if R]
	transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1 and R[0]!=R[1]]
	replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters if c!=R[0]]
	inserts    = [L + c + R               for L, R in splits for c in letters]
	return set(deletes + transposes + replaces + inserts)

# It returns all edits that are two or less edits away from the parameter word
def edits2(word):
	return set(e2 for e1 in edits1(word) for e2 in edits1(e1))

# It returns set of words which are present in DIC out of the parameter words
def known(words):
	return set(w for w in words if w in DIC)

def P(word):
	return WORDS[word] / N

def maximumProbable(words,n):
	if(len(words)<=n):
		return words
	s=set()
	i=0
	while(i<n):
		MAX=max(words,key=P)
		s.add(MAX)
		words.remove(MAX)
		i+=1
	return s

def candidates(word):
	if(len(known([word]))!=0):
		return []
	s1=known(edits1(word))
	if(len(s1)>=numIncorr):
		return maximumProbable(s1,numIncorr)
	s2=known(edits2(word))
	return s1.union(maximumProbable(s2.difference(s1),numIncorr-len(s1)))
for x in textToWords(open(sys.argv[1]).read()):
	l = list(known(candidates(x)))
	print("{} - {}".format(x,l))