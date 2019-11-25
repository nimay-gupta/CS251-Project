from django.shortcuts import render
import requests
import sys
from subprocess import run, PIPE
from django.http import JsonResponse
# import pyth.grammar
import rewrite
# import pyth.spell
import json


def home(request):
	return render(request, '/Users/bhaskar/Desktop/Project/mysite/templates/abc.html')

def answer_me(request):
    field = request.GET.get('inputValue')
    a1 = rewrite.main(field)
    print(a1)
    # a2=pyth.spell.outp(field)
    # print(a2)
    # a3=pyth.grammar.outp(field)
    # print(a3)

    ans={}
    for k in ans1.keys():
    	if(len(ans1[k])!=0):
    		ans[k]=["green"]
    		ans[k]+=ans1[k]
    	else:
    		ans[k]=[]
    # for k in ans2.keys():
    # 	if(len(ans3[k])!=0):
    # 		ans[k]=["blue"]
    # 		ans[k]+=ans3[k]
    # 	elif(len(ans2[k])!=0):
    # 		ans[k]=["red"]
    # 		ans[k]+=ans2[k]
    # 	elif(len(ans1[k])!=0):
    # 		ans[k]=["green"]
    # 		ans[k]+=ans1[k]
    # 	else:
    # 		ans[k]=[]
    print(ans) 
    
    return JsonResponse(answer)