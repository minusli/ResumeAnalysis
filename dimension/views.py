# coding: utf-8
from django.views.decorators.csrf import csrf_exempt

__author__ = 'ChrisLee'

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


from utils import json_return


@csrf_exempt
def searchDimension(reqeust):
    return json_return.json_return()



