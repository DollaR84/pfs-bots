"""
API methods for chat PayForSay Bot.

created on 12.10.2021

@author: Ruslan Dolovanyuk

"""

from config import Config as cfg


def get_another_token(current_token):
    result = None
    if current_token == cfg.API_TOKEN_CLIENT:
        result = cfg.API_TOKEN_SERVICE
    elif current_token == cfg.API_TOKEN_SERVICE:
        result = cfg.API_TOKEN_CLIENT
    return result


def get_type_bot(current_token):
    result = None
    if current_token == cfg.API_TOKEN_CLIENT:
        result = 'client'
    elif current_token == cfg.API_TOKEN_SERVICE:
        result = 'service'
    return result


def is_client_bot(current_token):
    return bool(get_type_bot(current_token) == 'client')


def is_service_bot(current_token):
    return bool(get_type_bot(current_token) == 'service')
