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

        mPactVerify = PactVerify(expected_format, hard_mode=False)
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
        mPactVerify = PactVerify(expected_format, hard_mode=False)
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

    def test_enum_iterate_list_13(self):
        expected_format = Like({
            'code': 0,
            'msg': 'success',
            'data': Enum([11, 22, 33], iterate_list=True)
        })
        result_1 = {
            'code': 0,
            'msg': 'success',
            'data': []
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_enum_iterate_list_13', json.dumps(mPactVerify.verify_info, indent=4))
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
                "description": Like("没有查询到VIN码对应的车辆信息", key_missable=True),
                "key_info": Like({
                    "brandName": "路虎", "brandId": "LANDROVER"
                }, key_missable=True, jsonloads=True),
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

    # keymissable
    def test_error_1(self):
        expected_format = Matcher(
            {
                "errorCode": 0,
                "data": Like(
                    {
                        "allRights": EachLike(
                            {
                                "level": 0,
                                "levelIcon": "string",
                                "rightsLevelGrowthMin": 0,
                                "rightsLevelGrowthMax": 0,
                                "currentLevelValue": 0,
                                "isCurrentLevel": True,
                                "isNextGrowthLevel": 0,  # 把这里改成int值
                                "rightDetail": EachLike(
                                    {
                                        "name": "string",
                                        "description": "string",
                                        "rightIcon": "string",
                                        "code": "string"
                                    }
                                )
                            }
                        )
                    }
                )
            }
        )
        result_1 = {
            "errorCode": 0,
            "data": {
                "allRights": [
                    {
                        "level": 0,
                        "levelIcon": "string",
                        "rightsLevelGrowthMin": 0,
                        "rightsLevelGrowthMax": 0,
                        "currentLevelValue": 0,
                        "isCurrentLevel": True,
                        "isNextGrowthLevel": True,
                        "rightDetail": [
                            {
                                "name": "string",
                                "description": "string",
                                "rightIcon": "string",
                                "code": "string"
                            }
                        ]
                    }
                ]
            }
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_error_1', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # hard_mode
    def test_hard_mode_1(self):
        expected_format = Like({
            'k1': 'v1',
            'k3': Like('v3', key_missable=True),
            'k4': Like({
                'v41': 11
            }),
            'k5': Like({
                'v51': 11
            }, dict_emptiable=True),
            'k6': Like('v6', nullable=True)
        })
        result_1 = {
            'k1': 'v1',
            'k2': 'v2',
            'k4': {
                'v41': 22
            },
            'k5': {},
            'k6': 11
        }
        # hard_mode=True,实际返回字段与契约定义字段要完全一致；hard_mode=False,实际返回字段可多于契约定义字段
        mPactVerify = PactVerify(expected_format, hard_mode=True)
        mPactVerify.verify(result_1)
        print('test_hard_mode_1', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # hard_mode
    def test_hard_mode_2(self):
        expected_format = Like({
            'k1': 'v1',
            'k3': 'v3',
            'k4': Like({
                'v41': 11
            })
        })
        result_1 = {
            'k1': 'v1',
            'k2': 'v2',
            'k4': 'v4'
        }
        # hard_mode=True,实际返回字段与契约定义字段要完全一致；hard_mode=False,实际返回字段可多于契约定义字段
        mPactVerify = PactVerify(expected_format, hard_mode=True)
        mPactVerify.verify(result_1)
        print('test_hard_mode_2', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # hard_mode
    def test_hard_mode_3(self):
        expected_format = Matcher({
            'k1': Matcher('v1', key_missable=True),
            'k4': EachLike({
                'v41': 11
            })
        })
        result_1 = {
            'k2': 'v1',
            'k4': [{
                'v42': 11
            }]
        }
        # hard_mode=True,实际返回字段与契约定义字段要完全一致；hard_mode=False,实际返回字段可多于契约定义字段
        mPactVerify = PactVerify(expected_format, hard_mode=True)
        mPactVerify.verify(result_1)
        print('test_hard_mode_3', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # hard_mode
    def test_hard_mode_4(self):
        expected_format = Like({
            'k1': 'v1',

        })
        result_1 = {
            'k2': Term('^\d{2}$', 22),
            'k3': Enum([11, 22, 33]),
            'k4': EachLike(11),
            'k5': Like(11)

        }
        # hard_mode=True,实际返回字段与契约定义字段要完全一致；hard_mode=False,实际返回字段可多于契约定义字段
        mPactVerify = PactVerify(expected_format, hard_mode=True)
        mPactVerify.verify(result_1)
        print('test_hard_mode_4', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == False

    # hard_mode
    def test_hard_mode_5(self):
        expected_format = Like({
            'k1': 'v1',
            'k3': Like('v3', key_missable=True),
            'k4': Like({
                'v41': 11
            }),
            'k5': Like({
                'v51': 11
            }, dict_emptiable=True),
            'k6': Like('v6', nullable=True),
            'k7': Like({
                'v71': 11
            }, jsonloads=True),
            'k8': EachLike(11),
            'k9': Term('^\d{2}$', example=22),
            'k10': Enum([11, 22, 33], iterate_list=True)
        })
        result_1 = {
            'k1': 'v1',
            # 'k2': 'v2',
            'k4': {
                'v41': 22
            },
            'k5': {},
            'k6': None,
            'k7': "{\"v71\":33}",
            'k8': [22],
            'k9': 33,
            'k10': [11, 22]

        }

        # 默认hard_mode=True,实际返回字段与契约定义字段要完全一致；hard_mode=False,实际返回字段可多于契约定义字段
        mPactVerify = PactVerify(expected_format, hard_mode=True)
        mPactVerify.verify(result_1)
        print('test_hard_mode_5', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # hard_mode
    def test_hard_mode_6(self):
        expect_format = EachLike({
            "date": "2018-01-01",
            "companyId": "10131",
            "userLoginId": "mjqflwf",
            "amount": -437.00,
            "orderSize": 1
        }, minimum=0)

        result_1 = [{
            'date': '2019-01-01',
            'companyId': '0cq3QTd6hzczDEQG6iX',
            'userLoginId': 'sz_szsmbqcfwyxgs',
            'amount': -300.0,
            'orderSize': 1
        }, {
            'date': '2019-01-01',
            'companyId': '10131',
            'userLoginId': 'OZXZS',
            'amount': -5160.0,
            'orderSize': 1
        }
        ]

        # hard_mode=True,实际返回字段与契约定义字段要完全一致；hard_mode=False,实际返回字段可多于契约定义字段
        mPactVerify = PactVerify(expect_format)
        mPactVerify.verify(result_1)
        print('test_hard_mode_6', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # hard_mode
    def test_example_1(self):
        expect_format = Like({
            "message": "查询成功",
            "success": True,
            "statusCode": 200,
            "data": EachLike({
                "oeName": Like("大灯 双氙气灯 右", key_missable=True),
                "info": Like("", key_missable=True),
                "oeCodeTrim": Like("63117271912", key_missable=True),
                "oeId": Like("402221", key_missable=True),
                "count": Like("1", key_missable=True),
                "catName": Like("车灯", key_missable=True),
                "catCode": Like("63", key_missable=True),
                "isGeneral": 0,  #
                "parentIdList": [],  #
                "exactSearch": False,  #
                "isShow": Like("Y", key_missable=True),
                "parentCatCode": Like("63_1573", key_missable=True),
                "parentCatName": Like("车灯", key_missable=True),
                "priceDate": 0,  #
                "vehicleBrandAll": False,  #
                "extendedProp": Like({
                    "product_period": "_201309",
                    "AE": ""
                }, key_missable=True),
                "shieldOeCode": False,  #
                "price4s": Like("12397.74", key_missable=True),
                "price": 0,  #
                "stdName": Like("车灯", key_missable=True),
                "oeCode": Like("63 11 7 271 912", key_missable=True),
                "tranformName": Like("车灯", key_missable=True),
            })
            ,
            "extendedPropName": Like({
                "product_period": "生产起止日期",
                "AE": "AE"
            })
        })

        result_1 = {
            "message": "查询成功",
            "success": True,
            "statusCode": 200,
            "data": [
                {
                    "oeName": "大灯 双氙气灯 右",
                    "info": "",
                    "oeCodeTrim": "63117271912",
                    "oeId": "402221",
                    "count": "1",
                    "catName": "车灯",
                    "catCode": "63",
                    "isGeneral": 0,
                    "parentIdList": [],
                    "exactSearch": False,
                    "isShow": "Y",
                    "parentCatCode": "63_1573",
                    "parentCatName": "大灯",
                    "priceDate": 0,
                    "vehicleBrandAll": False,
                    "extendedProp": {
                        "product_period": "_201309",
                        "AE": ""
                    },
                    "shieldOeCode": False,
                    "price4s": "12397.74",
                    "price": 0,
                    "stdName": "右大灯",
                    "oeCode": "63 11 7 271 912"
                },
                {
                    "oeName": "大灯 双氙气灯 左",
                    "info": "",
                    "oeCodeTrim": "63117271911",
                    "oeId": "402220",
                    "count": "1",
                    "catName": "车灯",
                    "catCode": "63",
                    "isGeneral": 0,
                    "parentIdList": [],
                    "exactSearch": False,
                    "isShow": "Y",
                    "parentCatCode": "63_1573",
                    "parentCatName": "大灯",
                    "priceDate": 0,
                    "vehicleBrandAll": False,
                    "extendedProp": {
                        "product_period": "_201309",
                        "AE": ""
                    },
                    "shieldOeCode": False,
                    "price4s": "12397.74",
                    "price": 0,
                    "stdName": "左大灯",
                    "oeCode": "63 11 7 271 911"
                },
                {
                    "isGeneral": 0,
                    "parentIdList": [],
                    "exactSearch": True,
                    "priceDate": 0,
                    "tranformName": "大灯",
                    "vehicleBrandAll": False,
                    "shieldOeCode": False,
                    "price": 0
                }
            ],
            "extendedPropName": {
                "product_period": "生产起止日期",
                "AE": "AE"
            }
        }

        # hard_mode=True,实际返回字段与契约定义字段要完全一致；hard_mode=False,实际返回字段可多于契约定义字段
        mPactVerify = PactVerify(expect_format)
        mPactVerify.verify(result_1)
        print('test_example_1', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    def test_example_2(self):
        expect_format = Like({
            "code": 0,
            "message": "操作成功",
            "data": EachLike({
                "id": "1",
                "menu_code": "routes",
                "menu_name": "路由",
                "module_id": 57,
                "menu_type": "dir",
                "menu_order": 1,
                "menu_show": 0,
                "menu_path": "/main",
                "parent_id": "-1",
                "sub_menu_list": EachLike({
                    "id": "3",
                    "menu_code": "serve",
                    "menu_name": "工单",
                    "module_id": 57,
                    "menu_type": "dir",
                    "menu_order": 2,
                    "menu_show": 1,
                    "menu_path": "/main/serve",
                    "parent_id": "1",
                    "icon": "inventory",
                    "menu_target": Like('', key_missable=True),
                    "sub_menu_list": EachLike({
                        "id": "4",
                        "menu_code": "serve_manage",
                        "menu_name": "工单管理",
                        "module_id": 57,
                        "menu_type": "ori_link",
                        "menu_target": Like("/Main/serve/ReceivingCarTicketList", key_missable=True),
                        "menu_order": 1,
                        "menu_show": 1,
                        "menu_path": "/main/serve/manage",
                        "parent_id": "54"
                    }, key_missable=True
                    )
                }, key_missable=True
                )
            }
            )
        })

        result_1 = {
            "code": 0,
            "message": "操作成功",
            "data": [{
                "id": "1",
                "menu_code": "routes",
                "menu_name": "路由",
                "module_id": 57,
                "menu_type": "dir",
                "menu_order": 1,
                "menu_show": 0,
                "menu_path": "/main",
                "parent_id": "-1",
                "sub_menu_list": [{
                    "id": "2",
                    "menu_code": "index",
                    "menu_name": "首页",
                    "module_id": 57,
                    "menu_type": "link",
                    "menu_order": 1,
                    "menu_show": 1,
                    "menu_path": "/main/index",
                    "parent_id": "1",
                    "icon": "home"
                }, {
                    "id": "3",
                    "menu_code": "serve",
                    "menu_name": "工单",
                    "module_id": 57,
                    "menu_type": "dir",
                    "menu_order": 2,
                    "menu_show": 1,
                    "menu_path": "/main/serve",
                    "parent_id": "1",
                    "icon": "inventory",
                    "sub_menu_list": [{
                        "id": "4",
                        "menu_code": "serve_manage",
                        "menu_name": "工单管理",
                        "module_id": 57,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/serve/ReceivingCarTicketList",
                        "menu_order": 1,
                        "menu_show": 1,
                        "menu_path": "/main/serve/manage",
                        "parent_id": "3"
                    }, {
                        "id": "5",
                        "menu_code": "serve_create",
                        "menu_name": "新建开单",
                        "module_id": 57,
                        "menu_type": "link",
                        "menu_order": 2,
                        "menu_show": 1,
                        "menu_path": "/main/serve/create",
                        "parent_id": "3"
                    }, {
                        "id": "6",
                        "menu_code": "serve_workshop",
                        "menu_name": "车间管理",
                        "module_id": 57,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/serve/WorkShop",
                        "menu_order": 3,
                        "menu_show": 1,
                        "menu_path": "/main/serve/workshop",
                        "parent_id": "3"
                    }, {
                        "id": "7",
                        "menu_code": "serve_invoiceRecord",
                        "menu_name": "单据记录",
                        "module_id": 57,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/serve/recordlist",
                        "menu_order": 4,
                        "menu_show": 1,
                        "menu_path": "/main/serve/invoiceRecord",
                        "parent_id": "3"
                    }, {
                        "id": "8",
                        "menu_code": "serve_spectaculars",
                        "menu_name": "客户看板",
                        "module_id": 57,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/serve/CustomerBoard",
                        "menu_order": 5,
                        "menu_show": 1,
                        "menu_path": "/main/serve/spectaculars",
                        "parent_id": "3"
                    }, {
                        "id": "9",
                        "menu_code": "serve_discountApprove",
                        "menu_name": "折扣审批",
                        "module_id": 57,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/serve/DiscountApproveList",
                        "menu_order": 6,
                        "menu_show": 1,
                        "menu_path": "/main/serve/discountApprove",
                        "parent_id": "3"
                    }, {
                        "id": "10",
                        "menu_code": "serve_ReservationRecord",
                        "menu_name": "预约记录",
                        "module_id": 57,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/serve/datelist",
                        "menu_order": 7,
                        "menu_show": 1,
                        "menu_path": "/main/serve/ReservationRecord",
                        "parent_id": "3"
                    }, {
                        "id": "11",
                        "menu_code": "serve_insureMng",
                        "menu_name": "保险管理",
                        "module_id": 57,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/member/InsuranceInfo",
                        "menu_order": 8,
                        "menu_show": 1,
                        "menu_path": "/main/serve/insureMng",
                        "parent_id": "3"
                    }, {
                        "id": "12",
                        "menu_code": "serve_pickCar",
                        "menu_name": "视频接车",
                        "module_id": 57,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/serve/WorkshopCameraServircrecordList",
                        "menu_order": 9,
                        "menu_show": 1,
                        "menu_path": "/main/serve/pickCar",
                        "parent_id": "3"
                    }, {
                        "id": "92",
                        "menu_code": "serve_info",
                        "menu_name": "工单详情",
                        "module_id": 57,
                        "menu_type": "link",
                        "menu_order": 10,
                        "menu_show": 0,
                        "menu_path": "/main/serve/info",
                        "parent_id": "3"
                    }, {
                        "id": "13",
                        "menu_code": "serve_detail",
                        "menu_name": "工单详情",
                        "module_id": 57,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/serve/detail",
                        "menu_order": 11,
                        "menu_show": 0,
                        "menu_path": "/main/serve/:id",
                        "parent_id": "3"
                    }
                    ]
                }, {
                    "id": "14",
                    "menu_code": "customer",
                    "menu_name": "客户",
                    "module_id": 18,
                    "menu_type": "dir",
                    "menu_order": 3,
                    "menu_show": 1,
                    "menu_path": "/main/customer",
                    "parent_id": "1",
                    "icon": "customer",
                    "sub_menu_list": [{
                        "id": "15",
                        "menu_code": "customer_add",
                        "menu_name": "新建客户",
                        "module_id": 18,
                        "menu_type": "link",
                        "menu_order": 2,
                        "menu_show": 1,
                        "menu_path": "/main/customer/add",
                        "parent_id": "14"
                    }, {
                        "id": "16",
                        "menu_code": "customer_list",
                        "menu_name": "客户车辆",
                        "module_id": 18,
                        "menu_type": "link",
                        "menu_order": 3,
                        "menu_show": 1,
                        "menu_path": "/main/customer/list",
                        "parent_id": "14"
                    }, {
                        "id": "17",
                        "menu_code": "customer_info",
                        "menu_name": "客户详情",
                        "module_id": 18,
                        "menu_type": "link",
                        "menu_order": 4,
                        "menu_show": 0,
                        "menu_path": "/main/customer/info",
                        "parent_id": "14"
                    }, {
                        "id": "18",
                        "menu_code": "customer_businessMng",
                        "menu_name": "商机管理",
                        "module_id": 18,
                        "menu_type": "link",
                        "menu_order": 5,
                        "menu_show": 1,
                        "menu_path": "/main/customer/businessMng",
                        "parent_id": "14"
                    }, {
                        "id": "19",
                        "menu_code": "customer_service",
                        "menu_name": "客情维护",
                        "module_id": 18,
                        "menu_type": "link",
                        "menu_order": 6,
                        "menu_show": 1,
                        "menu_path": "/main/customer/service",
                        "parent_id": "14"
                    }, {
                        "id": "20",
                        "menu_code": "customer_feedback",
                        "menu_name": "车主评价",
                        "module_id": 18,
                        "menu_type": "link",
                        "menu_order": 7,
                        "menu_show": 1,
                        "menu_path": "/main/customer/feedback",
                        "parent_id": "14"
                    }, {
                        "id": "21",
                        "menu_code": "customer_analyze",
                        "menu_name": "统计分析",
                        "module_id": 18,
                        "menu_type": "link",
                        "menu_order": 8,
                        "menu_show": 1,
                        "menu_path": "/main/customer/analyze",
                        "parent_id": "14"
                    }, {
                        "id": "22",
                        "menu_code": "customer_businessDetail",
                        "menu_name": "商机详情",
                        "module_id": 18,
                        "menu_type": "link",
                        "menu_order": 9,
                        "menu_show": 0,
                        "menu_path": "/main/customer/businessDetail/:cid?/:id?",
                        "parent_id": "14"
                    }, {
                        "id": "23",
                        "menu_code": "customer_buyCard",
                        "menu_name": "购买套餐",
                        "module_id": 18,
                        "menu_type": "link",
                        "menu_target": "/Main/member/BuyVippackage",
                        "menu_order": 10,
                        "menu_show": 0,
                        "menu_path": "/main/customer/buyCard",
                        "parent_id": "14"
                    }, {
                        "id": "24",
                        "menu_code": "customer_buyRechargCard",
                        "menu_name": "购买储值卡",
                        "module_id": 18,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/member/BuyVipRechargeCard",
                        "menu_order": 11,
                        "menu_show": 0,
                        "menu_path": "/main/customer/buyCard",
                        "parent_id": "14"
                    }, {
                        "id": "25",
                        "menu_code": "customer_buyVipCard",
                        "menu_name": "购买VIP卡",
                        "module_id": 18,
                        "menu_type": "ori_link",
                        "menu_target": "/main/customer/buyVipCard",
                        "menu_order": 12,
                        "menu_show": 0,
                        "menu_path": "/main/customer/buyCard",
                        "parent_id": "14"
                    }, {
                        "id": "26",
                        "menu_code": "customer_packageSetting",
                        "menu_name": "套餐设置",
                        "module_id": 18,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/system/VipPackageTemplate",
                        "menu_order": 13,
                        "menu_show": 0,
                        "menu_path": "/main/customer/cardSetting",
                        "parent_id": "14"
                    }, {
                        "id": "27",
                        "menu_code": "customer_packageDetail",
                        "menu_name": "套餐明细",
                        "module_id": 18,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/member/VipPackageDetail",
                        "menu_order": 14,
                        "menu_show": 0,
                        "menu_path": "/main/customer/cardDetail",
                        "parent_id": "14"
                    }, {
                        "id": "28",
                        "menu_code": "customer_rechargeCardSetting",
                        "menu_name": "储值卡设置",
                        "module_id": 18,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/system/VipRechargecardTemplate",
                        "menu_order": 15,
                        "menu_show": 0,
                        "menu_path": "/main/customer/rechargeCardSetting",
                        "parent_id": "14"
                    }, {
                        "id": "29",
                        "menu_code": "customer_rechargeCardDetail",
                        "menu_name": "储值卡明细",
                        "module_id": 18,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/member/RechargeCardDetail",
                        "menu_order": 16,
                        "menu_show": 0,
                        "menu_path": "/main/customer/rechargeDetail",
                        "parent_id": "14"
                    }, {
                        "id": "30",
                        "menu_code": "customer_vipCardSetting",
                        "menu_name": "VIP卡设置",
                        "module_id": 18,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/system/VipLevelCardTemplate",
                        "menu_order": 17,
                        "menu_show": 0,
                        "menu_path": "/main/customer/vipCardSetting",
                        "parent_id": "14"
                    }
                    ]
                }, {
                    "id": "31",
                    "menu_code": "stock",
                    "menu_name": "库存",
                    "module_id": 60,
                    "menu_type": "dir",
                    "menu_order": 4,
                    "menu_show": 1,
                    "menu_path": "/main/stock",
                    "parent_id": "1",
                    "icon": "inventory",
                    "sub_menu_list": [{
                        "id": "32",
                        "menu_code": "stock_fittingsMng",
                        "menu_name": "配件管理",
                        "module_id": 60,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/stock/InventoryBalanceList",
                        "menu_order": 1,
                        "menu_show": 1,
                        "menu_path": "/main/stock/fittingsMng",
                        "parent_id": "31"
                    }, {
                        "id": "33",
                        "menu_code": "stock_inboundMng",
                        "menu_name": "入库管理",
                        "module_id": 60,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/stock/InoutticketList?type=1",
                        "menu_order": 2,
                        "menu_show": 1,
                        "menu_path": "/main/stock/inboundMng",
                        "parent_id": "31"
                    }, {
                        "id": "34",
                        "menu_code": "stock_allotMng",
                        "menu_name": "调拨管理",
                        "module_id": 60,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/stock/TransFerList",
                        "menu_order": 3,
                        "menu_show": 1,
                        "menu_path": "/main/stock/allotMng",
                        "parent_id": "31"
                    }, {
                        "id": "35",
                        "menu_code": "stock_inventoryCheck",
                        "menu_name": "库存盘点",
                        "module_id": 60,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/stock/Stockcheck",
                        "menu_order": 3,
                        "menu_show": 1,
                        "menu_path": "/main/stock/inventoryCheck",
                        "parent_id": "31"
                    }, {
                        "id": "36",
                        "menu_code": "stock_assembleList",
                        "menu_name": "组装/拆卸",
                        "module_id": 60,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/stock/AssembleList",
                        "menu_order": 4,
                        "menu_show": 1,
                        "menu_path": "/main/stock/assembleList",
                        "parent_id": "31"
                    }, {
                        "id": "37",
                        "menu_code": "stock_stockReport",
                        "menu_name": "库存报表",
                        "module_id": 60,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/stock/StockCycle",
                        "menu_order": 5,
                        "menu_show": 1,
                        "menu_path": "/main/stock/stockReport",
                        "parent_id": "31"
                    }
                    ]
                }, {
                    "id": "50",
                    "menu_code": "report",
                    "menu_name": "报表",
                    "module_id": 52,
                    "menu_type": "ori_link",
                    "menu_target": "",
                    "menu_order": 7,
                    "menu_show": 1,
                    "menu_path": "/main/report",
                    "parent_id": "1",
                    "icon": "report-forms",
                    "sub_menu_list": [{
                        "id": "51",
                        "menu_code": "report_business",
                        "menu_name": "营业报表",
                        "module_id": 52,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/finance/RevenueReport",
                        "menu_order": 1,
                        "menu_show": 1,
                        "menu_path": "/main/report/business",
                        "parent_id": "50"
                    }, {
                        "id": "52",
                        "menu_code": "report_finance",
                        "menu_name": "财务报表",
                        "module_id": 52,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/stock/WaitingOutList",
                        "menu_order": 2,
                        "menu_show": 1,
                        "menu_path": "/main/report/finance",
                        "parent_id": "50"
                    }, {
                        "id": "53",
                        "menu_code": "report_marketing",
                        "menu_name": "营销报表",
                        "module_id": 52,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/stock/WaitingOutList",
                        "menu_order": 3,
                        "menu_show": 1,
                        "menu_path": "/main/report/marketing",
                        "parent_id": "50"
                    }
                    ]
                }, {
                    "id": "54",
                    "menu_code": "staff",
                    "menu_name": "员工",
                    "module_id": 4,
                    "menu_type": "dir",
                    "menu_order": 8,
                    "menu_show": 1,
                    "menu_path": "/main/staff",
                    "parent_id": "1",
                    "icon": "staff-manage",
                    "sub_menu_list": [{
                        "id": "55",
                        "menu_code": "staff_list",
                        "menu_name": "员工列表",
                        "module_id": 39,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/clerk/EmployeeList",
                        "menu_order": 1,
                        "menu_show": 1,
                        "menu_path": "/main/staff/list",
                        "parent_id": "54"
                    }, {
                        "id": "59",
                        "menu_code": "staff_performance",
                        "menu_name": "员工绩效",
                        "module_id": 43,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/clerk/SalesPerformance",
                        "menu_order": 5,
                        "menu_show": 1,
                        "menu_path": "/main/staff/performance",
                        "parent_id": "54"
                    }, {
                        "id": "60",
                        "menu_code": "staff_salaryReport",
                        "menu_name": "工资报表",
                        "module_id": 43,
                        "menu_type": "ori_link",
                        "menu_target": "/Main/clerk/SalaryReport",
                        "menu_order": 5,
                        "menu_show": 1,
                        "menu_path": "/main/staff/salaryReport",
                        "parent_id": "54"
                    }
                    ]
                }
                ]
            }
            ]
        }

        # hard_mode=True,实际返回字段与契约定义字段要完全一致；hard_mode=False,实际返回字段可多于契约定义字段
        mPactVerify = PactVerify(expect_format)
        mPactVerify.verify(result_1)
        print('test_example_2', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # keymissable
    def test_example_3(self):
        expected_format = Like({
            'sum': EachLike(1, nullable=True)
        })
        result_1 = {
            "sum": [None, None, None, 3, 6, 1, None]
        }
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_example_3', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True

    # type_strict
    def test_term_type_strict_1(self):
        expected_format = EachLike({
            'num': Term('^\d+$|^\d+\.\d+$', example=10, type_strict=False)
        })
        result_1 = [
            {'num': 10},
            {'num': 10.01}
        ]
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(result_1)
        print('test_term_type_strict_1', json.dumps(mPactVerify.verify_info, indent=4))
        assert mPactVerify.verify_result == True


if __name__ == '__main__':
    unittest.main()
