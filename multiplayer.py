from discord import player
import multidict
from numpy import true_divide

import Word
import discord

import datetime


class Multiplayer:
    def __init__(self, word_obj:Word):
        
        # self._room_id = int
        self._game_room_id = discord.ChannelType
        # self._game_room_wait = int
        self._message_wait = discord.Message
        
        self._playing = False
        self._author_id = int
        
        self._players = []
        #room_id : list_user.id
        self._word_object = word_obj
        
        self._dict_tours = {}
        """
        user_name.id (in this game) : tour (bool)
        By theses bools, the script knows who's have to
        play yet because during a tour, the users that havn't
        in this tour yet! Their tour value is False otherwise
        it's true. Their value is reset when a tour is completed.
        """
        
        self._time_creation = datetime.datetime.utcnow + datetime.timedelta(minutes=10)
    
    def set_word_object(self, w:Word):
        self._word_object = w
    
    def get_word_object(self):
        return self._word_object
    
    def refresh_who_had_played(self):
        """Refresh the dict_tour for knowing who's gonna have to play"""
        last_value_is_true = False
        foundt = False
        for player, play in self._dict_tours:
            if not foundt:            
                if play:
                    last_value = True
                else:
                    if last_value:
                        self._dict_tours[player] = True
                        foundt = True
        
    
    def get_who_playing(self):
        """
            Get the player wich had to play

        Returns:
            player_name(str): name of the player
        """
        last_value_is_true = False
        pl = str
        foundt = False
        for player, play in self._dict_tours:
            if not foundt:
                if play:
                    last_value = True
                else:
                    if last_value:
                        pl = player
                        foundt = True
        return pl
    
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

