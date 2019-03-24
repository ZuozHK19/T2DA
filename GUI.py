import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import webbrowser
from sqlreader import read_places_sqlite_and_create_csv, test_locating_and_reading_sql
from packager import *
import sys, time
import json
import threading

class Handler:
    def exit(self, *args):
        print("Quitting")
        Gtk.main_quit()

    def on_GO_pressed(self, button):
        threading.Thread(target=start_analysis).start()

    def open_Report(self, button):
        print('Opening report')
        webbrowser.open_new("./datapackage/report/t2da.html")

    def contact_Dev(self, button):
        print('Opening issues')
        webbrowser.open_new("https://github.com/ZuozHK19/T2DA/issues/new")

    def dialog_ok(self, button):
        global dialog
        dialog.hide()
        #dialog.destroy()
        #dialog = builder.get_object("Firefox_Open")

    def save_data(self, button):
        make_output()


def make_output():
    BASE_PATH = 'datapackage'
    if not os.path.isfile('private/websites.csv'): return
    with open('private/websites.csv', 'r') as f:
        reader = csv.reader(f)
        package, fields, col = process(BASE_PATH, reader)
        load_lists()
        places = get_places(reader, col)
    with open(BASE_PATH + "/data/places.csv", 'w+') as csvfile:
        spamwriter = csv.writer(csvfile)
        save_output(spamwriter, fields, places)

    summary = generate_summary(places)
    with open(BASE_PATH + "/report/data/summary.json", 'w+') as outfile:
        json.dump(summary, outfile)

    stats = generate_stats(places)
    with open(BASE_PATH + "/report/data/stats.json", 'w+') as outfile:
        json.dump(stats, outfile)

def start_analysis():
    print("Magic happens now...")
    gobutton.set_sensitive(False)
    label.set_text("")

    try:
        test_locating_and_reading_sql(False)
    except:
        gobutton.set_sensitive(True)
        dialog.show()
        return

    read_places_sqlite_and_create_csv()
    print("CSV files created")

    BASE_PATH = 'datapackage'
    with open('private/websites.csv', 'r') as f:
        reader = csv.reader(f)
        package, fields, col = process(BASE_PATH, reader)
        load_lists()
        places = get_places(reader, col)

    summary = generate_summary(places)
    rowcount = summary['count']['total']
    if rowcount is 0:
        label.set_text("No data available! Report was not generated.")
        print("Uh-oh! Nothing to write home about.")
    else:
        make_output()
        c_risky    = summary['count']['risky']
        c_verified = summary['count']['verified']
        t_min = summary['daterange']['from']
        t_max = summary['daterange']['to']
        output = (
            "From %r to %r\nYou visited %d Websites\nOf these %d are verified\nYou visited %d risky websites" %
            (t_min, t_max, rowcount, c_verified, c_risky)
        )
        print(output)
        label.set_text(output)

    gobutton.set_sensitive(True)

builder = Gtk.Builder()
builder.add_from_file("Test.glade")
builder.connect_signals(Handler())
window = builder.get_object("Window")
window.show_all()
dialog = builder.get_object("Firefox_Open")
label = builder.get_object("Results")
gobutton = builder.get_object("GO")
Gtk.main()
