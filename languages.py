"""
Languages module for bots.

Created on 09.10.2021

@author: Ruslan Dolovanyuk

"""

import json


class Languages:
    supported = None
    current = None


def local(section: str, phrase: str) -> str:
    return Languages.current[section].get(phrase, '')


def load_language(lang: str) -> None:
    with open('languages.json', 'r', encoding='utf-8') as langs:
        data = json.load(langs)
        Languages.supported = data['languages']
        Languages.current = data[lang]
