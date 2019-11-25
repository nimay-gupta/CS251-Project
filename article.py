# ARTICLE - last updated for NodeBox 1rc7
# Author: Tom De Smedt <tomdesmedt@organisms.be>
# See LICENSE.txt for details.

# Based on the Ruby Linguistics module by Michael Granger:
# http://www.deveiate.org/projects/Linguistics/wiki/English
import re
import requests

article_rules = [        

    ["euler|hour(?!i)|heir|honest|hono", "an"],       # exceptions: an hour, an honor

    # Abbreviations
    # Strings of capitals starting with a vowel-sound consonant
    # followed by another consonant,
    # and which are not likely to be real words.
    ["(?!FJO|[HLMNS]Y.|RY[EO]|SQU|(F[LR]?|[HL]|MN?|N|RH?|S[CHKLMNPTVW]?|X(YL)?)[AEIOU])[FHLMNRSX][A-Z]", "an"],
    ["^[aefhilmnorsx][.-]", "an"],
    ["^[a-z][.-]", "a"],

    ["^[^aeiouy]", "a"],                              # consonants: a bear
    ["^e[uw]", "a"],                                  # eu like "you": a european
    ["^onc?e", "a"],                                  # o like "wa": a one-liner
    ["uni([^nmd]|mo)", "a"],                          # u like "you": a university
    ["^u[bcfhjkqrst][aeiou]", "a"],                   # u like "you": a uterus
    ["^[aeiou]", "an"],                               # vowels: an owl
    ["y(b[lor]|cl[ea]|fere|gg|p[ios]|rou|tt)", "an"], # y like "i": an yclept, a year
    ["", "a"]                                         # guess "a"

]

def article(word):
    for rule in article_rules:
        pattern, article = rule
        if re.search(pattern, word) is not None:
            return article

sentence = "I am a uncle. I ate the apple in a morning."

puncts = ['.', '!', ',', ';', '"', "'", '(', ')', '-', '[', ']', '{', '}', '?', '/', ':', '@', '&']

for i in puncts:
    sentence = sentence.replace(i, ' '+i+' ')

WORDS = sentence.split()

for i in range(len(WORDS)):
    if WORDS[i] == 'a' or WORDS[i] == 'an' or WORDS[i] == 'the':
        art = article(WORDS[i+1])
        q = "https://api.datamuse.com/words?sp="
        response = requests.get(q+art+"&rc="+WORDS[i+1])
        f1 = response.json()[0]["score"]
        response = requests.get(q+"the&rc="+WORDS[i+1])
        f2 = response.json()[0]["score"]
        #print(i+1," ",f1," ",f2)
        if(f2 > 4*f1):
            best = "the"
            out = [best, art]
        else:
            best = art
            out = [best, "the"]
        if(best != WORDS[i]):
            print([i+1,WORDS[i],out])
