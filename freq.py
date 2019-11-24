import sys
import requests
import urllib


# q = "https://api.datamuse.com/words?md=f&sp="+sys.argv[2]
# q = q + '&lc=' + sys.argv[1]
# q = q + '&rc=' + sys.argv[3]

# response = requests.get(q)


phrase = sys.argv[1] + ' ' + sys.argv[2] + ' ' + sys.argv[3]

encoded_query = urllib.parse.quote(phrase)
params = {'corpus': 'eng-gb', 'query': encoded_query}
params = '&'.join('{}={}'.format(name, value) for name, value in params.items())

response = requests.get('https://api.phrasefinder.io/search?' + params)
assert response.status_code == 200

if len(response.json()["phrases"]) > 0:
	freq = response.json()["phrases"][0]["mc"]
else:
	freq = 0

print(freq)