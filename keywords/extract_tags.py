# coding: utf-8
__author__ = 'ChrisLee'

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from Main import settings


def find_resume_by_id(cv_id, source):
    return settings.MongoConf.resume_collection.find_one({"cv_id": cv_id, "source": source})
