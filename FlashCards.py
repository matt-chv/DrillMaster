"""
This is a python prototype for a SRS based math 
v0.1a: first run for with mult tables and first compute of due time
v0.1b: added \a in the msg_try_again to add a system beep when failing
v0.1c: adding argparse
v0.2: moving to MVC
NEXT: 
create client class to prepare for web server / client architecture
"""

from datetime import datetime as dt
from datetime import timedelta
import json
import logging
from os.path import expanduser, exists, join
import random
import sys
import select
import time
import tty
import termios

EXCEPTION_ESCAPED = "ESC pressed"
msg_bravo = "bravo     "
msg_try_again = "try again    \a"
ISO8601 = "%Y-%m-%dT%H:%M:%S"

demo_json = {  "1 + 1": "2",
  "6 \u00b7 8": "48",
  "\u221A 10 \u2245 (1 digit) ": "3"
}

class flash_card_deck:
    fn = None
    this_session_good = 0
    this_session_bad = 0
    shuffled = []
    def __init__(self,fp=None):
        logger.info("INIT DECK")
        print("INIT DECK")
        if fp:
            self.fn = fp
            log_msg = "loading %s deck from file"%(fp)
            logging.info(log_msg)
            if exists(fp):
                with open(fp) as json_file:
                    self.json = json.load(json_file)
            self.set_fn(fp)
            self.fn = join(fp)
        else:
            log_msg = "creating empty deck: %s"%(fp)
            logger.error(log_msg)

            self.json = {}
        
    def add_q_n_a(self,q,a,timeout):
        """ add a question q to the list of questions """
        if q in self.json:
            if self.json[q]["answer"]==a:
                pass
            else:
                raise Exception(ValueError,"different answer given for q=%s"%(q))
        else:
            self.json[q]={}
            self.json[q]["answer"]=a
            self.json[q]["count_good"]=0
            self.json[q]["count_bad"]=0
            self.json[q]["timeout"]=timeout
            self.json[q]["due"]="1970-01-01T00:00:00"
            self.json[q]["successful_repetitions"]=0
            self.json[q]["interval_s"]=1
            self.json[q]["ease_factor"]=1.3
    def increment_good (self,q):
        self.json[q]["count_good"]+=1
        self.json[q]["successful_repetitions"]+=1
        self.this_session_good+=1
    def increment_bad (self,q):
        self.json[q]["count_bad"]+=1
        self.json[q]["successful_repetitions"]=0
        self.this_session_bad+=1
    def save_hdd(self):
        if self.fn:
            logging.debug("saving to file: %s",self.fn)
            print("saving file")
            with open(self.fn, 'w') as json_file:
                json.dump(self.json, json_file, indent=2)
        else:
            logging.error("no file path to save file")

    def serialize(self):
        return json.dumps(self.json, indent=4, ensure_ascii=False)
    def set_fn(self,fn):
        self.fn = join(expanduser("~"),fn)
    def update_deck(self,answers):
      """ answers: list
         list of answer
         answer: q, timestamp, answer, ok/nok, delta_time, number_attemps
      """
      for a in answers:
        self.update_card(q,delta_time, a, number_attemps, timestamp)

    def update_card(self, q, time_question, typed_input, number_attempts,timestamp=None):
        """
        time_question: 
        """
        time_question = float(time_question)
        logging.debug("time question: %.2g",time_question)
        
        number_attempts = float(number_attempts)
        logging.debug("number attemps: %s",number_attempts)

        if not (q in self.json):
          print("************ Q NOT IN JSON ********")
        log_msg = "update_deck _SRS : %s"%(q)
        logging.info(log_msg)
        message = msg_bravo
        quality = None
        if self.json[q]["answer"]== typed_input:
            logging.info("%s good answer: %s",q, typed_input)
            self.increment_good(q)

            
            if number_attempts == 0:
                #if the countdown is greater than half of the countdown reset value
                #the answer was quick so good quality
                if time_question >= self.json[q]["timeout"]*3/4:
                    quality = 5
                elif time_question >= self.json[q]["timeout"]/2:
                    quality = 4
                else:
                    quality = 3
            elif number_attempts == 1:
                    quality = 2 #2 - incorrect response; where the correct one seemed easy to recall
            elif number_attempts ==2:
                quality = 1 #1 - incorrect response; the correct one remembered
        else:
            logging.info("bad answer")
            self.increment_bad(q)
            message = msg_try_again
            if number_attempts >= 3:
                quality = 0 #0 - complete blackout.

        if quality:
            #only update if we have defined quality - not defined when a few fails but less than 3
            successful_repetitions = self.json[q]["successful_repetitions"]
            interval_s = self.json[q]["interval_s"]
            ease_factor = self.json[q]["ease_factor"]
            
            interval_s , ease_factor = self.spaced_repetition(quality, interval_s, successful_repetitions, ease_factor)
            try:
                due = dt.strftime(dt.now() + timedelta(seconds=interval_s),ISO8601)
                logging.debug("now: %s",dt.now())
                self.json[q]["due"]=due #dt.strftime(dt.now() + timedelta(seconds=interval_s),ISO8601)
            
                log_msg = "question: %s - new interval_s: %s - new due: %s"%(q,interval_s,due)
                logging.info(log_msg)
            except OverflowError:
                logging.error("time overflow")
                logging.error("now: %s",dt.now())
                logging.error("timdelta_s: %s",interval_s)
                logging.error("timedelta_Y: %s",interval_s/3e7)
                print("error time overflow")
                print("now",dt.now())
                print("timedelta_s",interval_s)
            self.json[q]["ease_factor"] =ease_factor
            self.json[q]["interval_s"] =interval_s
            log_msg = "update done for : %s, new due: %s"%(q, self.json[q]["due"])
            logging.info(log_msg)
        else:
          log_msg = "quality for %s, should be ok but is: %s"%(q,quality)
          logging.debug(log_msg)
        
        return message
    def next_q(self):
        if not self.shuffled:
            self.shuffle_cards()
        next = self.shuffled.pop(0)
        return next

    def spaced_repetition(self,quality,interval_s,successful_repetitions,ease_factor,algo="mSM2"):
        """
        Parameters:
        -----------
        quality: 
            SM2: integer - user / student feedback: 0..5
                5 - perfect response
                4 - correct response after a hesitation
                3 - correct response recalled with serious difficulty
                2 - incorrect response; where the correct one seemed easy to recall
                1 - incorrect response; the correct one remembered
                0 - complete blackout.
            mSM2: float - SW computed based on correct answer and time needed.
        interval:
            SM2: inter-repetition interval after the n-th successful_repetitions (in days)
                    I(1):=1 ; I(2):=6; for n>2 I(n):=I(n-1)*EF
            mSM2: inter-repetition interval after the n-th successful_repetitions (in seconds)
        successful_repetitions:
            SM2: integer number of successful repetition
            mSM2: 
        ease_factor:
            SM2: float >=1.3, 
            mSM2: 
        Return:
        -------
        interval:
        
        successful_repetitions:

        ease_factor: EF':=f(EF,q)
            EF':=EF-0.8+0.28*q-0.02*q*q 
            Notes:
                EF' = EF for q=4
                EF_n = EF_(n-1)-0.8 = EF_1 - (0.8)*n (if always = 0) - SM2 limits this to 1.3

        """

        SM2_interval_to_mSM2_interval = 86400 # 84600 = 24 * 60 * 60


        if algo=="SM2":
            ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

            if ease_factor < 1.3:
                ease_factor = 1.3

            if successful_repetitions==0:
                interval_s = 1 * SM2_interval_to_mSM2_interval
            elif successful_repetitions==1:
                interval_s = 6 * SM2_interval_to_mSM2_interval
            else:
                interval_s = interval_s * ease_factor

        elif algo == "mSM2":
            ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            
            if ease_factor < 0.1:
                ease_factor = 0.1

            if successful_repetitions == 0:
                interval_s = 1 * SM2_interval_to_mSM2_interval
            elif successful_repetitions == 1:
                interval_s = 6 * SM2_interval_to_mSM2_interval
            else:
                interval_s = interval_s * ease_factor

            if interval_s < 1:
                interval_s = 1

        return interval_s, ease_factor

    def set_shuffled(self,questions=None, repetition = 1):
        """ call this function to force the list of questions to be studied first 
        This can be useful when tutor wants to ensure special set of questions is studied first
        works like a manual over-ride
        Parameters:
        -----------
        questions: list of str
            should be a list of keys existing in the self.json - no checks done !
        repetition: int
            number of time the list of questions needs to be asked (the list will be shuffled once extended)
        Returns:
        --------
        None
        Sets:
        -----
        self.shuffled
        """
        print("pre-set questions")
        if not questions:
            questions = ["%s · %s"%i for i in [(4,4),(4,5),(4,6),(6,5),(6,4),(5,3),(5,4)]]
            repetition = 3
        questions *= repetition
        random.shuffle(questions)
        self.shuffled = questions
            

    def shuffle_cards(self):
        """
        Returns: None
        Set: self.shuffled: list of str 
        """
        algo = "shuffling" #just taking them all at random
        algo = "bad_first_then_shuffle"
        if algo == "shuffling":
            shufled = [q for q in self.json]
            random.shuffle(shufled)
            self.shuffled = shufled
        else:
            self.unknown_deck = []
            self.bad_deck = []
            self.good_deck = []

            for q in self.json:
                if self.json[q]["count_good"]==0 and self.json[q]["count_bad"]==0:
                    self.unknown_deck.append(q)
                elif self.json[q]["count_good"] < self.json[q]["count_bad"]:
                    self.bad_deck.append((q,self.json[q]["count_good"] , self.json[q]["count_bad"]))
                elif dt.strptime(self.json[q]["due"], ISO8601) <= dt.now():
                    self.good_deck.append((q))
                else:
                    pass
            
            """start with revising - to ensure not forgotten (apply here SM2 or similar)
            then with bad deck - to ensure they are learned
            then unknown deck
            !!! report if more time needed to do all revising"""

            if self.good_deck:
                log_msg = "going over the good ones needing revising",len(self.good_deck)
                #print(log_msg)
                logging.info(log_msg)
                
                shuffled = self.good_deck[:5]
                random.shuffle(shuffled)
                self.shuffled=shuffled


            elif self.bad_deck:
                log_msg = "shuffling bad deck"
                logging.info(log_msg)

                self.bad_deck.sort(key = lambda x: (x[1]/(x[1]+x[2]), x[1]+x[2]))
                shuffled = [q[0] for q in self.bad_deck[:5]]
                random.shuffle(shuffled)
                self.shuffled = shuffled+shuffled+shuffled
            elif self.unknown_deck:
                log_msg = "shuffling unknown deck"
                logging.info(log_msg)

                shufled = self.unknown_deck.copy()
                random.shuffle(shufled)
                self.shuffled = shufled   
            else:
                log_msg = "random draw for drilling"
                logging.info(log_msg)

                shufled = [q for q in self.json]
                random.shuffle(shufled)
                self.shuffled = shufled[:5]

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

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



