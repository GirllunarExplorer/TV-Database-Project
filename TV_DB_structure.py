#!/usr/bin/env python

__author__ = 'GirlLunarExplorer'

import argparse
import os
import sqlite3
import re

conn = sqlite3.connect('TV.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Television(TVshow varchar(155) NOT NULL, Season varchar(155) NOT NULL, EpisodeNumber varchar(3), EpisodeName varchar(255), ShowId int NOT NULL)")
#c.execute("DROP TABLE Television")
conn.commit()


def normal_episodes(episode, tv_show, season):
    """Matches episodes that are labeled 01x01 - Episode Name or 01x01-02 - Long Episode Name"""
    episode_number, episode_name = episode.split(" - ", 1)
    episode_number = episode_number.split("x")[-1]
    long_episodes = episode_number.split("-", 1)

    for epi in long_episodes:
        print "Working on Episode {0} - {1} from TV show {1}".format(epi, episode_name, tv_show)
        c.execute("INSERT INTO Television VALUES (?,?,?,?,?)", (tv_show.decode('utf-8'), season, epi.decode('utf-8'), episode_name.decode('utf-8'), 0))
        conn.commit()


def unnamed_episodes(episode, tv_show, season):
    """Matches files that are named Episode 1, Episode 2, etc."""

    print "Working on Episode {0} from TV show {1}".format(episode, tv_show)
    c.execute("INSERT INTO Television VALUES (?,?,?,?,?)", (tv_show.decode('utf-8'), season, "NULL", episode.decode('utf-8'), 0))
    conn.commit()


def sql_TV_db(file_path):
    """Creates a TV db based on the folders and video files in a specified directory."""

    for root, dirs, files in os.walk(file_path):
        depth = root[len(file_path) + len(os.path.sep):].count(os.path.sep)
        if depth == 1:

            split_root =  root.split("/")
            tv_show = split_root[-2]
            season = split_root[-1].split("Season")[-1]
            episodes = list(set(f.split(".")[0] for f in files if f.endswith(("mkv", "avi", "mp4"))))

            for episode in episodes:
                if re.match("\d+x\d+[-\d+]*\s-\s[\w+\s\W]*", episode):
                    normal_episodes(episode, tv_show, season)

                elif re.match("episode\s\d+", episode, re.IGNORECASE):
                    unnamed_episodes(episode, tv_show, season)
                else: pass
        conn.commit()

    c.execute("select * from Television")
    c.close()




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create SQL DB of TV shows, consisting of seasons and episodes')
    parser.add_argument("--file_path", default="/Volumes/video/TV Shows/", help="must be file path")
    args = parser.parse_args()

    sql_TV_db(args.file_path)
