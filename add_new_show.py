#!/usr/bin/env python

from TV_DB_structure import *


conn = sqlite3.connect('TV.db')
c = conn.cursor()
c.execute("SELECT DISTINCT TVshow FROM Television")
all_shows = [str(item)[3:-3] for item in c.fetchall()]


def set_destination():
    default = '/Volumes/video/TV Shows/'
    file_path = raw_input("Please enter destination path.  Default is {0} \n"
                          "If this is ok, press enter to continue.\n".format(default))
    if not file_path:
        file_path = default
    return file_path


def add_show(TV_show):
    file_path = set_destination()
    TV_show_path = file_path + TV_show

    sql_TV_db(TV_show_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add a new show to the TV db')
    parser.add_argument("TV_Show", help="Must be a TV show name that is listed on the TVDB website.")
    args = parser.parse_args()

    add_show(args.TV_Show)

