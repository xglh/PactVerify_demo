#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/12 14:59
# @Author  : liuhui
# @Detail  :

from pactverify.matchers import Matcher, Like, EachLike, Enum, Term, PactVerify

# 定义契约格式
expect_format = Matcher({
    'code': 0,  # code key存在,值相等,code==0
    'msg': 'success',  # msg key存在,值相等,msg=='success'
    # [{}]结构
    'data': EachLike({
        "type_id": 249,  # type_id key存在,值类型相等,type(type_id) == type(249)
        "name": "王者荣耀",  # name key存在,值类型相等,type(name) == type("王者荣耀")
    }),
    'type': Enum([11,22]),
    'list': EachLike(11,minimum=2)
})

# 实际返回数据
actual_data = {
    "msg": "success",
    "code": 1,
    'type': 12,
    "data": [{
        # type_id类型不匹配
        "type_id": '249',
        "name": "王者荣耀"
    }, {
        # 缺少name
        "type_id": 250,
    }, {
        # 比契约定义多index字段
        "type_id": 251,
        "name": "刺激战场",
        "index": 111
    }
    ],
    'list': [11]
}
# hard_mode默认为true,hard_mode = True时,实际返回key必须严格等于预期key;hard_mode = False时,实际返回key包含预期key即可
mPactVerify = PactVerify(expect_format, hard_mode=True)
# 校验实际返回数据
mPactVerify.verify(actual_data)
# 校验结果  False
print(mPactVerify.verify_result)
''' 校验错误信息
错误信息输出actual_key路径：root.data.0.name形式
root为根目录,dict类型拼接key,list类型拼接数组下标(从0开始)
{   
    # 实际key少于预期key错误
	'key_less_than_expect_error': ['root.data.1.name'],
	# 实际key多与预期key错误,只在hard_mode = True时才报该错误
	'key_more_than_expect_error': ['root.data.2.index'],
	# 值不匹配错误
	'value_not_match_error': [{
			'actual_key': 'root.code',
			'actual_value': 1,
			'expect_value': 0
		}
	],
	# 类型不匹配错误
	'type_not_match_error': [{
			'actual_key': 'root.data.0.type_id',
			'actual_vaule': '249',
			'expect_type': 'int'
		}
	],
	# 数组长度不匹配错误
	'list_len_not_match_error': [{
			'actual_key': 'root.list',
			'actual_len': 1,
			'min_len': 2
		}
	],
	# 元祖不匹配错误
	'enum_not_match_error': [{
			'actual_key': 'root.type',
			'actual_value': 12,
			'expect_enum': [11, 22]
		}
	]
}

'''
print(mPactVerify.verify_info)
