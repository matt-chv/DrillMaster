from flask import Flask, jsonify, render_template, request, send_from_directory
import time
from random import choice
from os.path import abspath,join,dirname
import logging

# root_folder = abspath(dirname(__file__))
# root_folder = "c:/Perso/jquery.flashcards/"
# print(root_folder)
app = Flask(__name__, static_url_path='/static/')

cards_pdf = {} #card probability density function
for i in range(5):
    cards_pdf[i]=[1]

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
        logging.debug(equal_prob_list)
        next_index=choice(equal_prob_list)
    return(next_index)
            

# @app.route("/")
# def main():
#     return render_template('main.html', reload = time.time())

# @app.route("/api/info")
# def api_info():
#     info = {
#        "ip" : "127.0.0.1",
#        "hostname" : "everest",
#        "description" : "Main server",
#        "load" : [ 3.21, 7, 14 ]
#     }
#     return jsonify(info)

@app.route("/api/mnemo")
def randomize():
    card_index = int(request.args.get('card_index', 0))
    assesment_level = int(request.args.get('assesment_level', 0))
    cards_pdf[card_index].append(assesment_level)
    print(cards_pdf)
    card_index = get_next_card(cards_pdf,card_index)
    logging.debug(cards_pdf)
    return jsonify({
        "next_card_index"        :  (card_index),
    })

@app.route('/cards/<path:path>')
def send_cards_js(path):
    print(70,"mcv",path)
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
    logging.debug("debug")
    logging.info("info")
    logging.warning("alert")
    app.run(debug=True)