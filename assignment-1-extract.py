
import requests

endpoint = 'https://www.loc.gov/free-to-use'
parameters = {
    'fo' : 'json'
    }

collection = 'libraries'

collection_list_response = requests.get(endpoint + '/' + collection, params=parameters)

collection_list_response.url

collection_json = collection_list_response.json()
