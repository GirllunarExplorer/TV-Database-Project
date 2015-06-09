#!/usr/bin/env python

__author__ = 'GirlLunarExplorer'

import argparse, os, sqlite3, re

def sql_TV_db(file_path):
    conn = sqlite3.connect('TV.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Television(TVshow varchar(155) NOT NULL, Season varchar(155) NOT NULL, EpisodeNumber varchar(3), EpisodeName varchar(255), ShowId int NOT NULL)")
    #c.execute("DROP TABLE Television")
    conn.commit()

    for root, dirs, files in os.walk(file_path):
        depth = root[len(file_path) + len(os.path.sep):].count(os.path.sep)
        if depth == 1:

            split_root =  root.split("/")
            tv_show = split_root[-2]
            season = split_root[-1]
            try:
                season = int((re.findall("\d+", season))[0])
            except:
                season = 1 #sets the season to 1 if the folder for a particular season does not exist

            for episode in files:
                if episode.endswith(("mkv", "avi", "mp4")):
                    if "._" in episode:  #gets rid of hidden files
                        pass

                    elif re.match("\d+x\d+[-\d+]*\s-\s[\w+\s\W]*", episode):  #matches files that look like
                                                                            # 01x01(-02) - Episode name

                        episode = episode.split("x", 1)[1]
                        episode_sub_list = episode.split(" - ", 1)
                        episode_num = episode_sub_list[0]
                        long_episodes = episode_num.split("-", 1)
                        episode_name = episode_sub_list[1][0:-4]

                        for epi in long_episodes:
                            print "Working on Episode {0} - {1} from TV show {1}".format(epi, episode_name, tv_show)
                            c.execute("INSERT INTO Television VALUES (?,?,?,?,?)", (tv_show.decode('utf-8'), season, epi.decode('utf-8'), episode_name.decode('utf-8'), 0))
                            conn.commit()


                    else:
                        episode_name = episode[0:-4]
                        print "Episode {0} from TV show {1}".format(episode_name, tv_show)
                        c.execute("INSERT INTO Television VALUES (?,?,?,?,?)", (tv_show.decode('utf-8'), season, "NULL", episode_name.decode('utf-8'), 0))
                        conn.commit()

        conn.commit()

    c.execute("select * from Television")
    c.close()




if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Create SQL DB of TV shows, consisting of seasons and episodes')
    parser.add_argument("file_path", help="must be file path")
    args = parser.parse_args()

    sql_TV_db(args.file_path)
