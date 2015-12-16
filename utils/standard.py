# coding: utf-8
__author__ = 'ChrisLee'

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class SUCCESS:
    code = u'200-000'
    msg = u'SUCCESS'


class PARAM_ERROR:
    code = u'001-000'
    msg = u'参数问题'


class PARAM_LACK:
    code = u'001-001'
    msg = u'缺少参数错误'


class PARAM_FORMAT:
    code = u'001-002'
    msg = u'参数格式错误'


class PARAM_RANGE:
    code = u'001-003'
    msg = u'参数范围错误'


class RETURN_DATA_ERROR:
    code = u'004-000'
    msg = u'返回数据问题'


class RETURN_DATA_NOT_EXISTE:
    code = u'004-001'
    msg = u'返回数据不存在'


class INNER_ERROR:
    code = u'500-000'
    msg = u'服务器错误，请联系管理员'
