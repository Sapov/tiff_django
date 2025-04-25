import requests
import json

url = "https://enter.tochka.com/uapi/invoice/v1.0/bills/300000092/1cf95c4f-e794-4407-bac4-0829f19bd2be/email"

payload = json.dumps({
  "Data": {
    "email": "user@example.com"
  }
})
headers = {
  'Authorization': 'Bearer <token>',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
