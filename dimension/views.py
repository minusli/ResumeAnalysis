# coding: utf-8
from django.views.decorators.csrf import csrf_exempt

__author__ = 'ChrisLee'

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from utils import json_return
from utils import standard
from Main import settings
import json
from analysis import cal_profession_dimension, cal_stability_dimension


@csrf_exempt
def get_dimension(request):
    # 获取参数并且校验
    if "cv_id" not in request.POST:
        return json_return.json_return(False, standard.PARAM_LACK.code, standard.PARAM_LACK.msg + u": cv_id")
    if "source" not in request.POST:
        return json_return.json_return(False, standard.PARAM_LACK.code, standard.PARAM_LACK.msg + u": source")
    if request.POST["source"] not in [u"智联", u"英才", u"前程无忧"]:
        return json_return.json_return(False, standard.PARAM_RANGE.code, standard.PARAM_RANGE.msg + u": source只能是[智联,英才,前程无忧]之一")
    cv_id = request.POST["cv_id"]
    source = request.POST["source"]
    # 查询数据
    mongo_query = {"cv_id": cv_id, "source": source}
    data = settings.MongoConf.dimension_collection.find_one(mongo_query)
    settings.MongoConf.dimension_mongo.close()
    # 判断查询结果，并返回
    if not data:
        return json_return.json_return(False, standard.RETURN_DATA_NOT_EXISTE.code, standard.RETURN_DATA_NOT_EXISTE.msg + u": 没有指定简历的维度信息")
    else:
        if data and '_id' in data:
            data.pop("_id")
        return json_return.json_return(data=data)


@csrf_exempt
def cal_dimension(request):
    # 获取参数并校验
    try:
        data = request.body
        resume = json.loads(data)
    except Exception, e:
        return json_return.json_return(False, standard.PARAM_FORMAT.code, standard.PARAM_FORMAT.msg + u": 非标准JSON格式")
    if 'cv_id' not in resume:
        return json_return.json_return(False, standard.PARAM_LACK.code, standard.PARAM_LACK.msg + u": cv_id")
    if 'source' not in resume:
        return json_return.json_return(False, standard.PARAM_LACK.code, standard.PARAM_LACK.msg + u": source")
    if 'resume_id' not in resume:
        return json_return.json_return(False, standard.PARAM_LACK.code, standard.PARAM_LACK.msg + u": resume_id")
    if 'workExperienceList' not in resume:
        return json_return.json_return(False, standard.PARAM_LACK.code, standard.PARAM_LACK.msg + u": workExperienceList")
    # 开始计算
    try:
        cv_id = resume["cv_id"]
        source = resume["source"]
        resume_id = resume["resume_id"]
        profession = cal_profession_dimension(resume)
        stability = cal_stability_dimension(resume)
    except Exception, e:
        return json_return.json_return(False, standard.INNER_ERROR.code, standard.INNER_ERROR.msg + u": 计算维度出错")
    # 插入结果
    try:
        settings.MongoConf.dimension_collection.insert({
            "cv_id": cv_id,
            "source": source,
            "resume_id": resume_id,
            "profession": profession,
            "stability": stability,
        })
        settings.MongoConf.dimension_mongo.close()
    except Exception, e:
        return json_return.json_return(False, standard.INNER_ERROR.code, standard.INNER_ERROR.msg + u": 维度计算结果入库失败")
    # 返回
    return json_return.json_return()


