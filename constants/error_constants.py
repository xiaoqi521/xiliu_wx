# coding=utf-8

ERR_STATUS_SUCCESS = [0, u"成功 | Success"]
ERR_STATUS_FAIL = [-1, u"失败 | Fail"]

ERR_INVALID_PARAMETER = [10000, u"请求参数错误"]
#
ERR_SAVE_INFO_FAIL = [20000, u"保存数据错误"]
ERR_INVALID_DATA = [20001, u"数据不存在"]
ERR_INVALID_USER_PRIVILEGE = [20002, u"权限不够"]

ERR_USER_NOT_EXIST = [30101, u" 用户不存在"]
ERR_NAME_OR_PASSWORD = [30001, u"用户名或者密码错误"]
ERR_MOBILE_OR_PASSWORD = [30003, u"手机号或者密码错误"]
MOBILE_EXISTED = [30004, u"用户已存在"]

ERR_TOKEN_ERROR = [30105, u"TOKEN错误"]
ERR_SMS_CODE_TOO_FREQUENT = [30117, u"申请短信验证码过于频繁"]

ERR_INVALID_SMS_CODE = [40023, u"验证码不正确"]
ERR_MOBILE_ALREADY_EXIST = [40024, u"手机号已存在"]
ERR_MOBILE_NOT_EXIST = [40026, u"手机号不存在"]
ERR_INVALID_PASSWORD_REPEAT = [40025, u"密码与原密码相同，请重新输入"]
ERR_PASSWORD_ERROR = [40027, u"原密码错误"]

FILE_DoesNotExist = [40028, u"获取文件错误"]
FILE_IS_Existed = [40029, u"文件已存在"]

OBJECT_DOES_NOT_EXIST = [40400, u'对象不存在']
