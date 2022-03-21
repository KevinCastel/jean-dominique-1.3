from audioop import mul
import datetime
from datetime import time
from dis import disco
from email import message

from os import read, system
from re import M
from unicodedata import category
from aiohttp import client
from discord import CategoryChannel, Color, channel, cog, colour, command, embeds, guild, user
from discord.ext import tasks
from setuptools import Command

from correction import Correction


from File import FileEnvironnement

from HangmanGame import HangmanGame

from multiplayer import Multiplayer

from Word import Word

import discord
from discord.ext import commands

import discord_message
from discord_message import Discord_Command

class Application(discord.Client):
      
    def __init__(self, loop=None):
        super().__init__(loop=loop)
        # intents= discord.Intents.default()
        
        intent = self.intents.default()
        intent.members = True

        self.bot = commands.Bot(command_prefix=":", intents=intent)
        
        self.hg = HangmanGame()
        
        self.dict_jean_dominique_room_by_guild = {}
        #(int(server_id) : {name_channel:channel_id})

        self._dict_hangmans_solo_by_guild = {}
        #(int(server_id) : {user_id:[word_object, channel_id]})
        self._dict_hangmans_multi_by_guild = {}
        #(int(server_id) : [multiplayer_object]})
        
        self._dict_message = {
            "chars_tryed" : str,
            "error_on_command_unknow" : str,
            "error_unknow" : str,
            "introduce_help" : str,
            "help_play" : str,
            "introduce_message" : str,
            "word_introduce":str
        }
        
        self._file_lang = FileEnvironnement()
        self._file_lang.parse_xml_file()

    
    
    """
    Message
    """
    
    @commands.Cog.listener()
    async def on_ready(self):
        """
            on_ready method from discord.py API
        """
        print("Launched")
                
        self._dict_help_msg = self._file_lang.get_global_help_message_to_dict()
        
        jean_dominique_category_exist = False
        jean_dominique_category_id:int
        jean_dominique_category:discord.CategoryChannel
        
        jean_dominique_discuss_channel_exist = False
        
        dict_channel_name_exists = {
            "discuss" : False,
            "log-room" : False,
            "multiplayer-wait" : False
        }
        
        dict_channel_id = {
            "discuss" : int,
            "log-room" : int,
            "multiplayer-wait":int
        }
        
        
        list_jean_dominique_category_channel_id = []
        
        for guild in self.guilds:
            self._dict_hangmans_solo_by_guild[guild.id] = {}
            self._dict_hangmans_multi_by_guild[guild.id] = []
            
            jean_dominique_category_exist = self.check_category_exists(
                list_categories=guild.categories,
                category_name="jean-dominique")
            
            if not jean_dominique_category_exist:
                await guild.create_category(name="jean-dominique")

            jean_dominique_category_id = self.get_category_id(
                categories=guild.categories,
                category_name="jean-dominique")
            
            jean_dominique_category = self.get_category_by_id(
                list_categories=guild.categories,
                category_id = jean_dominique_category_id
            )
            
            for channel_name in dict_channel_name_exists.keys():
                dict_channel_name_exists[channel_name] = self.check_channel_exists(
                    list_channels_from_cat=jean_dominique_category.channels,
                    channel_name=channel_name)
                
            for channel_name,channel_exists in dict_channel_name_exists.items():
                if not channel_exists:
                    # await jean_dominique_category.create_text_channel()
                    await jean_dominique_category.create_text_channel(name=channel_name)
                
                dict_channel_id[channel_name] = self.get_channel_id_by_name(
                    name=channel_name,
                    list_channels_from_cat=jean_dominique_category.channels)
                        
            self.dict_jean_dominique_room_by_guild[guild.id] = dict_channel_id
            dict_channel_id = {
                "discuss":int,
                "log-room":int,
                "multiplayer-wait":int
            }
            
    
        # for dict_channel in self.dict_jean_dominique_room_by_guild.values():
        #     chan = self.get_channel(dict_channel["discuss"])
        #     await chan.send("Hey!\nI'm finally back.")
        
    # @commands.Cog.Listener()
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        message_object = discord.Message
        multi_object = None
        list_multi_channels_waiting = self._dict_hangmans_multi_by_guild[payload.guild.id]
        
        for waiting_multi_channel in list_multi_channels_waiting:
            if message_id == waiting_multi_channel.message.id:
                multi_object = waiting_multi_channel
                
        if not multi_object is None:
            multi_object.players.append(payload.author.id)
    
    # @client.event
    # async def on_raw_reaction_add(payload): #reaction, user
    #     global list_poll, dict_room
    #     user = payload.member
    #     if user.id == 938072411105034280:
    #         return
        
    #     index = 0
        
    #     # msg_id = int(Encode(str(payload.message_id)))
        
    #     msg_id = payload.message_id
    #     msg_id_encoded = hash_data(str(msg_id))
        
    #     chan = client.get_channel(payload.channel_id)
    #     messages = await chan.history(limit=200).flatten()
    #     log_room = client.get_channel(dict_room["log-room"])
        
        
    #     for m in messages:
    #         if msg_id == m.id:
    #             message = m
        
    #     poll = None
        
        
        
    #     does_user_already_voted = False
        
    #     for p in list_poll:
    #         if p.message_id == msg_id_encoded:
    #             poll = p
    #         if poll == None:
    #             index += 1
                
        
    #     if poll != None:
    #         for v in poll.dict_reacts.values():
    #             if not does_user_already_voted:
    #                 does_user_already_voted = user.id in v
    #         if not does_user_already_voted:
    #             poll.dict_reacts[str(payload.emoji)].append(user.id)            
    #             list_poll[index].dict_reacts = poll.dict_reacts
    #             await chan.send("Merci d'avoir voter")
    #             channel = client.get_channel(payload.channel_id)
    #             embed = discord.Embed(title="Vote", color=log_color)
    #             embed.set_author(name=user.name, icon_url=user.avatar.url)
    #             embed.add_field(name=f"New vote for '{poll.name}'", value=f"{user.name} voted at {get_time_now()}")
    #             await log_room.send(embed=embed)
    #         else:
    #             await message.remove_reaction(payload.emoji, user)
    #             await chan.send("Vous avez déjà voter")
    #             embed = discord.Embed(title="ERROR x.x", color=log_color)
    #             embed.set_author(name=user.name, icon_url=user.avatar.url)
    #             embed.add_field(name=f"New vote that doesn't counted for '{poll.name}'", value=f"{user.name} voted at {get_time_now()}")
    #             await log_room.send(embed=embed)
                                        
    
    #command
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 858045603371286548:
            return
        
        dict_channels_from_jean_dominique = {
            "discuss" : None,
            "log-room" : None,
            "multiplayer-wait" : None
            }
        jean_dominique_category = message.channel.category
        # for channel in jean_dominique_category.channels:
        #     if channel.name in dict_channels_from_jean_dominique:
        #         dict_channels_from_jean_dominique[channel.name] = self.get_channel(channel.id)
        
        if message.guild.id in self.dict_jean_dominique_room_by_guild:
            dict_channels_from_jean_dominique = self.dict_jean_dominique_room_by_guild[message.guild.id]
        
        new_game_channel = discord.channel
        
        dict_hangman = {}
        
        is_user_in_game = self.check_user_in_game(
            user_id=message.author.id,
            guild_id=message.guild.id)
        
        guild_id = message.guild.id
        
        jd_user = self.get_user(858045603371286548)
        
        list_sub_command = []
        list_match_groups = []
        is_cmd_valid = False
        
        list_game_data = []
        
        cmd = str(message.content)
        command_object = Discord_Command(command=cmd)
        if not is_user_in_game:
            if not dict_channels_from_jean_dominique["discuss"] is None:
                if message.channel.id == dict_channels_from_jean_dominique["discuss"]:
                    match_obbject = command_object.get_match()
                    if not match_obbject is None:
                        list_match_groups = command_object.get_match_group_elements(
                            m=match_obbject)
                        is_cmd_valid = command_object.check_command_valid(list_match_groups[0])
                        if is_cmd_valid:
                            list_sub_command = command_object.get_subcommand_by_command(
                                list_match_groups[0])
                            if not list_sub_command is None:
                                is_subcommand_valid = command_object.check_subcommand(
                                    subcommand=list_match_groups[1],
                                    list_subcommand=list_sub_command
                                )
                                if list_match_groups[0] == "play" or list_match_groups[0] == "jouer":
                                    if list_match_groups[1] == "solo":
                                        try:
                                            dict_hangman = self._dict_hangmans_solo_by_guild[guild_id]
                                            
                                            word_object = Word()
                                            word_object._set_word_with_hidden_characters()
                                            
                                            channel_name = "solo "+str(self.count_solo_channels(channels_solo=jean_dominique_category.channels))
                                            new_game_channel = await jean_dominique_category.create_text_channel(name=channel_name)
                                            
                                            dict_hangman[message.author.id] = [word_object, new_game_channel]
                                            
                                            self._dict_hangmans_solo_by_guild[guild_id] = dict_hangman

                                            e = discord.Embed(title="HangmanGame", colour=0x7D1784)
                                            if len(word_object.list_chars_tryed)>0:
                                                e.add_field(name=self._dict_message["chars_tryed"], value=word_object.get_chars_tryed(), inline=False)
                                                
                                            e.add_field(name=self._dict_message["word_introduce"], value=word_object._word_with_hidden_characters, inline=False)

                                            await new_game_channel.send(embed=e)
                                            
                                            
                                            # e = discord.Embed(title=f"AT {datetime.now()}")
                                            # e.add_field(name="")
                                        except:
                                            # await message.reply("Désolé mais une erreur est survenue...")
                                            await message.reply(self._dict_message["error_unknow"])
                                    elif list_match_groups[1] == "multi":                                       
                                        word_object = Word()
                                        word_object.set_word()
                                        word_object._set_word_with_hidden_characters()
                                        multi = Multiplayer(word_obj=word_object)

                                        
                                        e = discord.Embed(title=f"Multi by {message.author.name}")
                                        e.set_author(name=message.author.name, icon_url=message.author.avatar.url)
                                        e.add_field(name="Controller emoji for join", value="For join")
                                        
                                        # emoji = discord.                                        
                                        msg_wait = await dict_channels_from_jean_dominique["multiplayer-wait"]
                                        multi.message = msg_wait
                                        multi.author_id = message.author.id  
                                        multi.players.append(message.author.id)                                      
                                        r = str
                                        #r = #reaction (str) controller
                                        await msg_wait.add_reaction(r)
                                        self._dict_hangmans_multi_by_guild[message.guild.id].append(multi)
                                elif list_match_groups[0] == "aide" or list_match_groups[0] == "help":
                                    if list_match_groups[1] == "play" or "jouer":
                                        await message.reply(self._dict_message["help_play"])
                                        
                                elif list_match_groups[0] == "stop" or list_match_groups[0] == "arreter":
                                    list_multi_game_from_this_guild = self._dict_hangmans_multi_by_guild[message.guild.id]
                                    is_author_get_game = False
                                    multi = Multiplayer
                                    for g in list_multi_game_from_this_guild:
                                        if not is_author_get_game:
                                            is_author_get_game = (g.author_id == message.author.id)
                                            multi = g
                                    if multi.is_playing:
                                        if is_author_get_game:
                                            chnl_game = multi.room_game_id
                                            await chnl_game.delete()
                                            await self.get_channel(dict_channels_from_jean_dominique["discuss"]).send("La partie à était annuler")
                                        else:
                                            await self.get_channel(dict_channels_from_jean_dominique["discuss"]).send("Désolé mais vous n'êtes pas propriétaire de salon multijoueur")
                                    else:
                                        if is_author_get_game:
                                            msg = multi.message
                                            await msg.delete()
                                        else:
                                            await self.get_channel(dict_channels_from_jean_dominique["discuss"]).send("Désolé mais vous n'êtes pas propriétaire de salon multijoueur")
                                        
                                elif list_match_groups[0] == "demarrer" or list_match_groups[0] == "start":
                                    list_multi_game_from_this_guild = self._dict_hangmans_multi_by_guild[message.guild.id]
                                    is_author_get_game = False
                                    multi = Multiplayer
                                    for g in list_multi_game_from_this_guild:
                                        if not is_author_get_game:
                                            is_author_get_game = (g.author_id == message.author.id)
                                            multi = g
                                
                                    if is_author_get_game:
                                        if len(multi.players) > 1:
                                            multi.is_playing = True
                                            word_object = multi._word_obj
                                            msg_wait = multi.message
                                            await msg_wait.delete()
                                            
                                            game_chnl = await jean_dominique_category.create_text_channel(name=f"{message.author.name}")
                                            multi.room_game_id = game_chnl
                                            
                                            str_players = multi.players.split(",")
                                            
                                            e = discord.Embed(title="Hangman Multi")
                                            e.set_author(name=message.author.name, icon_url=message.author.avatar.url)
                                            e.add_field(name="Players:",value=str_players)
                                            
                                            await game_chnl.send(embeds=e)
                                            
                                            e = self.get_solo_game_embed(word_object=word_object)
                                            
                                            player = self.get_user(multi.get_who_playing())
                                            e.add_field(name="À qui de jouer?", value=player.name, inline=False)

                                            await game_chnl.send(embeds=e)
                                            
                                        else:
                                            await self.get_channel(dict_channels_from_jean_dominique["discuss"]).send("Vous n'êtes pas encore assez de joueurs...")
                                    else:
                                        await self.get_channel(dict_channels_from_jean_dominique["discuss"]).send("Désolé mais vous n'êtes pas propriétaire de salon multijoueur")
                                
                                
                            elif list_match_groups[0] == "uninstall" or list_match_groups[0] == "desinstaller":
                                list_channels = self.get_category_channels_by_guild_id(
                                    guild_id=guild_id)
                                
                                for c in list_channels:
                                    chan = self.get_channel(c)
                                    jean_dominique_category = chan.category
                                    await chan.delete(reason="uninstall")
                                
                                if not jean_dominique_category is None:
                                    await jean_dominique_category.delete()
                                
                                del self.dict_jean_dominique_room_by_guild[message.guild.id]
                                if message.author.id in self._dict_hangmans_solo_by_guild:
                                    del self._dict_hangmans_solo_by_guild[message.author.id]
                                    
                                if message.author.id in self._dict_hangmans_multi_by_guild:
                                    del self._dict_hangmans_multi_by_guild[message.author.id]
                                    
                            elif list_match_groups[0] == "aide" or list_match_groups == [0] == "help":
                                msg = self._dict_message["introduce_help"]+"\n```fix\n"
                                for command_name, function_command in self._dict_help_msg.items():
                                    msg += f"{command_name} : {function_command}\n"
                                msg += "```"
                                await message.reply(msg)
                    else:
                        correction = Correction(message.content)
                        correction.set_correction()
                        prediction = correction.get_correction_from_list()
                        msg = self._dict_message["error_on_command_unknow"]
                        msg += "\n Peut-être cette commande:"+prediction
                        await message.reply(msg)
                        
            else:
                if message.content == "$reinstall":
                    if jean_dominique_category is None:
                        g = self.get_guild(message.guild.id)
                        jean_dominique_category = await g.create_category(name="jean-dominique")
                    
                    for channel in jean_dominique_category.channels:
                        if not channel.name in dict_channels_from_jean_dominique:
                            await channel.delete()
                        elif channel.name in dict_channels_from_jean_dominique:
                            dict_channels_from_jean_dominique[channel.name] = True
                
                    for channel,exists in dict_channels_from_jean_dominique.items():
                        if not exists:
                            await jean_dominique_category.create_text_channel(name=channel)                                                     
                    
                    dict_c = self.dict_jean_dominique_room_by_guild
                    if not message.guild.id in dict_c:
                        dict_c[message.guild.id] = None
                
                    if not message.author.id in self._dict_hangmans_solo_by_guild:
                        self._dict_hangmans_solo_by_guild[message.author.id] = {}
                    
                    if not message.author.id in self._dict_hangmans_multi_by_guild:
                        self._dict_hangmans_multi_by_guild[message.author.id] = {}

        else:
            dict_hangman = self._dict_hangmans_solo_by_guild[message.guild.id]
            list_hangman_multi = self._dict_hangmans_multi_by_guild[message.guild.id]
            if message.author.id in dict_hangman[message.author.id]:
                list_game_data = dict_hangman[message.author.id]
                if list_game_data[1].id == message.channel.id:
                    if message.content == "$stop":
                        await list_game_data[1].delete()
                        
                        del dict_hangman[message.author.id]
                        self._dict_hangmans_solo_by_guild = dict_hangman
                        
                        
                    else:
                        if len(message.content) == 1:
                            if str(message.content).isalpha():
                                word_object = list_game_data[0]
                                word_object.add_char_to_list_tryed(c=message.content)
                                word_object.refresh_word(char_typed=message.content)
                                user_win = word_object.check_win()
                                if not user_win:
                                    list_game_data[0] = word_object
                                    
                                    e = self.get_solo_game_embed(word_object=word_object)
                                    
                                    new_game_channel = list_game_data[1]
                                    await new_game_channel.send(embed=e)
                                else:
                                    await self.get_channel(dict_channels_from_jean_dominique["discuss"]).send(f"{message.author.mention} Bravo!!!")
                                    await list_game_data[1].delete()
                                    
                                    del dict_hangman[message.author.id]
                            else:
                                await message.delete()
                        else:
                            await message.delete()
            else: #check if the user is in multi_game of this guild (if not del his msg)
                #do multiplayer stuff here!
                is_user_foundt_in_ones_of_the_games = False
                multi = Multiplayer
                word_object = Word
                won = False
                for hangman_multi in list_hangman_multi:
                    if not is_user_foundt_in_ones_of_the_games:
                        is_user_foundt_in_ones_of_the_games = (message.author.id in hangman_multi.players)
                    multi = hangman_multi
                    
                if is_user_foundt_in_ones_of_the_games:
                    if message.author.id in multi.players:
                        name_author = multi.get_who_playing()
                        #check the tour of the user (if not del msg)
                        if name_author == message.author.name:
                            if len(message.content) == 1:
                                if str(message.content).isalpha:
                                    word_object = multi.get_word_object()
                                    word_object.add_char_to_list_tryed(message.content)
                                    word_object.refresh_word()
                                    won = word_object.check_win()
                                    pl = multi.get_who_playing.split(",")
                                    if won:
                                        #do stuff when the player win
                                        await self.get_channel(dict_hangman["discuss"]).send(f"Bravo à {pl}")
                                        
                                        chnl_game = multi.room_game_id
                                        await chnl_game.delete()
                                        
                                        
                                        list_hangman_multi[message.guild.id]
                                    else:
                                        multi.refresh_who_had_played()
                                        multi.set_word_object(word_object)
                                        
                                        for hangman_game in list_hangman_multi:
                                            if message.author.id in hangman_game.players:
                                                list_hangman_multi[hangman_game] = multi
                                                
                                        index_object_to_delete = list_hangman_multi[multi] 
                                        self._dict_hangmans_multi_by_guild[message.guild.id].pop()
                                else:
                                    await message.delete()
                            else:
                                await message.delete()
                        else:
                            await message.delete()
                    else:
                        await message.delete()
                else:
                    await message.delete()
    
    #embed
    
    def get_error_embed(self, message:discord.Message, error_type:str, prediction:str=None):
        e = discord.Embed(title="ERROR:") #colour=color_error_embed)
        e.set_author(name=message.author)
        if error_type == "error_unknow":
            e.add_field(name="WHY?", value="An error was raised but not handled")
        elif error_type == "error_on_command_unknow":
            e.add_field(name="WHY?", value="The input wasn't correct")

        e.add_field(name="WHO?", value=f"Raised by {message.author.name}")
        e.add_field(name="WHEN?", value=f"Raised at {datetime.datetime.utcnow()}")
        if not prediction is None:
            e.add_field(name="Correction (maybe)", value=prediction)
        return e
    
    def get_solo_game_embed(self, word_object):
        e = discord.Embed(title="HangmanGame", colour=0x7D1784)
        if len(word_object.list_chars_tryed)>0:
            e.add_field(name=self._dict_message["chars_tryed"], value=word_object.get_chars_tryed(), inline=False)
            
        e.add_field(name=self._dict_message["word_introduce"], value=word_object._word_with_hidden_characters, inline=False)
        
        return e
    
    #event
    @tasks.loop(minutes=10)
    async def _check_waiting_room(self):
        list_index_to_delete = []
        index = 0
        for guild in self.guilds:
            index = 0
            for hangman_game_waiting in guild:
                if hangman_game_waiting.id > datetime.datetime.utcnow():
                    hangman_game_waiting.pop(index)
                index += 1

    
    #gestion user
    def check_user_in_game(self, user_id:int, guild_id:int):
        dict_user_in_game = self._dict_hangmans_multi_by_guild[guild_id]
        if len(dict_user_in_game) > 0:
            return (user_id in dict_user_in_game.keys())
        else:
            return False
   
 
    #gestion channels    
    def delete_game_channel(self):
        pass
        
    
    def count_solo_channels(self, channels_solo:discord.CategoryChannel.channels):
        """
            Count channels with the name wich start with "solo" 
            
        Args:
            channels_solo (discord.CategoryChannel.channels): list of all channels from an category

        Returns:
            num(int): index of channels
        """
        num = 0
        for c in channels_solo:
            if c.name.startswith("solo"):
                num += 1
        return num
    
    def get_channel_id_by_name(self, name:str, list_channels_from_cat:discord.CategoryChannel.channels):
        """
            Search an channel by his name to get and return his id

        Args:
            name (str): name of the channel to search
            list_channels_from_cat (discord.CategoryChannel.channels): list of existing channels in a category

        Returns:
            int : id of the channel to find
        """
        id:int
        for c in list_channels_from_cat:
            if c.name == name:
                id = c.id
        return id
    
    def check_channel_exists(self, list_channels_from_cat:discord.CategoryChannel.channels ,channel_name:str):
        """
            Check if an channel exists in list of channels from an guild by the channel name wich is searched        

        Args:
            list_channels_from_cat (discord.CategoryChannel.channels): list of the the whole categories from an guild
            channel_name (str): name of the channel wich is researched

        Returns:
            bool : if the channel exists or not
        """
        channel_exist = False
        for c in list_channels_from_cat:
            if not channel_exist:
                channel_exist = (c.name == channel_name)
        
        return channel_exist
    
    #gestion category
    def get_category_by_id(self, list_categories:discord.CategoryChannel, category_id:int):
        """
            Search an category by her id and returned as discord.CategoryChannel object

        Args:
            list_categories (discord.CategoryChannel): list of whole category from an guild
            category_id (int): id of the category searched

        Returns:
            discord.CategoryChannel wich is the category that was searched 
        """
        category = discord.CategoryChannel
        for c in list_categories:
            if c.id == category_id:
                category = c
        
        return category
    
    def check_category_exists(self, list_categories:discord.CategoryChannel, category_name:str):
        """
            Check if the category name specified as
                parameters

        Args:
            category_name (str): name of the category
            list_categories (discord.CategoryChannel) : list of all existing categories on an guild

        Returns:
            bool: if the category exist or not
        """
        category_exist = False; category_id = None        
        category_exist = False
        for category in list_categories:
            if not category_exist:
                category_exist = (category.name == "jean-dominique")

        return category_exist
    
    def get_category_id(self, categories:discord.CategoryChannel, category_name:str):
        """
            Get the ID of the category by searching by her name in the whole list of
                the categories of an guild

        Args:
            categories (discord.CategoryChannel): list of all categories existing on a guild
            category_name (str): name of the category wich is researched

        Returns:
            int: id of the category searched
        """
        id = 0
        for category in categories:
            if category.name == category_name:
                id = category.id
        
        return id
    
    def get_category_channels_by_guild_id(self, guild_id:int):
        list_channels = []
        for g_id,chan in self.dict_jean_dominique_room_by_guild.items():
            if g_id == guild_id:
                for chan_id in chan.values():
                    list_channels.append(chan_id)
        
        return list_channels


debug = Application()
debug.run("ODU4MDQ1NjAzMzcxMjg2NTQ4.YNYbPQ.2gQNj0wtHgdW3Vapk-HpqjaOpgk")
