import pandas as pd
import sqlite3
from datetime import datetime

def delete_db():
  con = sqlite3.connect("DrillMaster.db")
  cursor = con.cursor()
  cursor.execute("DROP TABLE users")
  cursor.execute("DROP TABLE questions")
  #cursor.execute("DROP TABLE history")

def create_db():
  con = sqlite3.connect("DrillMaster.db")
  cursor = con.cursor()
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
  cursor.execute(" INSERT INTO users (id, name) VALUES (1, 'Demo')")
  #cursor.execute(" INSERT INTO users (id, name) VALUES (4, 'Elodie')")
  #cursor.execute(" INSERT INTO users (id, name) VALUES (5, 'Camille')")
  con.commit()
  con.close()
  
def add_a_deck_log():
  #example from : https://stackoverflow.com/a/14814039/1167333
  con = sqlite3.connect("DrillMaster.db")
  cursor = con.cursor()
  ts_old = 1601414396
  ts = int(datetime.strftime(datetime.utcnow(), "%s"))
  many_inserts = [ (ts, 2, 2,10, 15, 0,0),(ts_old,2,2,10,15,0,1)]
  print(many_inserts)
  #cursor.execute(" INSERT INTO questions ( 'id', 'q_text') VALUES ( 0, 'no_id');")
  cursor.executemany(" INSERT INTO 'history' values ( ?, ?, ?, ?, ?, ?, ? ); ", many_inserts )
  con.commit()
  con.close()

def view_users_activities_log():
  con = sqlite3.connect("/var/www/DrillMaster/DrillMaster/DrillMaster.db")
  df = pd.read_sql_query("SELECT * FROM history",con)
  dfu = pd.read_sql_query("SELECT * FROM users",con)
  df = df.merge(dfu, how="left", left_on="U_ID", right_on="ID")
  df['TIME']=df['TIME'].apply(lambda x: pd.datetime.fromtimestamp(x).date())
  df['GOOD']=(df['ANSWER']==df['EXPECTED_ANSWER']).astype(int)
  #g = df.groupby(pd.DatetimeIndex(df['TIME']).normalize()).count()
  df = df[['TIME','NAME','ANSWER','GOOD']]
  g = df.groupby(by=['TIME','NAME']).agg({'GOOD':'sum','ANSWER':'count'}).reset_index()
  return g

if __name__=="__main__":
  #delete_db()
  #create_db()
  add_a_deck_log()
  df = view_users_activities_log()
  print(df)
