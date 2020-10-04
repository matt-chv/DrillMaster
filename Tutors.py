""" wrapper to create / update existing decks with new content 

Usage:
-----

deck = flash_card_deck("/var/www/DrillMaster/DrillMaster/Anthony.deck")
deck = summ_tables(5,5,deck)

"""

import logging
import random

from FlashCards import flash_card_deck

def update_deck(deck, generator):
  pass

def add_div_tables(previous_deck=None,mul=10,mult=10):
  """ create or add new divisions to deck """
  if not previous_deck:
    previous_deck = flash_card_deck()
  qna = []
  for i in range(1,mul+1):
    for j in range(1,mul+1):
      qna.append(("%s ÷ %s"%(i*j,j),"%s"%(i)))
  random.shuffle(qna)
  for q,a in qna:
    previous_deck.add_q_n_a(q,a,10)
  return previous_deck

def summ_tables(deck=None,add=5,summ=5):
  logger.debug("creating summs tables")
  qna = []
  for i in range(1, add +1):
    for j in range(1, summ +1):
      qna.append(("%s + %s"%(i,j),"%s"%(i+j)))
  random.shuffle(qna)
  for q,a in qna:
    deck.add_q_n_a(q,a,15)
  print(deck)
  return deck

logger = logging.getLogger()

if __name__=="__main__":
  logger.debug("MAIN")
  deck = flash_card_deck("/var/www/DrillMaster/DrillMaster/Anthony.json")
  print(10,deck.json)
  deck = summ_tables(deck,5,5)
  print(deck)
  print(deck.json)
  deck.save_hdd()
