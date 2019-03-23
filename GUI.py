import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import webbrowser
from sqlreader import read_places_sqlite_and_create_csv
from packager import process, load_lists, get_places, csv, datetime, save_output
import sys

class Handler:
    def exit(self, *args):
        print("Quitting")
        Gtk.main_quit()

    def on_GO_pressed(self, button):
        start_analysis()

    def open_Report(self, button):
        print('Opening report')
        webbrowser.open_new("./datapackage/report/t2da.html")

    def dialog_ok(self, button):
        dialog.destroy()
    
    def save_data(self, button):
        BASE_PATH = 'datapackage'
        with open('private/websites.csv', 'r') as f:
            reader = csv.reader(f)
            package, fields, col = process(BASE_PATH, reader)
            load_lists()
            places = get_places(reader, col)
        rowcount = len(places)
        print(fields)
        with open(BASE_PATH + "/data/places.csv", 'w') as csvfile:
            spamwriter = csv.writer(csvfile)
            save_output(spamwriter, fields, places)


def start_analysis():
    print("Magic happens now...")
    label.set_text("WORKING...")
    run = True

    try:
        read_places_sqlite_and_create_csv()
        print("CSV files created")
    except:
        run = False
        dialog.show()

    if (run):
	    BASE_PATH = 'datapackage'
	    with open('private/websites.csv', 'r') as f:
	        reader = csv.reader(f)
	        package, fields, col = process(BASE_PATH, reader)
	        load_lists()
	        places = get_places(reader, col)

	    rowcount = len(places)
	    if rowcount is 0:
	        print("Uh-oh! Nothing to write home about.")
	    else:
	        c_risky    = sum(1 for p in places if p['is_risky'])
	        c_verified = sum(1 for p in places if p['is_verified'])
	        t_min = min([int(p['timestamp']) for p in places if p['timestamp'] != ''])/1000000
	        t_max = max([int(p['timestamp']) for p in places if p['timestamp'] != ''])/1000000
	        output = ("From " + datetime.utcfromtimestamp(t_min).strftime('%Y-%m-%d %H:%M:%S') + " to " + datetime.utcfromtimestamp(t_max).strftime('%Y-%m-%d %H:%M:%S') +"\nYou visited %d Websites\nOf these %d are verified\nYou visited %d risky websites" % (rowcount, c_verified, c_risky))
	        print(output)
	        label.set_text(output)

builder = Gtk.Builder()
builder.add_from_file("Test.glade")
builder.connect_signals(Handler())
window = builder.get_object("Window")
window.show_all()
dialog = builder.get_object("Firefox_Open")
label = builder.get_object("Results")
Gtk.main()
