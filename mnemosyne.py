"""
Mnemosyne interface module
"""
import sqlite3
import facit.facit_wrapper as fw


def mnemosyne_to_json(db_full_path,name,tag):
    """ Converts a mnemosyne to a json file
    Paramters:
    ----------
    db_full_path: str
        full path to mnemosyne db (sqllite)
    Returns:
    --------
    None
    Usage:
    ------
    NTR
    """
    conn = sqlite3.connect(db_full_path)
    c = conn.cursor()
    t = (tag,)
    c.execute('SELECT * FROM cards WHERE tags=?',t)
    rows = c.fetchall()
    headers = list(map(lambda x: x[0], c.description))
    mycards = fw.Facit_Class(tag)
    for r in rows:
        #print(r[5],r[6])
        mycards.put_card(r[5],r[6])
    mycards.save_to_file(mnemosyne_db_path.replace(".db",".json")) 

if __name__=="__main__":
    mnemosyne_db_path = "C:/docs/Box Sync/Dropbox/anki downloads/mnemosyne_114cards_tiorgs_sqlite.db"
    mnemosyne_to_json(mnemosyne_db_path,name="TI orgs",tag="TI orgs")