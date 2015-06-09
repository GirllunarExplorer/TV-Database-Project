#!/usr/bin/env python
__author__ = 'tracyrohlin'

import tvdb_api, sqlite3
from pytvdbapi import api
from string import capwords
db = api.TVDB('B43FF87DE395DF56') #sets api key for pytvdb



conn = sqlite3.connect('TV.db')
c = conn.cursor()
c.execute("SELECT DISTINCT TVshow FROM Television")
TV_shows = [str(item)[3:-3] for item in c.fetchall()]


for show in TV_shows:

    try:
        t = tvdb_api.Tvdb(banners=True)

        results = db.search(show, 'en')
        possible_tv_shows = [str(item)[8:-1] for item in results]

        # searches tvdb for possible matches based on TV show
        # and gets the correct showID
        print "Currently working on " + show +"."
        for item in possible_tv_shows:
            possible_desc = t[item]["overview"]
            demarker = ". ".encode("utf8")
            lines = possible_desc.split(demarker)
            for line in lines:
                print line
            answer = raw_input("Is this the correct show description? \n")
            answer.lower()
            if answer[0] == "y":
                show_id = int(t[item]["id"])
                c.execute("UPDATE Television SET ShowId=? WHERE TVshow=?", (show_id, show))
                break
            else:
                show_id = raw_input("What is the show ID?")
                c.execute("UPDATE Television SET ShowId=? WHERE TVshow=?", (show_id, show))
                break

        print "CHECKING SEASONS NOW"
        tvshow = db.get_series(show_id, "en")
        for season in tvshow.seasons:
            if season != 0: #ignores interviews and specials


                c.execute("SELECT EpisodeName FROM Television WHERE ShowId=? AND Season=?", (show_id, season))
                list_of_episodes = [(str(episode)[3:-3]).lower() for episode in c.fetchall()]

                epis_we_have = set(list_of_episodes)

                episodes_should_have = []
                for ep in tvshow.seasons[season]:
                    episode_name = (str(ep.EpisodeName)).lower()
                    episodes_should_have.append(episode_name)


                tvdb_episodes = set(episodes_should_have)


                if tvdb_episodes.difference(epis_we_have):

                    difference = list(tvdb_episodes.difference(epis_we_have))

                    for diff in difference:
                        print "episode {0} from season {1} of {2}".format(diff, season, show)
                        if (raw_input("This episode seems to be missing from our database.\nDo you have this episode?\n").lower())[0] == "y":
                            c.execute("UPDATE Television SET EpisodeName=? WHERE ShowId=? AND Season=?", (capwords(diff), show_id, season))



                else:
                    print "There are no differences."

                print "FINISHED SEASON", season


    except Exception as e:
        print e



conn.commit()


c.execute("select * from Television")
res = [[item for item in results] for results in c.fetchall()]
c.close()
for item in res:
    print item

