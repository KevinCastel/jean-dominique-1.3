from xml.dom.expatbuilder import FILTER_SKIP
import xml.etree.ElementTree as ET

import os
from os import getcwd, listdir, system
from os.path import isfile

from discord import file

class FileEnvironnement:
    """
    Class FileEnvironnement is used for File Gestion.
    This class allows you to load and parse XML
    (Not polymorphism)    
    """
    
    def __init__(self, lang='en'):
        """
        

        Args:
            path ([type]): [description]
            lang (str, optional): [description]. Defaults to 'en'.
        """
        self.lang = lang
        #self.dict_command, self.dict_message, self.dict_error = {}, {}, {}
        
        self._dict_data = {}
        
        self.dict_path_file = {}
        self.dict_authorized_roles = {}
                
    def parse_xml_file(self):
        path = getcwd() + r"\lang.xml"
        
        print(path)
        list_child_to_explore = [
            "help", "game", "error"]
        if isfile(path):
            file = ET.parse(path)
            root = file.getroot()
            lang_root = root.findall(self.lang)
            
            for environnement_data in lang_root:
                for c in list_child_to_explore:
                    child = environnement_data.find(c)
                    for subchild in child:
                        self._dict_data[subchild.tag] = subchild.text
                        
    def get_global_help_message_to_dict(self):
        msg = self._dict_data["global_help"]
        list_msg = msg.split(";")
        dict_msg = {}
        for s in list_msg:
            l = s.split(":")
            dict_msg[l[0]] = l[1]
        return dict_msg
        
# file_lang = FileEnvironnement()
# file_lang.parse_xml_file()

# d = file_lang.get_global_help_message_to_dict()
