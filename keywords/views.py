# coding=utf-8
import json
import traceback
import jieba
import re
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from extract_tags import find_resume_by_id
from loadFile.constant_position import ConstantPosition
from utils import json_return, standard

category_keywords = ConstantPosition.category_keywords


@csrf_exempt
def resume_tag(request):
    # 获取参数并校验
    if 'cv_id' not in request.POST:
        return json_return.json_return(False, standard.PARAM_LACK.code, standard.PARAM_LACK.msg + u": cv_id")
    if 'source' not in request.POST:
        return json_return.json_return(False, standard.PARAM_LACK.code, standard.PARAM_LACK.msg + u": source")
    # if 'type' not in request.POST:
    #     return json_return.json_return(False, standard.PARAM_LACK.code, standard.PARAM_LACK.msg + u": type")
    cv_id = request.POST["cv_id"]
    source = request.POST["source"]
    # type = request.POST["type"]
    if source not in [u"智联", u"英才", u"前程无忧"]:
        return json_return.json_return(False, standard.PARAM_RANGE.code, standard.PARAM_RANGE.msg + u": source只能是[智联,英才,前程无忧]之一")
    # if type not in [u"产品", u"市场", u"技术", u"职能", u"设计", u"运营"]:
    #     return json_return.json_return(False, standard.PARAM_RANGE.code, standard.PARAM_RANGE.msg + u": type只能是六大类（产品，市场，技术，职能，设计，运营）之一")

    resume = find_resume_by_id(cv_id, source)
    if not resume:
        return json_return.json_return(False, standard.RETURN_DATA_NOT_EXISTE.code, standard.RETURN_DATA_NOT_EXISTE.msg + u": 没有该简历")
    tag_list = {}
    try:
        for t in ["产品", "市场", "技术", "职能", "设计", "运营"]:
            tag_list[t] = getResumeTag(resume, t)
    except Exception, e:
        return json_return.json_return(False, standard.INNER_ERROR.code, standard.INNER_ERROR.msg + u": 关键词计算错误")
    return json_return.json_return(data=tag_list)


def getResumeTag(doc, type):
    resume_info = doc["self_introduction"]
    if not resume_info:
        resume_info = ""
    workExperienceList = doc["workExperienceList"]
    projectList = doc["projectList"]
    if workExperienceList:
        for experience in workExperienceList:
            resume_info += experience["experience_desc"]
    if projectList:
        for project in projectList:
            resume_info += project["project_desc"]


    word_list = get_jd_analysis(resume_info, type)
    return word_list


def get_jd_analysis(jd, type):
    word_list = []
    LENGTH = 6
    try:
        words = set(jieba.cut(jd))
        english_words = get_english_words(words)
        word_list.extend(list(english_words))
        if len(word_list) >= LENGTH:
            return word_list[:6]
        category_words = set(category_keywords[type]) & words
        word_list.extend(list(category_words))
        word_list = list(set(word_list))
        if len(word_list) >= LENGTH:
            return word_list[:6]
    except:
        print "extract keywords error"
    return word_list


def get_english_words(words):
    english_words = set()
    for word in words:
        if word.encode('utf-8').isalnum():
            if not word.encode('utf-8').isdigit() and len(word) > 2:
                english_words.add(word)
            elif len(word) == 2:
                match = re.search(u"\d", word)
                if not match:
                    english_words.add(word)
            elif len(word) == 1:
                word = word.lower()
                if word == "c":
                    english_words.add(word)
    english_words -= {"br", "www", "cn", "1000CC"}
    return english_words
