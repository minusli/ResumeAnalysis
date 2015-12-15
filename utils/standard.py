# coding: utf-8
__author__ = 'ChrisLee'

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class SUCCESS:
    code = '200-000'
    msg = 'SUCCESS'


class PARAM_ERROR:
    code = '001-000'
    msg = '参数问题'


class PARAM_LACK:
    code = '001-001'
    msg = '缺少参数错误'


class PARAM_FORMAT:
    code = '001-002'
    msg = '参数格式错误'


class PARAM_RANGE:
    code = '001-003'
    msg = '参数范围错误'


class INNER_ERROR:
    code = '500-000'
    msg = '服务器错误，请联系管理员'
