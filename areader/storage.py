import glob
import json
import datetime

from .arvxivlib import *

config_file = "config.json"
storage_file = "db.json"

datetime_frmt = "%d/%m/%Y %H:%M:%S"

def parse_date(string : str) :
    return datetime.strptime(string,datetime_frmt)

def date_to_str(date) : 
    return date.strftime(datetime_frmt)



def init_storage():
    try: 
        os.mkdir("storage")
    except :
        print("")






class ConfigDb : 

    def load_db(self):
        try: 
            fp = open(config_file,'r')
            self.db = json.load(fp)
            fp.close()
        except :
            self.db = {
                "cats" : ["astro-ph.SR","astro-ph.EP","physics.comp-ph","cs.DC"],
                "fetch_count" : 500,
                "fav_authors" : [],
                "fav_keyword" : []
            }

    def save_db(self):
        fw = open(config_file, "w")
        json.dump(self.db, fw, indent = 4)
        fw.close()

    def __init__(self):

        init_storage()

        self.load_db()
        self.save_db()


class ArticleDb : 

    def load_db(self):
        try: 
            fp = open(storage_file,'r')
            self.db = json.load(fp)
            fp.close()
        except :
            self.db = {}

    def save_db(self):
        fw = open(storage_file, "w")
        json.dump(self.db, fw, indent = 4)
        fw.close()

    def __init__(self):

        init_storage()

        self.load_db()
        self.save_db()

        self.config = ConfigDb()


    def fetch_articles(self):
        article_lst = get_result_list(self.config.db["cats"],0,self.config.db["fetch_count"])

        for a in article_lst:
            hsh = get_entry_hash(a)

            if not (hsh in self.db.keys()):
                self.db[hsh] = {
                    "hash" : hsh,
                    "title" : a.title,
                    "authors" : [auth.name for auth in a.authors],
                    "abstract" : a.summary,
                    "id" : a.entry_id,
                    "published" : date_to_str(a.published),
                    "updated" : date_to_str(a.updated),
                    "comments" : a.comment,
                    "read" : False,
                    "favorite" : False
                }

        self.save_db()


    def get_unread_arts(self):
        tmp = []

        for k in self.db.keys():
            if not (self.db[k]["read"]):
                tmp.append(self.db[k])

        return sorted(tmp, key=lambda d: d['published'],reverse=True) 
        
    
    
    def get_unread_alert_arts(self):
        tmp = []

        for k in self.db.keys():
            if not (self.db[k]["read"]):

                art = self.db[k]

                alert = False

                str_auth = ""
                for a in art["authors"][:-1]:
                    str_auth += a + ", "
                str_auth += art["authors"][-1]

                for ka in self.config.db["fav_authors"]:
                    if ka in str_auth:
                        alert = True

                for ka in self.config.db["fav_keyword"]:
                    if ka in art["abstract"]:
                        alert = True

                if alert:
                    tmp.append(art)

        return sorted(tmp, key=lambda d: d['published'],reverse=True) 
        

    def set_read(self,hsh):
        self.db[hsh]["read"] = True
        self.save_db()
    

    





