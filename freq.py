import sys
import requests
import urllib
def phraseScore(phrase):

	encoded_query = urllib.parse.quote(phrase)
	params = {'corpus': 'eng-gb', 'query': encoded_query}
	params = '&'.join('{}={}'.format(name, value) for name, value in params.items())

	response = requests.get('https://api.phrasefinder.io/search?' + params)
	assert response.status_code == 200

	if len(response.json()["phrases"]) == 0:
		ans = 0
	else:
		ans = response.json()["phrases"][0]["mc"]

	return ans

