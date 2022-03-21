from discord import player
import multidict

import datetime

import discord

import Word

class Multiplayer:
    def __init__(self):
        
        # self._room_id = int
        self._game_room_id = int
         # self._game_room_wait = int
        self._message_wait = discord.Message
        self._author_id = int
        self._playing = False
        
        self._players = []
        #room_id : list_user.id
        self._word_object = Word
        
        self._dict_tours = {}
        """
        user_name.id (in this game) : tour (bool)
        By theses bools, the script knows who's have to
        play yet because during a tour, the users that havn't
        in this tour yet! Their tour value is False otherwise
        it's true. Their value is reset when a tour is completed.
        """
        self._time_creation = datetime.datetime.utcnow + datetime.timedelta(minutes=10)

    @property
    def is_playing(self):
        return self._playing
    
    @is_playing.setter
    def is_playing(self, v:bool):
        self._playing = v

    @property
    def author_id(self):
        return self._author_id
    
    @author_id.setter
    def author_id(self, i:int):
        self._author_id = i

    @property
    def room_game_id(self):
        return self._room_id
    
    @room_game_id.setter
    def room_game_id(self, i:int):
        self._game_room_id = i

    @property
    def message(self):
        return self._message_wait
    
    @message.setter
    def message(self, msg:discord.Message):
        self._message_wait = msg

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, x):
        self._players.append(x)

