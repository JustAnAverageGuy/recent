#!/usr/bin/env python3

import sys
import time

import gi

gi.require_versions({
    'Gtk' : '3.0', 
    'GLib': '2.0',
})
from gi.repository import Gtk, Gio, GLib


def add_to_recent(file_path):
    input_file = Gio.File.new_for_path(file_path)
    if not input_file.query_exists(None):
        print(f"No such file or directory: {file_path}")
        sys.exit(1)

    info = input_file.query_info("time::access", Gio.FileQueryInfoFlags.NONE, None)
    info.set_attribute_uint64("time::access", int(time.time()))
    input_file.set_attributes_from_info(info, Gio.FileQueryInfoFlags.NONE, None)

    uri = input_file.get_uri()
    rm = Gtk.RecentManager.get_default()
    rm.add_item(uri)

    GLib.idle_add(Gtk.main_quit)
    Gtk.main()


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} filename")
        sys.exit(0)

    add_to_recent(sys.argv[1])


if __name__ == "__main__":
    main()
