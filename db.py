#DB API

#standard modules
import logging


#PIP modules


import pandas as pd
import sqlite3
from datetime import datetime

db_path = "/var/www/DrillMaster/DrillMaster/DrillMaster.db"
logger = logging.getLogger()

def delete_db():
  con = sqlite3.connect(db_path)
  cursor = con.cursor()
  cursor.execute("DROP TABLE users")
  cursor.execute("DROP TABLE questions")
  #cursor.execute("DROP TABLE history")

def create_db():
  con = sqlite3.connect(db_path)
  cursor = con.cursor()
  cursor.execute('PRAGMA encoding="UTF-8";')
  cursor.execute(" CREATE TABLE IF NOT EXISTS USERS( ID INTEGER PRIMARY KEY, NAME TEXT)")
  cursor.execute(" CREATE TABLE IF NOT EXISTS QUESTIONS( ID INTEGER PRIMARY KEY, Q_TEXT TEXT)")
  cursor.execute(" CREATE TABLE IF NOT EXISTS HISTORY (\
    TIME TIMESTAMP,\
    ANSWER TEXT,\
    EXPECTED_ANSWER TEXT,\
    TIME_TO_ANSWER INTEGER,\
    TARGET_TIME_TO_ANSWER INTEGER,\
    Q_ID INTEGER,\
    U_ID INTEGER,\
    FOREIGN KEY (Q_ID) REFERENCES questions(id),\
    FOREIGN KEY (U_ID) REFERENCES users(id)\
    );")
  #cursor.execute(" INSERT INTO users (id, name) VALUES (0, 'Demo')")
  #cursor.execute(" INSERT INTO users (id, name) VALUES (1, 'Demo')")
  cursor.execute(" INSERT INTO users (id, name) VALUES (4, 'Elodie')")
  cursor.execute(" INSERT INTO users (id, name) VALUES (5, 'Camille')")
  con.commit()
  con.close()
  
def add_a_deck_log():
  #example from : https://stackoverflow.com/a/14814039/1167333
  con = sqlite3.connect(db_path)
  cursor = con.cursor()
  ts_old = 1601414396
  ts = int(datetime.strftime(datetime.utcnow(), "%s"))
  many_inserts = [ (ts, 2, 2,10, 15, 0,0),(ts_old,2,2,10,15,0,1)]
  print(many_inserts)
  #cursor.execute(" INSERT INTO questions ( 'id', 'q_text') VALUES ( 0, 'no_id');")
  cursor.executemany(" INSERT INTO 'history' values ( ?, ?, ?, ?, ?, ?, ? ); ", many_inserts )
  con.commit()
  con.close()

def update_logs(user_id,answers,deck):
  """ update DB logs 
  Parameters:
  -----------
  Returns:
  --------
  Modify:
  -------
  """
  con = sqlite3.connect(db_path)
  cursor = con.cursor()
  cursor.execute('PRAGMA encoding="UTF-8";')
  # [{"question":"2 · 7","answer":"14","number_attempts":"0","timestamp":"1601660293044","timer":"9"}
  many_inserts = []
  logger.warning("update logs for user id: %s",user_id)
  for a in answers:
    ts = int(int(a["timestamp"])/1000)
    answer = a["answer"]
    expected = deck.json[a["question"]]["answer"]
    logger.warning("expected: %s",expected)
    time_to_answer = 15*a["number_attempts"]+a["timer"]
    ttta = 15 #target time to answer
    qid = 0
    uid = str(user_id)
    
    many_inserts.append((ts, answer,expected, time_to_answer,ttta,qid,uid))
  cursor.executemany(" INSERT INTO 'history' values ( ?, ?, ?, ?, ?, ?, ? ); ", many_inserts )
  con.commit()
  con.close()
  logging.info("db update done")


def view_users_activities_log():
  con = sqlite3.connect(db_path)
  df = pd.read_sql_query("SELECT * FROM history",con)
  dfu = pd.read_sql_query("SELECT * FROM users",con)
  df = df.merge(dfu, how="left", left_on="U_ID", right_on="ID")
  print(df)
  print("-"*15)
  print(dfu)
  df['TIME']=df['TIME'].apply(lambda x: pd.datetime.fromtimestamp(x).date())
  df['GOOD']=(df['ANSWER']==df['EXPECTED_ANSWER']).astype(int)
  #g = df.groupby(pd.DatetimeIndex(df['TIME']).normalize()).count()
  df = df[['TIME','NAME','ANSWER','GOOD']]
  g = df.groupby(by=['TIME','NAME']).agg({'GOOD':'sum','ANSWER':'count'}).reset_index()
  return g

def remove_ts():
  con = sqlite3.connect(db_path)
  cursor = con.cursor()

  #cursor.execute("DELETE from history WHERE TIME>=1609372800;")
  cursor.execute("DELETE from history WHERE U_ID='5';")
  cursor.execute("DELETE from history WHERE U_ID='4';")
  con.commit()
  con.close()



if __name__=="__main__":
  #delete_db()
  #create_db()
  #add_a_deck_log()
  remove_ts()
  df = view_users_activities_log()
  print(df)
