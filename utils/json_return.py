# coding: utf-8
__author__ = 'ChrisLee'

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from django.http import HttpResponse
import json


def json_return(flag=True, msg="SUCCESS", data={}):
    return HttpResponse(json.dumps({'flag': flag, 'msg': msg, 'data': data}))
