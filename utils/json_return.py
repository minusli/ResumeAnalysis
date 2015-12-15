# coding: utf-8
__author__ = 'ChrisLee'

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from django.http import HttpResponse
import json
import standard


def json_return(flag=True, msg=standard.SUCCESS.msg, data=None, code=standard.SUCCESS.code):
    return HttpResponse(json.dumps({'flag': flag, 'msg': msg, 'data': data, "code": code}))
