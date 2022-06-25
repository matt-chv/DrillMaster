"""
v0.1: shows cards, talks back, checks answers
v0.2: talks back to cards back-end
"""

#import standard modules
import logging
from os.path import abspath, exists, join, pardir
from os import environ
from urllib.parse import unquote

#import pip modules
from flask import Flask, json, request, Response, send_from_directory, render_template

#import own
from FlashCards import load_deck
from db import init_db, upgrade_db, view_users_activities_log, update_logs, get_df_db

if 'FLASK_ENV' in environ:
  if environ['FLASK_ENV'] == 'prod':
    app_data_folder = "/var/www/DrillMaster/DrillMaster/"
    deck_path = join(app_data_folder,"decks")
  else:
    app_data_folder = abspath(join(__file__,pardir))
    deck_path = join(app_data_folder,"decks")
else:
    app_data_folder = "/var/www/DrillMaster/DrillMaster/"
    deck_path = join(app_data_folder,"decks")
    logging.error("MISSING FLASK_ENV for proper operation")

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG)
#note important to keep encoding utf-8 to log request with cards
#content in utf-8 format
handler = logging.FileHandler(join(app_data_folder,"debug.log"), encoding='utf-8')
formatter = logging.Formatter('%(name)s %(message)s')
handler.setFormatter(formatter) # Pass handler as a parameter, not assign
root_logger.addHandler(handler)


students = [{"id": '0', "name": "demo", "deck":"demo.json"},
            {"id": '4', "name": "elodie","deck":"Elodie.json"},
           {"id": '5', "name": "camille", "deck":"number_bound_10_100.json"},
          {"id": '6', "name": "Anthony", "deck":"number_bound_1_20.json"}    
          ]

api = Flask(__name__,static_url_path='/static')

api.config["APPLICATION_ROOT"] = "/drillmaster"


@api.route('/students', methods=['GET'])
def get_students():
  return json.dumps(students)


@api.route("/answer", methods=['POST'])
def post_answers():
  user_id = request.args.get('id')
  myjson = request.json
  root_logger.debug("entering answer")
  logging.debug("received json: %s",json.dumps(myjson))
  
  deck = None
  for user in students:
    root_logger.debug("user: %s---%s",user["id"],user_id)
    if user["id"]==user_id:
      deck=user["deck"]
  
  if deck is None:
    deck="demo.json"
    user_id="0"
  
  root_logger.info("request method: %s",request.method)
  root_logger.info("request json : %s",request.json)
  res =load_deck(deck,None,root_folder=deck_path)

  for card in myjson:
    for key in card:
      logging.debug("debug received card: %s",card[key])
    res.update_card(card["question"],float(card["timer"]),card["answer"],card["number_attempts"], card["timestamp"])
    res.save_hdd()
  update_logs(user_id,myjson,res)
  qs = []
  for i in range(10):
    qs.append(res.next_q())
  deck = {}
  for q in qs:
    logging.debug("POST - adding q: %s",q)
    deck[q]=res.json[q]
  return json.dumps(deck)


@api.route("/deck", methods=['GET'])
def get_deck():
  user_id = request.args.get('id')
  deck = None
  root_logger.debug("hello student id: %s", user_id)
  for user in students:
    if user["id"]==user_id:
      deck=user["deck"]
  if deck is None:
    deck="demo.json"
    user_id="0"
  
  
  root_logger.info("request method: %s",request.method)
  root_logger.info("request json : %s",request.json)
  res =load_deck(deck,None,root_folder=deck_path)
  
  #res =load_deck("Elodie.json",None,"/var/www/FlaskApp/FlaskApp/")
  if request.method == 'GET':
    if not res.shuffled:
      res.shuffle_cards()
    qs = res.shuffled
    deck = {}
    for q in qs:
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
  #logging.debug("submitted deck: %s",json.dumps(deck))
  return json.dumps(deck)

@api.route("/log")
def logs():
  df = get_df_db("SELECT * FROM HISTORY")
  records = df.to_dict('records')
  columns = df.columns
  return render_template('record.html', records=records, colnames=columns)

@api.route('/educator')
def educator():
  df = view_users_activities_log()
  records = df.to_dict('records')
  columns = df.columns
  return render_template('record.html', records=records, colnames=columns)
  #return df.to_html()

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

@api.route('/<path:filename>')
def manifest(filename):
  if filename=="manifest.json":
    root_logger.info("returning manifest.json")
    if exists(join("/var/www/DrillMaster/DrillMaster","manifest.json")):
      root_logger.info("manifest exists")
    else:
      root_logger.info("manifest does not exists")
    return send_from_directory("/var/www/DrillMaster/DrillMaster","manifest.json")
  elif filename=="sw.js":
    return send_from_directory("/var/www/DrillMaster/DrillMaster","sw.js")

@api.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@api.cli.command('upgradedb')
def initdb_command():
    """Upgrades the database."""
    upgrade_db()
    print('Upgrade the database.')

if __name__ == '__main__':
  logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
  root_logger.setLevel(logging.DEBUG)
  consoleHandler = logging.StreamHandler()
  consoleHandler.setFormatter(logFormatter)
  root_logger.addHandler(consoleHandler) 
  api.run(debug=True, port=5005)
