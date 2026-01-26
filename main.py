'''
curl -X 'POST' \
  'http://185.185.143.231:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "string",
  "email": "string",
  "password": "string"
}'

curl -X 'PUT' \
  'http://185.185.143.231:5051/v1/account/5b010d18-36f9-433b-9898-8c3bb7c18835' \
  -H 'accept: text/plain'

'''
import pprint
import requests

# url = 'http://185.185.143.231:5051/v1/account'
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json'
# }
#
# json = {
#     "login": "bhs-test2",
#     "email": "bhs-test@test2",
#     "password": "123456789"
# }
#
# response = requests.post(
#     url=url,
#     headers=headers,
#     json=json
# )

url = 'http://185.185.143.231:5051/v1/account/5b010d18-36f9-433b-9898-8c3bb7c18841'
headers = {
    'accept': 'text/plain'
}



response = requests.put(
    url=url,
    headers=headers,
)


print(response.status_code)
pprint.pprint(response.json())

response_json = response.json()

print(response_json['resource']['rating']['quantity'])