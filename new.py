import requests
city = input("City: ")
res = requests.get(f"http://wttr.in/{city}?format=3")
print(res.text)
