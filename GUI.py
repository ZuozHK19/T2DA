import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from sqlreader import read_places_sqlite_and_create_csv
from packager import process, load_lists, get_places, csv

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def on_GO_pressed(self, button):
        print("Magic happens now...")

        read_places_sqlite_and_create_csv()
        print("CSV files created")

        BASE_PATH = 'datapackage'
        with open('private/moz_places_100.csv', 'r') as f:
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
            print("Verified: %d, Risky: %d, Total: %d" % (c_verified, c_risky, rowcount))

builder = Gtk.Builder()
builder.add_from_file("Test.glade")
builder.connect_signals(Handler())
window = builder.get_object("Window")
window.show_all()
Gtk.main()
