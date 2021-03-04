#DB API

#standard modules
import logging
from os import environ


#PIP modules


import pandas as pd
import sqlite3
from datetime import datetime

if 'FLASK_ENV' in environ:
  if environ['FLASK_ENV']=="development":
    db_path = "DrillMaster_dev.sqllite"
  else:
    db_path = "/var/www/DrillMaster/DrillMaster/DrillMaster.db"
logger = logging.getLogger()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    #if not hasattr(g, 'sqlite_db'):
      #g.sqlite_db = connect_db()
    con = connect_db()
    #return g.sqlite_db
    return con

def init_db():
    db = get_db()

    with open('schema.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def upgrade_db():
  db = get_db()
  with open('upgrade_scheme.sql', 'r') as f:
    db.cursor().executescript(f.read())
  db.commit()

def connect_db():
    """Connects to the specific database."""
    #rv = sqlite3.connect(app.config['DATABASE'])
    try:
      con = sqlite3.connect(db_path)
    except:
      print(50,db_path)
      logging.error("db_path",db_path)
      raise
    #rv.row_factory = sqlite3.Row
    #return rv
    return con

def delete_db():
  con = sqlite3.connect(db_path)
  cursor = con.cursor()
  cursor.execute("DROP TABLE users")
  #cursor.execute("DROP TABLE questions")
  #cursor.execute("DROP TABLE history")
  
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
    time_to_answer = a["timer"]
    number_attempts = a["number_attempts"]
    ttta = 15 #target time to answer
    qid = 0
    uid = str(user_id)
    
    many_inserts.append((ts, answer,expected, time_to_answer, ttta,number_attempts,qid,uid))
  logger.warning("many inserts")
  logger.warning(many_inserts)
  cursor.executemany(" INSERT INTO 'history' values ( ?, ?, ?, ?, ?, ?, ?, ? ); ", many_inserts )
  con.commit()
  con.close()
  logging.info("db update done")

def get_df_db(sql_query):
  """ returns a dataframe from the database
  wrapper for the db access
  """
  con = sqlite3.connect(db_path)
  df = pd.read_sql_query(sql_query, con)
  return df

def view_users_activities_log():
  df = get_df_db("SELECT * FROM history")
  dfu = get_df_db("SELECT * FROM users")
  df = df.merge(dfu, how="left", left_on="U_ID", right_on="ID")
  df = df.sort_values(by="TIME",ascending=False)
  df['TIME']=df['TIME'].apply(lambda x: pd.datetime.fromtimestamp(x).date())
  df['GOOD']=(df['ANSWER']==df['EXPECTED_ANSWER']).astype(int)

  print(df.head(10))
  print("-------")
  #g = df.groupby(pd.DatetimeIndex(df['TIME']).normalize()).count()
  df = df[['TIME','NAME','NUMBER_ATTEMPTS','GOOD']]
  g = df.groupby(by=['TIME','NAME']).agg({'GOOD':'sum','NUMBER_ATTEMPTS':'sum'}).reset_index()
  g['NUMBER_ATTEMPTS']+=g['GOOD']
  g = g.sort_values(by="TIME",ascending=False)
  return g

def remove_ts():
  con = sqlite3.connect(db_path)
  cursor = con.cursor()

  #cursor.execute("DELETE from history WHERE TIME>=1609372800;")
  cursor.execute("DELETE from history WHERE U_ID='4';")
  #cursor.execute("DELETE from history WHERE U_ID='6';")
  con.commit()
  con.close()

def get_users():
  con = sqlite3.connect(db_path)
  df = pd.read_sql_query("SELECT * FROM users",con)
  return df

def add_user(name):
  con = sqlite3.connect(db_path)
  cursor = con.cursor()
  print(name)
  name = (None,name)
  cursor.execute(" INSERT INTO USERS(ID, NAME) VALUES (?,?)",name)
  last_id = cursor.lastrowid
  print("last1",last_id)
  con.commit()
  last_id2 = cursor.last_id
  print("last2",last_id2)
  con.close()
  last_id3 = cursor.last_id
  print("last3",last_id3)

if __name__=="__main__":
  print(environ['FLASK_ENV'])
  #delete_db()
  #create_db()
  #add_a_deck_log()

  #remove_ts()

  #df = get_users()
  #print(df)
  #add_user("Anthony")
  #df = view_users_activities_log()
  #print(df)
  #print(get_df_db("SELECT * FROM HISTORY"))
