# coding: utf-8
__author__ = 'ChrisLee'

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

import re
import datetime
from Main import settings
import pymongo
import time

# 平均每份工作经历的时长(月)
avg_months = 28.8504280074


def cal_dimension():
    in_mongo = settings.MongoConf.resume_mongo
    out_mongo = settings.MongoConf.dimension_mongo

    in_table = settings.MongoConf.resume_collection
    out_table = settings.MongoConf.dimension_collection

    today = datetime.datetime.today()
    temp_count = 0
    try:
        for resume in in_table.find({
            "$or": [{"dimension_flag": False}, {"dimension_flag": {"$exists": False}}],
        }, timeout=False).batch_size(20).skip(temp_count):
            cv_id = resume["cv_id"]
            source = resume["source"]
            resume_id = resume["resume_id"]
            profession = cal_profession_dimension(resume)
            stability = cal_stability_dimension(resume)
            try:
                out_table.insert({
                    "cv_id": cv_id,
                    "source": source,
                    "resume_id": resume_id,
                    "profession": profession,
                    "stability": stability,
                })
            except Exception, e:
                print e
            in_table.update({"_id": resume["_id"]}, {
                "$set": {
                    "dimension_flag": True
                }
            })
            temp_count += 1
            if temp_count % 10000 == 0:
                out_mongo.close()
                in_mongo.close()
                print today, "正在计算:", temp_count
    except Exception, e:
        print "error:", temp_count, e
    in_mongo.close()
    out_mongo.close()
    print today, "完成:", temp_count


def cal_profession_dimension(resume):
    # 计算加权工作月数
    months = 0.0
    weight = 0.8
    zhishu = 1.0
    zhishu_item = 1.8
    total_weight = 0
    try:
        for work in resume["workExperienceList"]:
            months += cal_delta_month(work["start_date"], work["end_date"]) * (weight ** (zhishu))
            total_weight += weight ** (zhishu)
            zhishu += zhishu_item
    except Exception, e:
        pass
    try:
        months /= total_weight
    except Exception, e:
        pass

    score = months / avg_months
    if score > 0.98:
        score = 0.98
    if score < 0.15:
        score = 0.15
    return score


def cal_stability_dimension(resume):
    score = 0.15  # 默认分数
    months = 0
    works = resume["workExperienceList"]
    try:
        # 取前三份工作经历的工作月数加权累加和，权值分别是0.5,0.3,0.2,
        months += cal_delta_month(works[0]["start_date"], works[0]["end_date"]) * 0.5
        months += cal_delta_month(works[1]["start_date"], works[1]["end_date"]) * 0.3
        months += cal_delta_month(works[2]["start_date"], works[2]["end_date"]) * 0.2
    except Exception, e:
        pass
    if months > avg_months:
        score = 1.1 - months / (10 * avg_months)
    else:
        score = months / avg_months
    if score > 0.98:
        score = 0.98
    if score < 0.15:
        score = 0.15
    return score


def cal_month(time_str):
    ret = 0
    if time_str:
        temps = re.split(ur"\D+", time_str)
        try:
            year = int(temps[0])
            assert year > 1000
            ret += year * 12
        except Exception, e:
            pass
        try:
            month = int(temps[1])
            assert 1 <= month <= 12
            ret += month
        except Exception, e:
            pass
        if ret == 0:
            today = datetime.date.today()
            ret = today.year * 12 + today.month
    return ret


def cal_delta_month(start, end):
    if start and end:
        start = cal_month(start)
        end = cal_month(end)
        delta = max(end - start, 0)
        return delta

    elif start and not end:
        start = cal_month(start)
        today = datetime.date.today()
        end = today.year * 12 + today.month
        delta = max(end - start, 0)
        return delta

    else:
        return 0


if __name__ == "__main__":
    """离线计算代码"""
    cal_dimension()

