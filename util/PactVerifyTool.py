# coding:utf-8
from .contracts import Contract
from util.matchers import PactVerify


# 契约校验工具类
class PactVerifyTool:

    def __init__(self):
        self.pact_verify_info = {}

    def verify(self, actual_data, pact_name):
        expected_format = getattr(Contract, pact_name)
        mPactVerify = PactVerify(expected_format)
        mPactVerify.verify(actual_data)
        self.pact_verify_info = mPactVerify.verify_info
        return mPactVerify.verify_result
