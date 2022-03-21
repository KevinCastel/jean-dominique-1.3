import re

from Word import Word
from multiplayer import Multiplayer

import os
from os import system

import discord_message
from discord_message import Discord_Command

from File import FileEnvironnement

msg_input = "Taper votre commande :"
inputed = ""
is_inputed_valid = False
is_subcommand_valid = False
match_object = re.match
list_match_groups = list()
list_sub_command = []

is_waiting_for_multi = False
in_game = False
game_won = False
word_object = Word

multi = Multiplayer()

file_lang = FileEnvironnement(lang="fr")
file_lang.parse_xml_file()
dict_message = file_lang._dict_data

run_app = True

while run_app:
    system("cls")
    if in_game:
        print("Charactères essayaient:",word_object.get_chars_tryed())
        print("Mot à trouver :", word_object._word_with_hidden_characters)
        
    
    inputed = input(msg_input)
    dc_object = Discord_Command(inputed)
    
    if not in_game:
        match_object = dc_object.get_match()

        if not match_object is None:
            list_match_groups = dc_object.get_match_group_elements(match_object)
            is_inputed_valid = dc_object.check_command_valid(list_match_groups[0])
            if is_inputed_valid:
                list_sub_command = dc_object.get_subcommand_by_command(
                    list_match_groups[0]
                )
                if not list_sub_command is None:
                    is_subcommand_valid = dc_object.check_subcommand(
                        subcommand=list_match_groups[1],
                        list_subcommand=list_sub_command
                    )
                    if list_match_groups[0] == "play" or list_match_groups[0] == "jouer":
                        if list_match_groups[1] == "solo":
                            try:
                                word_object = Word()
                                word_object.set_word()
                                word_object._set_word_with_hidden_characters()
                                msg_input = "Taper une lettre:"
                                in_game = True
                                print("Un jeu à était démarrer.")
                                
                            except:
                                print(dict_message["error_unknow"])
                        elif list_match_groups[1] == "multi":
                            try:
                                print("Un salon d'attente à était créer")
                                is_waiting_for_multi = True
                                msg_input = "(attente multi) taper votre commande:"
                            except:
                                print(dict_message["error_unknow"])
                elif list_match_groups[0] == "demarrer" or list_match_groups[0] == "start":
                    print("yes")
                    if is_waiting_for_multi:
                        print("Bien! Voyons cela alors:")
                        print(multi._time_creation)
                        print(multi._tc)
                    else:
                        print("Vous n'avez pas demander pour jouer en multi...")
        else:
            print(dict_message["error_on_command_unknow"])
    else:
        if inputed != "$stop":
            if len(inputed) == 1:
                if inputed.isalpha():
                    word_object.add_char_to_list_tryed(inputed)
                    word_object.refresh_word(inputed)
                    game_won = word_object.check_win()
                    if game_won:
                        word_object = Word
                        msg_input = "Taper votre commande :"
                        print("Bravo! Vous avez gagné")
                        in_game = False
                else:
                    print("Obliger d'une saisit alpha.")
            else:
                print("Juste une lettre suffit ;)")
        else:
            msg_input = "Taper une commande :"
            in_game = False
    
    run_app = (inputed != "exit" or in_game or is_waiting_for_multi)
    input("...")