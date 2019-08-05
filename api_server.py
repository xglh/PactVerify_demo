#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/20 19:20
# @Author  : liuhui
# @Detail  : 测试用api_server

import json
from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/config', methods=['GET'])
def test():
    rsp_body = {
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

    rsp = make_response(json.dumps(rsp_body), 200)
    return rsp


@app.route('/configV2', methods=['GET'])
def test2():
    rsp_body = {
        "msg": "success",
        "code": 0,
        'name': 'liuhui',
        'addr': '上海浦东',
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

    rsp = make_response(json.dumps(rsp_body), 200)
    return rsp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