def deck_from_json(json_demo_deck=demo_json):
  new_deck = flash_card_deck()
  for v in json_demo_deck:
    new_deck.add_q_n_a(v, json_demo_deck[v],15)
  return new_deck
    
def timed_input(buffer = "", timeout = 10):

    result = buffer
    time_spent = 0
    s_steps = 0.05
    s = 0
    count_down = int(timeout/s_steps)
    show_countdown = False
    crlf_pressed = False

    for remaining in range(count_down, 0, -1):
        if show_countdown:
            sys.stdout.write("\r%2d seconds remaining, answer: %s"%(int(remaining*s_steps), result)) 
        else:
            sys.stdout.write("\r%s    "%(result)) 
        sys.stdout.flush()
        
        time.sleep(s_steps)
        s += s_steps
        time_spent +=s_steps
        if s >=1/s_steps:
            s -=1/s_steps
            sys.stdout.write("\r")
            sys.stdout.write("\r%s    "%(result)) 
            
            sys.stdout.flush()
        
        if isData():
            c = sys.stdin.read(1)
            if c == '\x1b':         # x1b is ESC
                raise Exception(EXCEPTION_ESCAPED)
            elif ord(c) == 10 or ord(c)==13:
                crlf_pressed = True
                break
            elif ord(c) == 127:
                #backspace
                result = result[:-1]
            else:
                result +=c
    return(result, crlf_pressed, time_spent)

