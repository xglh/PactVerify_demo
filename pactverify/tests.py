# coding:utf-8

import unittest, json
from pactverify.matchers import Matcher, Like, EachLike, Term, Enum, PactVerify


class Test(unittest.TestCase):

    # Matcher基础配置-校验通过
    def test_matcher_base_1(self):
        expected_format = Matcher({
            'code': 0,
            'msg': 'success',
            'data': Matcher({'name': 'Jonas', 'age': 10, 'phone': 'bbb'}, jsonloads=True)
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            'data': "{\"name\": \"Jonas\", \"age\": 10, \"phone\": \"bbb\"}",
            'age_2': 'aaa'
        }

        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_matcher_base_1', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # Macher基础基础配置2-校验不通过
    def test_matcher_base_2(self):
        expected_format = Matcher({
            'code': 0,
            'msg': 'fail',
        })
        result_2 = [{
            'code': 0,
            'msg': 'success',
            'data': {'name': 'Jonas', 'age': 10, 'phone': 'bbb'},
            'age_2': 'aaa'
        }]
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_2)
        print('test_matcher_base_2', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # Macher配置
    def test_matcher_base_3(self):
        expected_format = Matcher({'k1': 'v1'})
        result_2 = {
            'k1': 'v2',
            'code': 0,
            'msg': 'success',
            'data': {'name': 'Jonas', 'age': 10, 'phone': 'bbb'},
            'age_2': 'aaa'
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_2)
        print('test_matcher_base_3', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # Macher配置
    def test_matcher_base_4(self):
        expected_format = Matcher(11)
        result_2 = 'aa'
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_2)
        print('test_matcher_base_4', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # Macher配置
    def test_matcher_base_5(self):
        expected_format = Matcher({
            'code': 0,
            'msg': 'success',
            'data': Like(
                {'name': 'Jonas11', 'age': 12, 'phone': 'bbbaa'}
            )
        })
        result_2 = {
            'code': 0,
            'msg': 'success',
            'data': {'name': 'Jonas', 'age': '11', 'phone': 'bbb'},
            'age_2': 'aaa'
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_2)
        print('test_matcher_base_5', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # keymissable
    def test_Matcher_keymissable_6(self):
        expected_format = Matcher({
            'code': Like(0, key_missable=True),
            'msg': Matcher('success', key_missable=True),
            'data': Like({
                'name': 'lilei',
                'age': Like('18', key_missable=True)
            }, key_missable=True)
        })
        result_1 = {
            'code': 0,
            'data': {
                'name': 'lilei',
            }
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_Matcher_keymissable_6', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # Macher配置
    def test_matcher_dict_emptiable_7(self):
        expected_format = Matcher({
            'code': 0,
            'msg': 'success',
            'data': Matcher(
                {'name': 'Jonas11', 'age': 12, 'phone': 'bbbaa'}, dict_emptiable=True
            )
        })
        result_2 = {
            'code': 0,
            'msg': 'success',
            'data': {},
            'age_2': 'aaa'
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_2)
        print('test_matcher_dict_emptiable_7', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # Macher配置
    def test_matcher_nullable_8(self):
        expected_format = Matcher({
            'code': 0,
            'msg': 'success',
            'data': Matcher(
                {'name': 'Jonas11', 'age': 12, 'phone': 'bbbaa'}, nullable=True
            )
        })
        result_2 = {
            'code': 0,
            'msg': 'success',
            'data': None
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_2)
        print('test_matcher_nullable_8', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # Macher配置
    def test_matcher_nullable_9(self):
        expected_format = Matcher({
            'code': 0,
            'msg': 'success',
            'data': Matcher(
                {'name': 'Jonas11', 'age': 12, 'phone': 'bbbaa'}, nullable=True
            )
        })
        result_2 = {
            'code': 0,
            'msg': 'success',
            'data': {'name': None, 'age': None, 'phone': None}
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_2)
        print('test_matcher_nullable_9', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # Like基础配置-校验通过
    def test_like_base_1(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'price': 1.0,
            'valid': True,
            'info': None,
            'info_1': [11],
            'info_2': {'k1': 'v1'}
        })
        result_1 = {
            'code': 1,
            'msg': 'haha',
            'price': 2.0,
            'valid': False,
            'info': None,
            'info_1': [1112],
            'info_2': []
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_like_base_1', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # Like配置-校验不通过
    def test_like_base_2(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'price': 1.0,
            'valid': True,
            'info': None,
            'info_1': [11],
            'info_2': {'k1': 'v1'},
            'info_3': 11
        })
        result_1 = {
            'code': 1,
            'msg': 'haha',
            'price': 2.0,
            'valid': False,
            'info': None,
            'info_1': [1112],
            'info_2': 11
        }
        # # print(expected_format)
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_like_base_2', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # Like-Term嵌套-校验不通过
    def test_like_base_3(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'price': 1.0,
            'valid': True,
            'info': None,
            'info_1': [11],
            'info_2': Term(r'\d{2}', 11)
        })
        result_1 = {
            'code': 1,
            'msg': 'haha',
            'price': 2.0,
            'valid': False,
            'info': None,
            'info_1': [1112],
            'info_2': 1
        }
        # # print(expected_format)
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_like_base_3', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # Like配置,目标数据格式不符合
    def test_like_base_4(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'price': 1.0,
            'valid': True,
            'info': None,
            'info_1': [11],
            'info_2': {'k1': 'v1'}
        })
        result_1 = 11
        # # print(expected_format)
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_like_base_4', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # Like-Like嵌套
    def test_like_base_5(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'price': 1.0,
            'valid': True,
            'info': None,
            'info_1': [11],
            'info_2': Like({
                "k1": 11,
                "k2": '22',
                'k3': 1.0
            })
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            'price': 1.0,
            'valid': True,
            'info': None,
            'info_1': [11],
            'info_2': {
                "k1": 11,
                "k2": 22
            }
        }
        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_like_base_5', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # Like-Like嵌套

    def test_like_base_6(self):
        expected_format = Matcher({
            "msg": "success",
            "code": 0,
            "data": Like({
                "target_user_info": Like({
                    "user_identity": 1,
                    "game_certify_info": EachLike({
                        "dict_id": 1,
                        "name": "王者荣耀",
                        "order_index": 1,
                        "url": "https://g.baojiesports.com/bps/89044cf2425d4b96b0540ee0bcc8123e-150-100.png",
                        "code": "1"
                    })
                }),
                "in_order_relation": 0,
                "order_sequence": "",
                "current_order_status": -1,
                "current_order_status_desc": "",
                "countdown": -1,
                "order_status_circulation": []
            })
        })
        result_1 = {
            "msg": "success",
            "code": 0,
            "data": {
                "target_user_info": {
                    "user_identity": 1,
                    "game_certify_info": [{
                        "dict_id": 1,
                        "name": "王者荣耀",
                        "order_index": 1,
                        "url": "https://g.baojiesports.com/bps/89044cf2425d4b96b0540ee0bcc8123e-150-100.png",
                        "code": "1"
                    }, {
                        "dict_id": 3,
                        "name": "绝地求生",
                        "order_index": 2,
                        "url": "https://g.baojiesports.com/bps/2f7e78df1ece496aa6a01df958bd7828-150-100.png",
                        "code": "3"
                    }
                    ]
                },
                "in_order_relation": 0,
                "order_sequence": "",
                "current_order_status": -1,
                "current_order_status_desc": "",
                "countdown": -1,
                "order_status_circulation": []
            }
        }
        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_like_base_6', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # Like-Matcher嵌套
    def test_like_base_7(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'price': 1.0,
            'valid': True,
            'info': None,
            'info_1': [11],
            'info_2': Matcher({'k1': 'v1'}),
            'info_3': Matcher(11),
            'info_4': Matcher(11)
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            'price': 1.0,
            'valid': True,
            'info': None,
            'info_1': [11],
            'info_2': {
                "k1": 11,
                "k2": 22
            },
            'info_3': 'aa',
            'info_4': []
        }
        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_like_base_7', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # Like基础配置-校验通过
    def test_like_jsonloads_1(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'price': 1.0,
            'valid': True,
            'info': None,
            'info_1': [11],
            'info_2': Like({'k1': 'v1'}, jsonloads=True)
        })
        result_1 = {
            'code': 1,
            'msg': 'haha',
            'price': 2.0,
            'valid': False,
            'info': None,
            'info_1': [1112],
            'info_2': "{\"k1\": \"v2\"}"
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_like_jsonloads_1', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # Term基础配置
    def test_term_base_1(self):
        expected_format = Term(r'^\d{2}$', 11)
        result_1 = 123
        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_term_base_1', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # Term key_missable
    def test_term_base_2(self):
        expected_format = Like({
            'name': 'lilei',
            'age': Term(r'^\d{2}$', example=11, key_missable=True)

        })
        result_1 = {
            'name': 'lilei'
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_term_base_2', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # Term key_missable
    def test_term_key_missable_3(self):
        expected_format = Like({
            'name': 'lilei',
            'age': Term(r'^\d{2}$', example=11, key_missable=True),
            'count': Term(r'^\d{2}$', example=11, key_missable=True),

        })
        result_1 = {
            'name': 'lilei',
            'count': 123
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_term_key_missable_3', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # Term key_missable
    def test_term_key_missable_4(self):
        expected_format = Term(r'^\d{2}$', example=11, key_missable=True)
        result_1 = 123
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_term_key_missable_4', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # Term nullable
    def test_term_nullable_5(self):
        expected_format = Term(r'^\d{2}$', example=11, nullable=True)
        result_1 = None
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_term_nullable_5', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # Term nullable
    def test_term_nullable_6(self):
        expected_format = Like({
            'code': Term(r'^\d{2}$', example=11, nullable=True)
        })

        result_1 = {
            'code': None
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_term_nullable_6', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # EachLike单层配置
    def test_eachlike_base_1(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'data': EachLike({
                "k1": 11,
                'k2': 'aa',
                'k3': 'haah'})
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            'data': [{
                "k1": 11,
                'k2': 'aa',
                'k3': True},
                {
                    "k1": 11,
                    'k2': 'aa'}
            ]
        }
        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        ##print('test_eachlike_base_1', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # EachLike多层嵌套
    def test_eachlike_base_2(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'data': EachLike(EachLike({
                "k1": 11,
                'k2': 'aa',
                'k3': 'haah'}))
        })
        result_1 = {
            'code': 'aa',
            'msg': 'success',
            'data': [[{
                "k1": 11,
                'k2': 'aa',
                'k3': True}
            ], [
                {
                    "k1": 11,
                    'k2': 'aa'}
            ]]
        }
        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        # print('test_eachlike_base_2', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # EachLike-Term嵌套
    def test_eachlike_base_3(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'data': EachLike(EachLike({
                "k1": 11,
                'k2': 'aa',
                'k3': Term('^\d{2}$', example=11)}))
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            'data': [[{
                "k1": 12123,
                'k2': 'aaasda',
                'k3': 123},
                {
                    "k1": 12324,
                    'k2': 'aa'}
            ], [{
                'k2': 'aa'}]]
        }
        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_eachlike_base_2', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # EachLike-len测试
    def test_eachlike_base_4(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'data': EachLike({
                "k1": 11,
                'k2': 'aa',
                'k3': Term('^\d{2}$', example=11)}, minimum=3)
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            'data': []
        }
        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_eachlike_base_4', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # EachLike-len测试
    def test_eachlike_base_5(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'data': EachLike({
                "k1": 11,
                'k2': 'aa',
                'k3': Term('^\d{2}$', example=11)}, minimum=1)
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            'data': [{
                "k1": 11,
                'k2': 'aa',
                'k3': '11'}]
        }
        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_eachlike_base_5', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # EachLike测试
    def test_eachlike_base_6(self):
        expected_format = EachLike({
            'user': 'lilei',
            'age': 10,
            'sex': Matcher('man')
        })
        result_1 = [{
            'user': 'lili',
            'age': 12,
            'sex': 'women'
        }]
        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_eachlike_base_6', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    def test_eachlike_base_7(self):
        expected_format = EachLike(
            11
        )
        result_1 = [11, 'aa']
        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        # print(expected_format.generate())

        mPactVerify.verify(result_1)
        # print('test_eachlike_base_7', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    def test_eachlike_base_8(self):
        expected_format = EachLike(EachLike(
            {'k1': 'v1'}
        ))
        result_1 = [[{'k1': 'v2'}]]
        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        # print(expected_format.generate())

        mPactVerify.verify(result_1)
        print('test_eachlike_base_8', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # EachLike最小长度允许为空
    def test_eachlike_base_9(self):
        expected_format = EachLike(
            {'k1': 'v1'}, minimum=0
        )
        result_1 = []
        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        # print(expected_format.generate())

        mPactVerify.verify(result_1)
        print('test_eachlike_base_9', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # EachLike最小长度允许为空
    def test_eachlike_base_10(self):
        expected_format = Matcher({
            "msg": "success",
            "code": 0,
            "data": Like({
                "basic_info": Like({
                    "game_code": 1,
                    "bj": Like({
                        "tags_strength": EachLike(EachLike({
                            "tag_id": 273,
                            "tag_name": "Carry全场",
                        }, minimum=0)),
                        "tags_service": EachLike(EachLike({
                            "tag_id": 294,
                            "tag_name": "开挂/作弊"
                        }, minimum=0)),
                        "tips_strength": EachLike("非常差！"),
                        "tips_service": EachLike("非常差！各方面都很差！")
                    }),
                    "bn": Like({
                        "tags_strength": EachLike(EachLike({
                            "tag_id": 273,
                            "tag_name": "Carry全场"
                        }, minimum=0)),
                        "tags_service": EachLike(EachLike({
                            "tag_id": 294,
                            "tag_name": "开挂/作弊"
                        }, minimum=0)),
                        "tips_strength": EachLike("非常差！"),
                        "tips_service": EachLike("非常差！各方面都很差！")
                    }),
                }),
                "baoji_info": EachLike({
                    "uid": "809c94b9",
                    "chicken_id": "87385416",
                    "username": "勇敢的暴鸡",
                    "avatar": "https://qn-bn-pub.kaiheikeji.com/baobao/defalutavatar/baobaodefalutavatar.png",
                    "sex": 1,
                    "identity": 1,
                    "baoji_level": 100,
                    "baoji_level_name": "普通暴鸡"
                })
            })
        })
        result_1 = {
            "msg": "success",
            "code": 0,
            "data": {
                "basic_info": {
                    "game_code": 1,
                    "bj": {
                        "tags_strength": [[], [], [], [], [{
                            "tag_id": 273,
                            "tag_name": "Carry全场"
                        }, {
                            "tag_id": 274,
                            "tag_name": "意识超群"
                        }, {
                            "tag_id": 287,
                            "tag_name": "制霸峡谷"
                        }
                        ]],
                        "tags_service": [[{
                            "tag_id": 294,
                            "tag_name": "开挂/作弊"
                        }, {
                            "tag_id": 293,
                            "tag_name": "恶意挂机"
                        }, {
                            "tag_id": 292,
                            "tag_name": "演员"
                        }, {
                            "tag_id": 291,
                            "tag_name": "色情骚扰"
                        }, {
                            "tag_id": 290,
                            "tag_name": "脏话连篇"
                        }, {
                            "tag_id": 289,
                            "tag_name": "言语辱骂"
                        }
                        ], [{
                            "tag_id": 294,
                            "tag_name": "开挂/作弊"
                        }, {
                            "tag_id": 293,
                            "tag_name": "恶意挂机"
                        }, {
                            "tag_id": 292,
                            "tag_name": "演员"
                        }, {
                            "tag_id": 291,
                            "tag_name": "色情骚扰"
                        }, {
                            "tag_id": 290,
                            "tag_name": "脏话连篇"
                        }, {
                            "tag_id": 289,
                            "tag_name": "言语辱骂"
                        }
                        ], [{
                            "tag_id": 295,
                            "tag_name": "态度冷淡"
                        }, {
                            "tag_id": 296,
                            "tag_name": "频繁索要好评"
                        }, {
                            "tag_id": 297,
                            "tag_name": "服务时长不足"
                        }
                        ], [{
                            "tag_id": 295,
                            "tag_name": "态度冷淡"
                        }, {
                            "tag_id": 296,
                            "tag_name": "频繁索要好评"
                        }, {
                            "tag_id": 297,
                            "tag_name": "服务时长不足"
                        }
                        ], [{
                            "tag_id": 278,
                            "tag_name": "真·声控福利"
                        }, {
                            "tag_id": 280,
                            "tag_name": "沉着冷静"
                        }, {
                            "tag_id": 279,
                            "tag_name": "电竞BB机"
                        }, {
                            "tag_id": 282,
                            "tag_name": "教学有干货"
                        }, {
                            "tag_id": 283,
                            "tag_name": "温柔"
                        }
                        ]],
                        "tips_strength": ["非常差！", "比较差", "一般，还需改善", "很不错，仍可改善", "非常好，6到飞起"],
                        "tips_service": ["非常差！各方面都很差！", "不满意，比较差", "一般，还需改善", "满意，仍可改善", "非常满意"]
                    },
                    "bn": {
                        "tags_strength": [[], [], [], [], [{
                            "tag_id": 273,
                            "tag_name": "Carry全场"
                        }, {
                            "tag_id": 274,
                            "tag_name": "意识超群"
                        }, {
                            "tag_id": 287,
                            "tag_name": "制霸峡谷"
                        }
                        ]],
                        "tags_service": [[{
                            "tag_id": 294,
                            "tag_name": "开挂/作弊"
                        }, {
                            "tag_id": 293,
                            "tag_name": "恶意挂机"
                        }, {
                            "tag_id": 292,
                            "tag_name": "演员"
                        }, {
                            "tag_id": 291,
                            "tag_name": "色情骚扰"
                        }, {
                            "tag_id": 290,
                            "tag_name": "脏话连篇"
                        }, {
                            "tag_id": 289,
                            "tag_name": "言语辱骂"
                        }
                        ], [{
                            "tag_id": 294,
                            "tag_name": "开挂/作弊"
                        }, {
                            "tag_id": 293,
                            "tag_name": "恶意挂机"
                        }, {
                            "tag_id": 292,
                            "tag_name": "演员"
                        }, {
                            "tag_id": 291,
                            "tag_name": "色情骚扰"
                        }, {
                            "tag_id": 290,
                            "tag_name": "脏话连篇"
                        }, {
                            "tag_id": 289,
                            "tag_name": "言语辱骂"
                        }
                        ], [{
                            "tag_id": 295,
                            "tag_name": "态度冷淡"
                        }, {
                            "tag_id": 296,
                            "tag_name": "频繁索要好评"
                        }, {
                            "tag_id": 297,
                            "tag_name": "服务时长不足"
                        }
                        ], [{
                            "tag_id": 295,
                            "tag_name": "态度冷淡"
                        }, {
                            "tag_id": 296,
                            "tag_name": "频繁索要好评"
                        }, {
                            "tag_id": 297,
                            "tag_name": "服务时长不足"
                        }
                        ], [{
                            "tag_id": 278,
                            "tag_name": "真·声控福利"
                        }, {
                            "tag_id": 279,
                            "tag_name": "电竞BB机"
                        }, {
                            "tag_id": 283,
                            "tag_name": "温柔"
                        }, {
                            "tag_id": 284,
                            "tag_name": "敲可爱"
                        }, {
                            "tag_id": 288,
                            "tag_name": "就很甜"
                        }, {
                            "tag_id": 285,
                            "tag_name": "峡谷御姐"
                        }
                        ]],
                        "tips_strength": ["非常差！", "比较差", "一般，还需改善", "很不错，仍可改善", "非常好，6到飞起"],
                        "tips_service": ["非常差！各方面都很差！", "不满意，比较差", "一般，还需改善", "满意，仍可改善", "非常满意"]
                    }
                },
                "baoji_info": [{
                    "uid": "809c94b9",
                    "chicken_id": "87385416",
                    "username": "勇敢的暴鸡",
                    "avatar": "https://qn-bn-pub.kaiheikeji.com/baobao/defalutavatar/baobaodefalutavatar.png",
                    "sex": 1,
                    "identity": 1,
                    "baoji_level": 100,
                    "baoji_level_name": "普通暴鸡"
                }
                ]
            }
        }

        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        # print(expected_format.generate())

        mPactVerify.verify(result_1)
        print('test_eachlike_base_10', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # EachLike最小长度允许为空
    def test_eachlike_base_11(self):
        expected_format = EachLike(
            {'k1': Matcher('v1')}
        )
        result_1 = [{'k1': 'v1'}, {'k1': 'v2'}]
        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        # print(expected_format.generate())

        mPactVerify.verify(result_1)
        print('test_eachlike_base_9', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # EachLike单层配置
    def test_eachlike_jsonloads_12(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'data': EachLike({
                'k1': 11,
                'k2': 'aa',
                'k3': 'haah'}, jsonloads=True)
        }, jsonloads=True)
        result_1 = '''{\"code\":0,\"msg\":\"success\",\"data\":"[{\"k1\":11,\"k2\":\"aa\",\"k3\":true}]"}'''
        # # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_eachlike_jsonloads_12', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # EachLike key_missable
    def test_eachlike_key_missable_13(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'data': EachLike({
                'k1': 11,
                'k2': 'aa',
                'k3': 'haah'}, key_missable=True)
        })
        result_1 = {
            'code': 0,
            'msg': 'success'
        }
        mPactVerify = PactVerify(expected_format)

        mPactVerify.verify(result_1)
        print('test_eachlike_key_missable_13', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # EachLike key_missable
    def test_eachlike_key_missable_14(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'data': EachLike({
                'k1': 11,
                'k2': 'aa',
                'k3': 'haah'}, key_missable=True)
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            'data': [{
                'k1': '11',
                'k2': 'aa',
                'k3': 'haah'
            }]
        }
        mPactVerify = PactVerify(expected_format)

        mPactVerify.verify(result_1)
        print('test_eachlike_key_missable_14', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # EachLike key_missable
    def test_eachlike_key_missable_15(self):
        expected_format = EachLike({
            'k1': 11,
            'k2': 'aa',
            'k3': 'haah'}, key_missable=True)
        result_1 = []
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_eachlike_key_missable_14', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # EachLike key_missable
    def test_eachlike_key_nullable_16(self):
        expected_format = EachLike(11, nullable=True)
        result_1 = None
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_eachlike_key_nullable_16', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # EachLike key_missable
    def test_eachlike_key_nullable_17(self):
        expected_format = Like({
            'list': EachLike(11, nullable=True)
        })
        result_1 = {
            'list': None
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_eachlike_key_nullable_17', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # EachLike key_missable
    def test_eachlike_key_nullable_18(self):
        expected_format = Like({
            'list': EachLike({'age': 18}, nullable=True)
        })
        result_1 = {
            'list': [{
                'age': None
            }]
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_eachlike_key_nullable_18', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # EachLike key_missable
    def test_eachlike_key_nullable_19(self):
        expected_format = Like({
            'list': EachLike({'age': 18}, nullable=True)
        })
        result_1 = {
            'list': [None]
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_eachlike_key_nullable_19', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # EachLike key_missable
    def test_eachlike_key_nullable_20(self):
        expected_format = Like({
            'list': EachLike(EachLike({'age': 18}, nullable=True), nullable=False)
        })
        result_1 = {
            'list': [[{
                'age': None
            }], [None]]
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_eachlike_key_nullable_20', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # enum校验_1
    def test_enum_base_1(self):
        expected_format = Enum([11, 22])
        result_1 = 13

        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_enum_base_1', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # enum校验_2
    def test_enum_base_2(self):
        expected_format = Enum([{'k1': 'v1'}, {'k1': 'v2'}])
        result_1 = {'k2': 'v2'}

        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_enum_base_2', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # enum校验_3
    def test_enum_base_3(self):
        expected_format = Matcher({
            'code': 0,
            'msg': 'success',
            'age': Enum([11, 22, 33])
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            'age': 11
        }
        # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_enum_base_1', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # enum校验_4
    def test_enum_base_4(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'age': Enum([11, 22])
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            'age': 11
        }
        # print(expected_format.generate())
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_enum_base_1', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # enum校验_5
    def test_enum_base_5(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'data': EachLike({'name': Enum(['liuhui', 'xiaoli'])})
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            'data': [{'name': 'liuhui'}]
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_enum_base_1', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # enum校验_6
    def test_enum_base_6(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'data': Enum([11, 22, 33], iterate_list=True)
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            'data': [11, 12]
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_enum_base_6', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # enum校验_7
    def test_enum_base_7(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            "reasonList": Enum([{
                "key": "InstallAssurePolicy",
                "name": "保装车",
                "reason": "第1项:品质不支持;第2项:品质不支持"
            }, {
                "key": "QualityAssurePolicy",
                "name": "商家质保",
                "reason": "null;第2项:质保1年:品质不支持;第3项:质保1年:品质不支持"
            }, {
                "key": "ReturnAndChangePolicy",
                "name": "包退货",
                "reason": "null;第2项:7天包退货:品质不支持;第3项:7天包退货:品质不支持;第4项:7天包退货:品质不支持"
            }, {
                "key": "CassQualityAssurePolicy",
                "name": "开思质保",
                "reason": "质保六个月第1项：品质不支持;质保六个月第2项：标准名称不支持;质保六个月第3项：品质不支持"
            }, {
                "key": "CompensationPolicy",
                "name": "假一罚N",
                "reason": "暂无配置"
            }], iterate_list=True)
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            "reasonList": [{
                "key": "InstallAssurePolicy",
                "name": "保装车",
                "reason": "第1项:品质不支持;第2项:品质不支持"
            }, {
                "key": "QualityAssurePolicy",
                "name": "商家质保",
                "reason": "null;第2项:质保1年:品质不支持;第3项:质保1年:品质不支持"
            }, {
                "key": "ReturnAndChangePolicy",
                "name": "包退货",
                "reason": "null;第2项:7天包退货:品质不支持;第3项:7天包退货:品质不支持;第4项:7天包退货:品质不支持"
            }, {
                "key": "CassQualityAssurePolicy",
                "name": "开思质保",
                "reason": "质保六个月第1项：品质不支持;质保六个月第2项：标准名称不支持;质保六个月第3项：品质不支持"
            }, {
                "key": "CompensationPolicy",
                "name": "假一罚N",
                "reason": "暂无配置"
            }
            ]
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_enum_base_7', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # enum校验_6
    def test_enum_base_8(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'data': Enum([11, 22, 33], iterate_list=True)
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            'data': 11
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_enum_base_8', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    def test_enum_jsonloads_9(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'data': Enum([11, 22, 33], iterate_list=True, jsonloads=True)
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            'data': "[11,22]"
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_enum_jsonloads_9', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    def test_enum_key_missable_9(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'data': Enum([11, 22, 33], iterate_list=True, jsonloads=True, key_missable=True)
        })
        result_1 = {
            'code': 0,
            'msg': 'success'
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_enum_key_missable_9', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    def test_enum_key_missable_10(self):
        expected_format = Enum([11, 22, 33], key_missable=True)
        result_1 = None
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_enum_key_missable_10', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    def test_enum_nullable_11(self):
        expected_format = Enum([11, 22, 33], nullable=True)
        result_1 = None
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_enum_nullable_11', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    def test_enum_nullable_12(self):
        expected_format = Like({
            'code': Enum([11, 22, 33], nullable=True)
        })

        result_1 = {
            'code': 23
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_enum_nullable_12', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # like_nulable校验
    def test_like_nulable_1(self):
        expect_format = Like({
            'k1': 'v1'
        }, nullable=True)
        # 实际数据
        actual_data = {'k1': None}
        mPactVerify = PactVerify(expect_format)
        mPactVerify.verify(actual_data)
        print('test_like_nulable_1', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # like_nulable校验
    def test_like_nulable_2(self):
        expect_format = Like(11, nullable=True)
        actual_data = None
        mPactVerify = PactVerify(expect_format)
        mPactVerify.verify(actual_data)
        print('test_like_nulable_2', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # like_nulable校验
    def test_like_nulable_3(self):
        expect_format = Like({
            'code': 0,
            'data': Like({
                'k1': Like('v1', nullable=True),
                'k2': 'v2'
            }, nullable=False)
        }, nullable=False)
        actual_data = {
            'code': 0,
            'data': {
                'k1': None,
                'k2': ''
            }
        }
        mPactVerify = PactVerify(expect_format)
        mPactVerify.verify(actual_data)
        print('test_like_nulable_3', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # like_dict_emptiable校验
    def test_dict_emptiable_1(self):
        expect_format = Like({
            'code': 0,
            'data': Like({
                'k1': 'v1',
                'info': Like({
                    'name': 'li'
                })
            }, dict_emptiable=True)
        })
        actual_data = {
            'code': 0,
            'data': {}
        }
        mPactVerify = PactVerify(expect_format)
        mPactVerify.verify(actual_data)
        print('test_dict_emptiable_1', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # like_dict_emptiable校验
    def test_dict_emptiable_2(self):
        expect_format = Like({
            'code': 0,
            'data': Like({
                'k1': 'v1',
                'info': Like({
                    'name': 'li'
                }, dict_emptiable=True)
            }, dict_emptiable=True)
        })
        actual_data = {
            'code': 0,
            'data': {
                'k1': 'v1',
                'info': {}
            }
        }
        mPactVerify = PactVerify(expect_format)
        mPactVerify.verify(actual_data)
        print('test_dict_emptiable_2', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # like_dict_emptiable校验
    def test_dict_emptiable_3(self):
        expect_format = Like({
            'code': 0,
            'data': Like(11, dict_emptiable=True)
        })
        actual_data = {
            'code': 0,
            'data': {}
        }
        mPactVerify = PactVerify(expect_format)
        mPactVerify.verify(actual_data)
        print('test_dict_emptiable_3', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # keymissable
    def test_keymissable_2(self):
        expected_format = Matcher(11, key_missable=True)
        result_1 = 'aa'
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_keymissable_2', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # keymissable
    def test_keymissable_3(self):
        expected_format = Like(11, key_missable=True)
        result_1 = 'aa'
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_keymissable_2', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # keymissable
    def test_keymissable_4(self):
        expected_format = Like({
            'list': EachLike({
                "id": "1158622356088750081",
                "created_at": 1565072071000,
                "updated_at": 1565072071000,
                "user_id": "1158291201286074370",
                "vin_code": "1FA6P8TH9G5328025",
                "query_fee": 0.0,
                "query_status": 0,
                "description": Like("没有查询到VIN码对应的车辆信息", key_missable=False),
                "key_info": Like({
                    "brandName": "路虎", "brandId": "LANDROVER"
                }, key_missable=False, jsonloads=True),
                "result_id": "0"
            })
        })
        result_1 = {"list": [{
            "id": "1158622356088750081",
            "created_at": 1565072071000,
            "updated_at": 1565072071000,
            "user_id": "1158291201286074370",
            "vin_code": "1FA6P8TH9G5328025",
            "query_fee": 0.0,
            "query_status": 0,
            "description": "没有查询到VIN码对应的车辆信息",
            "result_id": "0"
        }, {
            "id": "1158622352030654465",
            "created_at": 1565072070000,
            "updated_at": 1565072070000,
            "user_id": "1158291201286074370",
            "vin_code": "SALWR2WF9EA323304",
            "query_fee": 0.0,
            "query_status": 1,
            "result_id": "1158622351816744962",
            "key_info": "{\"brandName\":\"路虎\",\"brandId\":\"LANDROVER\"}"
        }]}
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_keymissable_4', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True


if __name__ == '__main__':
    unittest.main()
