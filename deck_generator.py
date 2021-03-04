"""
Learning Deck Generator 
@TODO: add Practice Deck Generators
"""
import logging
logger = logging.getLogger()

#own module
from FlashCards import flash_card_deck


def number_bound(min_total=10,max_total=100):
    """ generates number bound with sums
    between min_total and max_total
    """
    logger.debug("creating 20+20")
    summs_deck = flash_card_deck()
    print("test",summs_deck) 
    for i in range(min_total, max_total +1):
        for j in range(min_total, max_total +1):
            if (i+j)>min_total and (i+j)<max_total:
                summs_deck.add_q_n_a("%s + %s"%(i,j),"%s"%(i+j),15)
    return summs_deck

def summ_tables(add=20,summ=20):
    logger.debug("creating 20+20")
    summs_deck = flash_card_deck()
    print("test",summs_deck) 
    for i in range(1, add +1):
        for j in range(1, summ +1):
            summs_deck.add_q_n_a("%s + %s"%(i,j),"%s"%(i+j),15)
    return summs_deck

def add_mult_tables(mul=6,mult=6,previous_deck=None):
    """ creates or add new tables Q&A """
    if not previous_deck:
        previous_deck = flash_card_deck()
    for i in range(1,mul+1):
        for j in range(1,mul+1):
            previous_deck.add_q_n_a("%s · %s"%(i,j),"%s"%(i*j),10)
    return previous_deck

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

if __name__=="__main__":
    logger.setLevel(logging.DEBUG)
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("TEST DEBUG")

    deck = number_bound()
    deck.set_fn("number_bound_10_100.json")
    deck.set_shuffled()
    deck.save_hdd()

    deck = number_bound(1,20)
    deck.set_fn("number_bound_1_20.json")
    deck.set_shuffled()
    deck.save_hdd()