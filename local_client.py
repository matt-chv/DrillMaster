import requests
from sys import argv

base_url_dev = "http://localhost:5005"
base_url_prod = "https://drillmaster.xyz"


def get_decks(base_url=base_url_dev):
  deck_url = base_url + "/deck?id=%s"
  print(deck_url)
  user_ids = [4]
  for uid in user_ids:
    r=requests.get(deck_url%uid)
    print(r.content[:200])


def push_answers():
  deck_url = base_url + "deck?id=%s"
  json_deck = [{"question":"1 + 1","answer":"2","number_attempts":"0","timestamp":"1601404033687","timer":"11"},{"question":"6 · 8","answer":"48","number_attempts":"0","timestamp":"1601404036654","timer":"12"},{"question":"√ 10 ≅ (1 digit) ","answer":"3","number_attempts":"0","timestamp":"1601404039688","timer":"12"}]

  r = requests.post(deck_url,json=json_deck,headers = {'Content-type': 'application/json'})
  print(r.content)

if __name__=="__main__":
  server_url = base_url_dev
  if argv[1]=="prod":
    server_url = base_url_prod
  get_decks(server_url)
  print(argv)
  #push_answers()
