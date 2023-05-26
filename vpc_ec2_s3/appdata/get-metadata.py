import requests

response = requests.get("http://169.254.169.254/latest/meta-data")
print(r.text.split("\n"))