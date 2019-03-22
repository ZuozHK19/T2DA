import os
import sqlite3
import re
import fnmatch
import configparser
import platform


test_mode = True    #when true use a local copy of the DB instead of the one used by firefox

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
    if (test_mode):
        return "./";
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

def test_locating_and_reading_sql():
    cur = open_history_db(get_path())
    select_statement = "select moz_places.url, moz_places.visit_count from moz_places;"
    cur.execute(select_statement)
    results = cur.fetchall()
    for url, count in results:
        print(url)

def read_places_sqlite_and_create_csv():
    cur = open_history_db(get_path())
    select_statement = "select moz_places.url, moz_places.visit_count from moz_places;"
    cur.execute(select_statement)
    results = cur.fetchall()
    out = open("websites.csv", "w")
    for url, count in results:
        out.write(url + "\t" + str(count) + "\n")

#test_locating_and_reading_sql()

read_places_sqlite_and_create_csv()
