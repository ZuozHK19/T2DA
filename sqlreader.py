import os
import sqlite3
import re
import fnmatch
import configparser
import platform
import csv

def get_path_linux():
    data_path = os.path.expanduser('~')+"/.mozilla/firefox"
    for file in os.listdir(data_path):
        if fnmatch.fnmatch( file, '*.default'):
            data_path += "/" + file
            break
    return data_path

def get_path_windows():
    mozilla_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox')
    mozilla_profile_ini = os.path.join(mozilla_profile, r'profiles.ini')
    profile = configparser.ConfigParser()
    profile.read(mozilla_profile_ini)
    data_path = os.path.normpath(os.path.join(mozilla_profile, profile.get('Profile0', 'Path')))
    return data_path

def get_path():
    test_mode = os.path.isfile(os.path.join("private", 'places.sqlite'))
    if (test_mode):
        return "private"
    else:
        if (platform.system() == "Windows"):
            data_path = get_path_windows()
        elif (platform.system() == "Linux"):
            data_path = get_path_linux()
        return data_path

def open_history_db(data_path):
   history_db = os.path.join(data_path, 'places.sqlite')
   c = sqlite3.connect(history_db)
   cursor = c.cursor()
   return cursor

def test_locating_and_reading_sql(and_print=True):
    cur = open_history_db(get_path())
    select_statement = "select moz_places.id, moz_places.url, moz_places.title, moz_places.rev_host, moz_places.visit_count, moz_places.hidden, moz_places.typed, moz_places.favicon_id, moz_places.frecency, moz_places.last_visit_date, moz_places.guid, moz_places.foreign_count, moz_places.url_hash, moz_places.description, moz_places.preview_image_url, moz_places.origin_id from moz_places;"
    cur.execute(select_statement)
    if not and_print: return
    results = cur.fetchall()
    for url, count in results:
        print(url)

def read_places_sqlite_and_create_csv():
    cur = open_history_db(get_path())
    select_statement = "select moz_places.id, moz_places.url, moz_places.title, moz_places.rev_host, moz_places.visit_count, moz_places.hidden, moz_places.typed, moz_places.favicon_id, moz_places.frecency, moz_places.last_visit_date, moz_places.guid, moz_places.foreign_count, moz_places.url_hash, moz_places.description, moz_places.preview_image_url, moz_places.origin_id from moz_places;"
    cur.execute(select_statement)
    results = cur.fetchall()
    try:
        os.mkdir('private')
    except OSError as exc:
        pass
    out = csv.writer(open(os.path.join("private", "websites.csv"),"w+"))
    out.writerow(['id','url','title','rev_host','visit_count','hidden','typed','favicon_id','frecency','last_visit_date','guid','foreign_count','url_hash','description','preview_image_url','origin_id'])
    for iD,url,title,rev_host,visit_count,hidden,typed,favicon_id,frecency,last_visit_date,guid,foreign_count,url_hash,description,preview_image_url,origin_id in results:
        out.writerow([iD,url,title,rev_host,visit_count,hidden,typed,favicon_id,frecency,last_visit_date,guid,foreign_count,url_hash,description,preview_image_url,origin_id])

if __name__ == "__main__":
    #test_locating_and_reading_sql()
    read_places_sqlite_and_create_csv()
