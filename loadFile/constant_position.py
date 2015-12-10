# coding: utf-8
__author__ = 'Administrator'
import os
import codecs
import time
path = os.path.dirname(__file__) + u"/position"

class ConstantPosition:
    category_keywords = {}
    position_keywords = {}
    @staticmethod
    def init_position_jd():
        '''
        初始化五大类职位
        '''
        category_path = path + u"/category"
        for dir in os.listdir(category_path):
            ConstantPosition.position_keywords.setdefault(dir, {})
            ConstantPosition.category_keywords.setdefault(dir, [])
            temp_path = os.path.join(category_path, dir)
            for fileName in os.listdir(temp_path):
                position = fileName.split(u'.txt')[0].upper()
                ConstantPosition.position_keywords[dir].setdefault(position, [])
                infile = codecs.open(temp_path + "/" + fileName, 'r', encoding='utf-8')
                List = [line.strip().split('\t')[0].upper() for line in infile]
                List.append(position)
                ConstantPosition.position_keywords[dir][position].extend(List)
                ConstantPosition.category_keywords[dir].extend(List)
                infile.close()


    careerList = []
    @staticmethod
    def init_carrer():
        """
        初始化拉钩标准职位（含有英文职位，统一用大写）
        """
        infile = codecs.open(path+"/career.txt", 'r', encoding='utf-8')
        ConstantPosition.careerList = [line.strip().upper() for line in infile]


    field_keywords = []
    @staticmethod
    def init_filed_keywords():
        """
        初始化行业关键词（不含有英文领域词）
        """
        infile = codecs.open(path+"/field_words.txt", 'r', encoding='utf-8')
        ConstantPosition.field_keywords = infile.read().split(' 1\r\n')

    direction_keywords = []
    @staticmethod
    def init_direction_words():
        """
        初始化方向词  姜龙龙
        """
        infile = codecs.open(path+"/new_direction_words.txt", 'r', encoding='utf-8')
        ConstantPosition.direction_keywords = infile.read().split('\r\n')

    @staticmethod
    def init():
        tt = time.time()
        ConstantPosition.init_position_jd()
        ConstantPosition.init_carrer()
        ConstantPosition.init_filed_keywords()
        ConstantPosition.init_direction_words()
        print "init position file use time: " + str(time.time() - tt)


ConstantPosition.init()