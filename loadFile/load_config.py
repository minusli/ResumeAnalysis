# coding: utf-8
__author__ = 'Administrator'
import os
import codecs

path = os.path.dirname(__file__)
read = codecs.open(path + "config.txt", 'r', encoding='utf-8')

class Config:
    config = {}
    @staticmethod
    def init_config():
        for line in read:
            if line.find('=') >= 0:
                key, value = line.split('=')
                Config.config[key.strip()] = value.strip()

Config.init_config()