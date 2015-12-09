# coding: utf-8
from django.views.decorators.csrf import csrf_exempt

__author__ = 'ChrisLee'

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from utils import json_return
import pymongo
from Main import settings
import json
from analysis import cal_profession_dimension, cal_stability_dimension


@csrf_exempt
def get_dimension(request):
    # 获取参数并且校验
    cv_id = request.POST.get("cv_id", "")
    source = request.POST.get("source", "")
    if not isinstance(cv_id, basestring):
        return json_return.json_return(False, "cv_id 参数错误")
    if not isinstance(source, basestring):
        return json_return.json_return(False, "source 参数错误")
    mongo_query = {"cv_id": cv_id, "source": source}
    client = pymongo.Connection(settings.MongoConf.dimension_host, settings.MongoConf.dimension_port)
    client["admin"].authenticate("suanfa", "123456")
    table = client[settings.MongoConf.dimension_db][settings.MongoConf.dimension_table]
    data = table.find_one(mongo_query)
    if data and '_id' in data:
        data.pop("_id")
    return json_return.json_return(data=data)


@csrf_exempt
def cal_dimension(request):
    # 获取数据
    try:
        data = request.body
        print data
        resume = json.loads(data)
    except Exception, e:
        return json_return.json_return(False, "params error:" + str(e))
    # 准备mongo
    out_mongo = pymongo.Connection(settings.MongoConf.dimension_host, settings.MongoConf.dimension_port)
    out_mongo["admin"].authenticate("admin", "abc@123")
    out_mongo.safe = True
    out_table = out_mongo[settings.MongoConf.dimension_db][settings.MongoConf.dimension_table]
    # 开始计算
    try:
        cv_id = resume["cv_id"]
        source = resume["source"]
        resume_id = resume["resume_id"]
        profession = cal_profession_dimension(resume)
        stability = cal_stability_dimension(resume)
    except Exception, e:
        return json_return.json_return(False, "error in prepare data: " + str(e))
    # 插入结果
    try:
        out_table.insert({
            "cv_id": cv_id,
            "source": source,
            "resume_id": resume_id,
            "profession": profession,
            "stability": stability,
        })
    except Exception, e:
        return json_return.json_return(False, "error in insert: " + str(e))
    return json_return.json_return()


