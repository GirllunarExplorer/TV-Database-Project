# TV-Database-Project
Creates a database of all the shows, seasons and episodes in a folder.  All episode files follow a "01 - Episode name.file" format or a "Episode 1.file" format.

TV_DB_structure.py creates the initial database.  It takes the folder where all the TV shows are stored as an argument:

   python TV_DB_structure.py "/Volumes/video/TV Shows/"
    ...
    >>> working on  Jonathan Strange & Mr Norrell The Friends Of English Magic Episode 01 from TV show Jonathan Strange & Mr Norrell
    >>> working on  Jonathan Strange & Mr Norrell How Is Lady Pole Episode 02 from TV show Jonathan Strange & Mr Norrell
    >>> working on  Jonathan Strange & Mr Norrell The Education of a Magician Episode 03 from TV show Jonathan Strange & Mr Norrell
    >>> working on  Jonathan Strange & Mr Norrell All The Mirrors Of The World Episode 04 from TV show Jonathan Strange & Mr Norrell
    ...

TV_Search.py searches through the database and finds mismatches between what TVDB has in their database and what the user has in their folder.

First it searches by TV show and asks the user if the show description matches the show they have.  This is to prevent searching TVDB for the wrong show.
    python TV_Search.py 
   
    >>> Currently working on Helix.
    >>> A team of scientists from the Centre for Disease Control travel to a high tech research facility in the Arctic to investigate a possible disease outbreak, only to find themselves pulled into a terrifying life-and-death struggle that holds the key to mankind's salvation...or total annihilation.
    >>> Is this the correct show description? 
    yes
   
    >>> CHECKING SEASONS NOW
    >>> episode vector from season 1 of Helix
    >>> This episode seems to be missing from our database.
    >>> Do you have this episode?
    yes

If the user inputs "yes", the database is updated.  Otherwise, the user may wish to find the missing episode.



