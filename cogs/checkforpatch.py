import requests
import re

version=None
url = 'http://api.kongor.online/patcher/patcher.php'
payload = {
    'latest' : '',
    'os': 'was-crIac6LASwoafrl8FrOa',
    'arch' : 'x86_64'
    }
x = requests.post(url,data=payload)
data=x.text
data=re.split(';s:\d+:',data)

for i in range(len(data)):
    if '"latest_version"' in data[i]:
        version=data[i+1]

if version != None:
    print(version)