# coding: utf-8
from django.views.decorators.csrf import csrf_exempt

__author__ = 'ChrisLee'

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from utils import json_return
import pymongo
from Main import settings


@csrf_exempt
def search_dimension_by_cvid(request):
    # 获取参数并且校验
    ids = request.POST.get("ids", "")
    if not isinstance(ids, basestring):
        return json_return.json_return(False, "参数错误")
    ids = ids.split(",")
    data = []  # 默认数据返回格式
    if ids:
        mongo_query = {
            "$or": [{"cv_id": _id} for _id in ids]
        }

        data = list(pymongo.Connection(settings.MongoConf.dimension_host, settings.MongoConf.dimension_port)[
            settings.MongoConf.dimension_db][settings.MongoConf.dimension_table].find(mongo_query))
    return json_return.json_return(data=data)
