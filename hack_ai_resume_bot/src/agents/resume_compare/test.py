import requests
import json

url = "https://api.coresignal.com/cdapi/v1/linkedin/job/search/filter"

payload = json.dumps({
  "title": "Java Developer",
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer eyJhbGciOiJFZERTQSIsImtpZCI6IjE4MmE3MDM1LWRmN2EtYzdkOS04MGQwLTljOThjZjFlYTA5OCJ9.eyJhdWQiOiJzcGl0IiwiZXhwIjoxNzM1MjM0MjgxLCJpYXQiOjE3MDM2NzczMjksImlzcyI6Imh0dHBzOi8vb3BzLmNvcmVzaWduYWwuY29tOjgzMDAvdjEvaWRlbnRpdHkvb2lkYyIsIm5hbWVzcGFjZSI6InJvb3QiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzcGl0Iiwic3ViIjoiZmEwYzRjOWMtYzIxYy1mZmRmLWMwYjktNDhhZWQ1YWY5YzE2IiwidXNlcmluZm8iOnsic2NvcGVzIjoiY2RhcGkifX0.N13pF6Lh4EZSK9dYknUIl6aZTjHEiynhvuTWIKa_xhNSU9SN0_kYqHH4lXRjDlpCKkUrVZ09JFbPswG3Y_I5BA'
}

response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)

print(json.loads(response.text)[0])

# scheduler seed agent1qwge5z5m6ghkm35sum22zeuv7q37nv7yj5cw7n2l8k2zd44e8n5njmez40r