#!/usr/bin/env python3

from linkedin_api import Linkedin
import ConfigParser


api = Linkedin("email", "mot_de_passe")  



config = ConfigParser.ConfigParser()
config.readfp(open(r'./config'))
path1 = config.get('My Section', 'path1')
path2 = config.get('My Section', 'path2')
path3 = config.get('My Section', 'path3')