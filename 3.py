from nltk.corpus import wordnet
import sys

synonyms = []

for syn in wordnet.synsets(sys.argv[1]):
	for l in syn.lemmas():
		synonyms.append(l.name())
		
print(set(synonyms))