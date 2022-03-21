import re

from os import system

from discord import command
from matplotlib.pyplot import cm

class Discord_Command:
    
    def __init__(self, command:str):
        super().__init__()
        
        self.regex = re
        
        self._command = command
        self._argument: list(str)
    
    def get_match(self):
        """
            Test patterns (list) wich are returned as group

        Returns:
            re.match.groups : list of match (re.match.groups())
        """
        list_patttern = [
            "^\$(?P<command>play|lang|help)\s\++(?P<sub_command>solo|multi|play|jouer|lang)", #en long-commands
            "^\$(?P<command>jouer|lang|aide)\s\++(?P<sub_command>solo|multi|play|jouer|lang)",#fr long-commands
            "^\$(?P<command>uninstall|stop|aide|reinstalle|desinstaller|demarrer|start)" #en/fr short-commands
        ]
        m = None
        for p in list_patttern:
            if m is None:
                m = re.match(pattern=p, string=self._command)
        return m
    
    def get_match_group_elements(self,m):
        return list(m.groups())

    def check_command_valid(self, cmd:str):
        return (cmd in ["desinstaller","help","lang", "play","jouer","stop","uninstall","aide","start","demarrer"])
    
    def get_subcommand_by_command(self, cmd:str):
        """
            Get subcommand of an command by the command

        Returns:
            list(str): list of subcommand from an command
        """
        dict_subcommand_by_command = {
            "demarrer" : None,
            "lang": ["fr","en"],
            "play": ["solo","multi"],
            "jouer": ["solo","multi"],
            "stop": None,
            "uninstall":None,
            "aide":["play","lang","jouer"],
            "help":["play","lang","jouer"],
            "start" : None
        }
        return dict_subcommand_by_command[cmd]

    def check_subcommand(self, subcommand:str, list_subcommand:str):
        return (subcommand in list_subcommand)
    