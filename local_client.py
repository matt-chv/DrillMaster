import requests

base_url = "http://localhost:5005/"

def get_decks():
  deck_url = base_url + "deck?id=%s"

  print("deck 4")
  r=requests.get(deck_url%4)
  print(r.content)
  print("\n\ndeck 5")
  r=requests.get(deck_url%5)
  print(r.content)
  r=requests.get(deck_url%1)
  print(r.content)

def push_answers():
  deck_url = base_url + "deck?id=%s"
  json_deck = [{"question":"1 + 1","answer":"2","number_attempts":"0","timestamp":"1601404033687","timer":"11"},{"question":"6 · 8","answer":"48","number_attempts":"0","timestamp":"1601404036654","timer":"12"},{"question":"√ 10 ≅ (1 digit) ","answer":"3","number_attempts":"0","timestamp":"1601404039688","timer":"12"}]

  r = requests.post(deck_url,json=json_deck,headers = {'Content-type': 'application/json'})
  print(r.content)

push_answers()