def show_flash_cards(flash_cards,total_time_s):

    total_time = 0
    escaped = False
    if not flash_cards.shuffled:
        # if the list of questions has not be set, then generate it
        flash_cards.shuffle_cards()
        
    while total_time < total_time_s:
        q = flash_cards.next_q()
        typed_input=""
        res = ""
        time_question = 0 
        number_attempts = 0
        while (res!= msg_bravo):
            print(q)
            try:
                typed_input, crlf_pressed, time_spent = timed_input(typed_input, timeout = flash_cards.json[q]["timeout"])
            except Exception as e:
                if str(e)== EXCEPTION_ESCAPED:
                    escaped = True
                    break
            else:
                total_time += time_spent
                time_question += time_spent
                
                if crlf_pressed:
                    res = flash_cards.update_card(q,time_question,typed_input, number_attempts)
                    typed_input = ""
                    if res==msg_bravo:
                        time_question = 0
                else: 
                    res = msg_try_again

                """ res = update_flash_cards(result, flash_cards,q)
                if result== flash_cards[q]:
                    res = "bravo"+" "*30
                else:
                    res = "try again"+" "*30
                    memorized[q]+=1
                """
                if number_attempts>=2:
                    sys.stdout.write("\r")
                    sys.stdout.write("help : %s "%(flash_cards.json[q]["answer"]))
                    sys.stdout.flush()
                    time.sleep(0.25 * number_attempts)
                    sys.stdout.write("\r")

                sys.stdout.write("\r")
                sys.stdout.write("%s \n"%(res))
                sys.stdout.flush()
            number_attempts+=1
        if escaped:
            print(EXCEPTION_ESCAPED)
            break
    sys.stdout.write("\r")
    sys.stdout.write("total time %0.1f (s) \n"%(total_time))
    sys.stdout.flush()
    
    return total_time
    

