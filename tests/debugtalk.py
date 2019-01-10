# coding:utf-8
from util.PactVerifyTool import PactVerifyTool


# 契约校验,pact_name在util.contracts中定义
def pact_verify(response, pact_name):
    rsp_body = response.json
    mPactVerifyTool = PactVerifyTool()
    # 存入pact_verify_result和pact_verify_info到response对象
    response.pact_verify_result = mPactVerifyTool.verify(rsp_body, pact_name)
    response.pact_verify_info = mPactVerifyTool.pact_verify_info
