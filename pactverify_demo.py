#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 20:23
# @Author  : liuhui
# @Detail  : 使用示例

from pactverify.utils import generate_pact_json_by_response

if __name__ == '__main__':
    response_json = {
        "msg": "success",
        "code": 0,
        "data": [{
            "type_id": 249,
            "name": "王者荣耀",
            "order_index": 1,
            "status": 1,
            "subtitle": " ",
            "game_name": "王者荣耀"
        }, {
            "type_id": 250,
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
            "game_name": "刺激战场"
        }
        ]
    }
    # 参数说明：响应json数据,契约关键字标识符(默认$)
    pact_json = generate_pact_json_by_response(response_json, separator='$')
    print(pact_json)
    '''
    # 模板生成只会包含$EachLike、$Like,可以根据具体校验需求更改,数组取第一个元素为模板来生成
    {
        '$Like': {
            'msg': 'success',
            'code': 0,
            'data': {
                '$EachLike': {
                    'type_id': 249,
                    'name': '王者荣耀',
                    'order_index': 1,
                    'status': 1,
                    'subtitle': ' ',
                    'game_name': '王者荣耀'
                }
            }
        }
    }
    '''