def load_deck(name,definition,root_folder=None):
    """
    name: the deck name under which saved on HDD with with .json extension
    definition: the function used to initialise deck if no file found on HDD
    """
    if not root_folder:
        root_folder = join(expanduser("~"))
    deck_fp = join(root_folder,name)
    if exists(deck_fp):
        logging.info("loading existing deck: %s"%(name))
        deck = flash_card_deck(deck_fp)
    if name=="Elodie.json" and not (definition is None):
        deck = definition(deck)
        deck.set_fn(name)
        deck.set_shuffled()
    elif name=="Camille.json":
        deck = definition()
        deck.set_fn(name)
    elif name=="Papa.json":
        print("creating papa deck")
        deck = definition()
        deck.set_fn(name)
        deck.set_shuffled()
    else:
        logging.info("requested deck name: %s, loading demo",name)
        deck = deck_from_json()
    return deck

class Card_Display():
    """ python for console and js for HTML5 """
    def __init__(self):
        pass
    def show_flash_cards(self):
        pass
    def timed_input(self):
        pass

logger = logging.getLogger()
if __name__=="__main__":
    import argparse
    logger.setLevel(logging.DEBUG)
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("TEST DEBUG")
    known_students = ["Camille","Elodie","Papa"]

    parser = argparse.ArgumentParser(description='CLI for flash cards')
    parser.add_argument('student', choices=known_students,
                    help='the name of the student')

    parser.add_argument("next", choices=["practice","more"],
              help="practice or add new skills to be practiced")

    parser.add_argument("--function", "-f", choices=["add","mult","div"],
            help = "if adding new skills to deck, choose which ones")

    args = parser.parse_args()
    args_dict = vars(args)

    if args_dict["student"] in known_students:
        deck_name = args_dict["student"]+".json"
    else:
        exit()

    if args_dict["next"]=="more":
      extend_deck = {"add":"","mult":"","div":"add_div_tables"}
      flash_cards = load_deck(deck_name,eval(extend_deck[args_dict["function"]]),"./")
      flash_cards.save_hdd()
      exit()

    #FROM NOW WE ARE IN PRACTICE MODE
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())

        if deck_name == "Papa.json" or deck_name == "Elodie.json":
            func = add_mult_tables
        elif deck_name == "Camille.json":
            func = summ_tables
        flash_cards = load_deck(deck_name,func)

        if deck_name == "Papa.deck" or deck_name == "Elodie.deck":
            pass
            #flash_cards.set_shuffled()
        
        if deck_name == "Papa.deck":
            logging.getLogger().setLevel(logging.DEBUG)
        
        print("\n\n\n*********************\n\t\t\t%s \n*********************\n"%(deck_name))

        total_time  = show_flash_cards(flash_cards, total_time_s = 300)
        flash_cards.save_hdd()
        print("total error count:",flash_cards.this_session_bad)
        print("total card seen  :",flash_cards.this_session_bad+flash_cards.this_session_good)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    print("finis !!!")
