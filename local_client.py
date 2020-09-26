import requests

base_url = "http://localhost:5005/"

deck_url = base_url + "deck?id=%s"

print("deck 4")
r=requests.get(deck_url%4)
print(r.content)
print("\n\ndeck 5")
r=requests.get(deck_url%5)
print(r.content)
r=requests.get(deck_url%1)
print(r.content)

