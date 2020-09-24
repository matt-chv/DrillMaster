"""
v0.1: shows cards, talks back, checks answers
v0.2: talks back to cars back-end
"""

#import standard modules
import logging
from urllib.parse import unquote

#import pip modules

from flask import Flask, json, request, Response

#import own
from FlashCards import load_deck


root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('/var/www/DrillMaster/DrillMaster/debug.log', encoding='utf-8')
formatter = logging.Formatter('%(name)s %(message)s')
handler.setFormatter(formatter) # Pass handler as a parameter, not assign
root_logger.addHandler(handler)


students = [{"id": "4", "name": "elodie"}, {"id": "5", "name": "camille"}]

api = Flask(__name__,static_url_path='/static')

api.config["APPLICATION_ROOT"] = "/drillmaster"


@api.route('/students', methods=['GET'])
def get_students():
  return json.dumps(students)

@api.route("/deck", methods=['GET','POST'])
def get_deck():
  logging.info("request method: %s",request.method)
  logging.info("request json : %s",request.json)
  res =load_deck("Elodie.json",None,"/var/www/FlaskApp/FlaskApp/")
  
  res =load_deck("Elodie.json",None,"/var/www/FlaskApp/FlaskApp/")
  if request.method == 'GET':
  
    if not res.shuffled:
      res.shuffle_cards()
    qs = res.shuffled
    deck = {}
    for q in qs:
      logging.debug("GET -adding q: %s",q)
      deck[q]=res.json[q]
  elif request.method == 'POST':
    myjson = request.json
    logging.debug("received json: %s",json.dumps(myjson))
    for card in myjson:
      for key in card:
        logging.debug("debug received card: %s",card[key])
      res.update_card(card["question"],float(card["timer"]),card["answer"],card["number_attempts"], card["timestamp"])
      res.save_hdd()
    qs = []
    for i in range(10):
      qs.append(res.next_q())
    deck = {}
    for q in qs:
      logging.debug("POST - adding q: %s",q)
      deck[q]=res.json[q] 
  logging.debug("request: %s",request.method) 
  logging.debug("submitted deck: %s",json.dumps(deck))
  return json.dumps(deck)

@api.route('/student')
def student():
  args = request.args
  id = args['id']
  for s in students:
    if s["id"]==id:
      name = s["name"]
    return api.send_static_file('cards.html')

@api.route('/favicon.ico')
def favicon():
	return api.send_static_file("favicon.ico")

@api.route("/drillmaster/")
@api.route('/')
@api.route('/index')
def index():
    return api.send_static_file('index.html')
    #return index_html

if __name__ == '__main__':
    api.run(debug=True, port=5005)
