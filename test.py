import sys, os
import requests

url = 'https://file.io/'
data = {
    "file": open(sys.argv[1], "rb"),
    "maxDownloads": 100,
    "autoDelete": True
}
response = requests.post(url, files=data)
res = response.json()
print(res)
print(res["link"])
