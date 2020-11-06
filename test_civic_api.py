import requests, json

url = "https://www.googleapis.com/civicinfo/v2/representatives"  # Base URL for all our API calls

querystring = {"key":"AIzaSyB4-zXa4A6ltGlHFpRq_ofDIJZnY0QlwKo",  # API key I setup in the Google Developer's Console
               "address":"4110 W Franklin st, Richmond, VA",  # Sample Address
               "includeOffices": "true",  # Includes offices in addition to officials, can set false
               "levels":"country",  # Sample level of government
               "roles":"executiveCouncil"  # Sample role at the given level to query
               }

response = requests.request("GET", url, params=querystring)  # Performs a GET at our base URL with the defined
                                                             # querystring

json_data = response.json()  # Converts the response object to a python dictionary

# print(json_data['officials'][0]['urls']) <-- When looking at what the print statement below outputs, this should give:
#  ['https://kaine.senate.gov/']
# we can also use print(type(json_data['officials'])) or similar to discern the type of object the data we want is
# stored in, so we know how to access it

print(json_data)#['officials'][0]['channels'])


