#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/20 20:23
# @Author  : liuhui
# @Detail  : 使用实例

from pactverify.matchers import Matcher, Like, EachLike, Term, Enum, PactVerify

# 定义契约格式
expect_format = Matcher({'k1': 'v1'})
# 实际数据
actual_data = {'k1': 'v2'}
# 实例化PactVerify类
mPactVerify = PactVerify(expect_format)
# 契约校验
mPactVerify.verify(actual_data)
# 校验结果  False
print(mPactVerify.verify_result)
# 输出校验信息
'''
{
	'key_not_macth_error': [],
	'value_not_match_error': [{
			'actual_value': 'v2',
			'expect_value': 'v1'
		}
	],
	'type_not_match_error': [],
	'list_len_not_match_error': [],
	'enum_not_match_error': []
}
'''
print(mPactVerify.verify_info)

# 预期11
expect_format_1 = Matcher(11)
# 预期1.0
expect_format_2 = Matcher(1.0)
# 预期'11'
expect_format_3 = Matcher('11')
# 预期返回数据actual为dict结构,actual['k1'] == 'v1'
expect_format_4 = Matcher({'k1': 'v1'})

expect_format = Like({
    # name字段值类型匹配
    'name': 'lilei',
    # age字段值匹配
    'age': Matcher(12),
})

# Matcher: 值匹配
expect_format = Matcher({
    "msg": "success",  # msg字段存在,并且msg="success"
    "code": 200,  # code字段存在,并且code="success"
    # Enum:枚举匹配
    'name': Enum(['lili', 'xiaohei']),  # name字段存在,并且name in ['lili', 'xiaohei']
    # Term:正则匹配
    "addr": Term(r'深圳*', example='深圳宝安'),  # name字段存在,并且addr正则匹配深圳*,example为正则表达式测试用str
    # Like:类型匹配
    "config": Like({
        'carModeCode': '11'  # carModeCode字段存在,并且type('carModeCode') == type('11')
    }),
    # EachLike: 数组值类型匹配
    "data": EachLike({
        "type_id": 249,  # type_id字段存在,并且type('type_id') == type(249)
        "name": "王者荣耀",
        "order_index": 1,
        "status": 1,
        "subtitle": " ",
        "game_name": "王者荣耀"
    }),
    # EachLike: 数组值类型匹配
    'data_2': EachLike({
        "type_id": 249,
        "name": "王者荣耀",
        "order_index": 1,
        "status": 1,
        "subtitle": " ",
        "game_name": "王者荣耀"
    }, minimum=2)  # 数组元素最小长度为2
})

# 实际返回数据
actual_data = {
    "msg": "success",
    "code": 0,
    'name': 'liuhui',
    'addr': '上海浦东',
    'config': {
        'carModeCode': 11
    },
    "data": [{
        "type_id": '249',
        "name": "王者荣耀",
        "order_index": 1,
        "status": 1,
        "subtitle": " ",
        "game_name": "王者荣耀"
    }, {
        "name": "绝地求生",
        "order_index": 2,
        "status": 1,
        "subtitle": " ",
        "game_name": "绝地求生"
    }, {
        "type_id": 251,
        "name": "刺激战场",
        "order_index": 3,
        "status": 1,
        "subtitle": " ",
    }
    ],
    'data_2': []
}
mPactVerify = PactVerify(expect_format)
# 校验实际返回数据
mPactVerify.verify(actual_data)
# 校验结果  False
print(mPactVerify.verify_result)
'''{
    # key不匹配,预期字段不存在
	'key_not_macth_error': ['type_id', 'game_name'],
	#值不匹配
	'value_not_match_error': [{
			'actual_value': 0,
			'expect_value': 200
		}, {
			'actual_value': '上海浦东',
			'expect_regex': '深圳*'
		}
	],
	# 类型不匹配
	'type_not_match_error': [{
			'actual_vaule': 11,
			'expect_type': 'str'
		}, {
			'actual_vaule': '249',
			'expect_type': 'int'
		}
	],
	# 数组长度不匹配
	'list_len_not_match_error': [{
			'actual_value': [],
			'min_len': 2
		}
	],
	# 枚举数据不匹配
	'enum_not_match_error': [{
			'actual_value': 'liuhui',
			'expect_enum': ['lili', 'xiaohei']
		}
	]
}'''
print(mPactVerify.verify_info)
