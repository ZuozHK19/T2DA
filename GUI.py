import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from sqlreader import read_places_sqlite_and_create_csv

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def on_GO_pressed(self, button):
        print("Magic happens now...")
        read_places_sqlite_and_create_csv()
        print("CSV files created")


builder = Gtk.Builder()
builder.add_from_file("Test.glade")
builder.connect_signals(Handler())
window = builder.get_object("Window")
window.show_all()
Gtk.main()
