"""
Configure module for bot.

Created on 09.10.2021

@author: Ruslan Dolovanyuk

"""

import os


class Config:
    API_TOKEN_CLIENT = os.getenv('API_TOKEN_CLIENT')
    API_TOKEN_SERVICE = os.getenv('API_TOKEN_SERVICE')

    DB_URL = os.getenv('DB_URL')

    lang = 'ru'
