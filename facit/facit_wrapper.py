"""
Facit API
Uses Promptos Facit: Practice makes perfect
"""
import json
from uuid import uuid4

class Facit_Class:
    """
    Usage:
    ------
    mycards = Facit_Class("german",cards=[{
    "frontValue": "tactful",
    "frontHint":  "diplomatic about what you say",
    "backValue":  "taktvoll",
    "backHint":   ""
    }])
    print(mycards.get_cards())
    mycards.save_to_file("c:/tmp/german.json")
    """
    json_string={}
    def __init__(self,name,details="",uuid_string=None,source="",\
        next_decks=[],prev_decks=[],cards=[]):
        self.json_string["name"]=name
        self.json_string["details"]=details
        if uuid_string is None:
            uuid_string = str(uuid4())
        self.json_string["uuid"]=uuid_string
        self.json_string["source"]=source
        self.json_string["next"]=next_decks
        self.json_string["prev"]=prev_decks
        self.json_string["cards"]=[]
        if not len(cards)==0:
            for c in cards:
                self.put_card(c["frontValue"],c["backValue"],c["frontHint"],c["backHint"])
    def put_card(self,frontValue,backValue,frontHint="",backHint=""):
        self.json_string["cards"].append({"frontValue":frontValue,"frontHint":frontHint,\
            "backValue":backValue,"backHint":backHint})
    def get_cards(self):
        return self.json_string
    def save_to_file(self,full_path):
        with open(full_path,'w') as fo:
            json.dump(self.json_string,fo, indent=4)


if __name__=="__main__":
    mycards = Facit_Class("am6x",cards=[{
    "frontValue": "tactful",
    "frontHint":  "diplomatic about what you say",
    "backValue":  "taktvoll",
    "backHint":   ""
  }])
    print(mycards.get_cards())
    mycards.save_to_file("c:/tmp/test.json")