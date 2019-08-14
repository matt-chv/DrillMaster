from flask import Flask, jsonify, render_template, request, send_from_directory
import time
import json
from random import choice
from os.path import abspath,join,dirname
import logging

# root_folder = abspath(dirname(__file__))
# root_folder = "c:/Perso/jquery.flashcards/"
# print(root_folder)
app = Flask(__name__, static_url_path='/static/')

cards_pdf = {} #card probability density function

def get_next_card(cards_pdf, card_index):
    """
    Parameters:
    -----------
    cards_pdf: dict of list
    Rerturn:
    --------
    next_index: int
    the index of the next card to be displayed
    """
    algo_version = 1
    print(algo_version)
    if algo_version ==0:
        next_index =  (card_index+1)%5
    elif algo_version==1:
        #make a list of all cards such as they have equal probability
        #each card has probability being drawn ~1/(average scores)
        sum_all_scores = 0
        for i in range(len(cards_pdf)):
            sum_all_scores+=sum(cards_pdf[i])
        equal_prob_list = []
        for i in range(len(cards_pdf)):
            #here the multiplier int(summ_all_scores)/sum(cards_pdf[i])
            #is an approximation, more accurately should be a compute of all prime dividers and scaling
            #not done yet and probably never
            equal_prob_list+=[i]*int((sum_all_scores/sum(cards_pdf[i])))
        next_index=choice(equal_prob_list)
    return(next_index)
            
@app.route("/api/mnemo")
def randomize():
    card_index = int(request.args.get('card_index', 0))
    assesment_level = int(request.args.get('assesment_level', 0))
    cards_pdf[card_index].append(assesment_level)
    card_index = get_next_card(cards_pdf,card_index)
    logging.debug(cards_pdf)
    return jsonify({
        "next_card_index"        :  (card_index),
    })

@app.route("/api/lessons")
def get_lesson():
    """
    Parameters:
    cards: str
        name of the cards to be loaded - in the cards folder
    Return:
    -------
    lessons: json
    json string (utf-8) containing front / back and hints for the flashcard
    """ 
    lessons = request.args.get('cards',0)
    print("mcv 67",lessons)
    cards_fp ="C:/Perso/flashcards/static/cards/%s.json"%(lessons) 
    print("mcv 69",cards_fp)
    fp = abspath(join('/static','cards',"%s.js"%(lessons)))
    with open(cards_fp,'r', encoding='utf-8') as fi:
        json_cards = json.load(fi)
    for i in range(len(json_cards["cards"])):
        cards_pdf[i]=[1]
    print("mcv lessons length",i)
    print("mcv 76",json_cards["cards"])
    return jsonify({
        "lessons"        :  json_cards["cards"],
    })

@app.route('/api/learn')
def send_learn():
    """
    Parameters:
    -----------
    Return:
    -------
    Example:
    --------
    GET http://127.0.0.1:5000/api/learn?cards=hsk1
    """
    print("test mcv 78")
    lessons = request.args.get('cards',0)
    print("mcv 92",lessons)
    return render_template('learn.html', learn_card=lessons)

@app.route('/cards/<path:path>')
def send_cards_js(path):
    return send_from_directory('static/cards', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static',
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    app.run(debug=True)