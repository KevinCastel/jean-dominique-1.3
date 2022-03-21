from discord import player
import multidict


class Multiplayer:
    def __init__(self):
        
        self._room_id = int
        
        self._playing = False
        
        self._players = []
        #room_id : list_user.id
        self._word_object = None
        
        self._dict_tours = {}
        """
        user_name.id (in this game) : tour (bool)
        By theses bools, the script knows who's have to
        play yet because during a tour, the users that havn't
        in this tour yet! Their tour value is False otherwise
        it's true. Their value is reset when a tour is completed.
        """
        
    @property
    def roomid(self):
        return self._room_id
    
    @roomid.setter
    def roomid(self, i:int):
        self._room_id = i
        
    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, x):
        self._players.append(x)

