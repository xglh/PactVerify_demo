#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/20 19:20
# @Author  : liuhui
# @Detail  : unittest用例
import json
import unittest, requests, HtmlTestRunner, os
from pactverify.matchers import Matcher, Like, EachLike, Term, Enum, PactVerify


class PactTest(unittest.TestCase):

    def test_config_2(self):
        url = 'http://127.0.0.1:8080/configV2'
        config_rsp = requests.get(url)
        config_contract_format = Matcher({
            "msg": "success",
            "code": 200,
            'name': Enum(['lili', 'xiaohei']),
            'addr': Term(r'深圳*', example='深圳宝安'),
            "data": EachLike({
                "type_id": 249,
                "name": "王者荣耀",
                "order_index": 1,
                "status": 1,
                "subtitle": " ",
                "game_name": "王者荣耀"
            }),
            'data_2':
                EachLike({
                    "type_id": 249,
                    "name": "王者荣耀",
                    "order_index": 1,
                    "status": 1,
                    "subtitle": " ",
                    "game_name": "王者荣耀"
                }, minimum=1)
        })

        mPactVerify = PactVerify(config_contract_format)
        actual_rsp_json = config_rsp.json()
        mPactVerify.verify(actual_rsp_json)

        err_msg = 'PactVerify_fail,verify_result:{},verify_info:{}'.format(mPactVerify.verify_result,
                                                                           json.dumps(mPactVerify.verify_info,
                                                                                      indent=4))

        assert mPactVerify.verify_result == False, err_msg


if __name__ == '__main__':
    current_path = os.path.abspath(__file__)
    current_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    suite = unittest.defaultTestLoader.discover(current_dir, pattern="test_*.py")
    runner = HtmlTestRunner.HTMLTestRunner(combine_reports=True, report_name="MyReport", add_timestamp=False)
    runner.run(suite)
