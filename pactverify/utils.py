import copy
import json
from pactverify.core import Like, EachLike
from pactverify.matchers import PactJsonVerify
from pactverify.pact2json3 import pact_like, pact_eachlike, pact_term, pact_enum, pact_matcher


def generate_pact_json_by_response(target_data, pactverify_json=None, is_list=False, separator='$'):
    """
    根据接口返回数据自动生成json格式断言数据
    :param target_data:  返回数据
    :param pactverify_json: 自动生成的断言数据
    :param is_list:
    :return:
    """

    base_types = (float, str, int, bool)

    like_key = separator + Like.__name__
    eachlike_key = separator + EachLike.__name__

    values_key = separator + 'values'
    params_key = separator + 'params'

    if pactverify_json is None:

        if not isinstance(target_data, (list, dict)):
            try:
                tmp = json.loads(target_data)
                if isinstance(tmp, (list, dict)):
                    target_data = tmp
            except Exception as e:
                print('【pactverify生成json断言数据异常】：{}'.format(str(e)))
                return None

        pactverify_json = {}

    if type(target_data) == dict:
        if (is_list):
            pass
        else:
            pactverify_json = {like_key: copy.deepcopy(target_data)}

        for k, v in target_data.items():
            if (is_list):
                target_data[k] = {}
            else:
                pactverify_json[like_key][k] = {}
            if type(v) in base_types:
                if (like_key in pactverify_json.keys()):

                    pactverify_json[like_key][k] = v
                else:

                    pactverify_json[k] = v
            else:
                if (is_list):
                    pactverify_json[k] = generate_pact_json_by_response(v, pactverify_json[k], False, separator)
                else:
                    pactverify_json[like_key][k] = generate_pact_json_by_response(v,
                                                                                  pactverify_json[like_key][
                                                                                      k],
                                                                                  False, separator)

    elif type(target_data) == list:
        if len(target_data) == 0:
            pactverify_json = {
                eachlike_key: {
                    values_key: "空数组占位",
                    params_key: {
                        "minimum": 0
                    }
                }
            }
        else:
            example_data = target_data[0]
            pactverify_json = {
                eachlike_key: example_data
            }
            pactverify_json[eachlike_key] = generate_pact_json_by_response(example_data,
                                                                           pactverify_json[eachlike_key],
                                                                           True, separator)


    elif type(target_data) == type(None):
        pactverify_json = {
            like_key: {
                values_key: "null占位",
                params_key: {
                    "nullable": True
                }
            }
        }

    elif type(target_data) in base_types:
        if is_list:
            pactverify_json = copy.deepcopy(target_data)
        else:
            pactverify_json = {
                like_key: copy.deepcopy(target_data)
            }
    return pactverify_json


def generate_json_by_pact(pactverify_json, separator='$'):
    '''
     传入契约，根据契约生成对应的json
     支持
     基本的匹配类型，包括含有参数的情况
        1、Matcher 类，校验规则：值匹配
        2、Like 类，校验规则：类型匹配
        3、EachLike 类，校验规则：数组类型匹配
        4、Term 类，校验规则：正则匹配
        5、Enum 类，校验规则：枚举匹配
     每一级的处理都是独立的递归处理，如果json深度太深，性能会存在问题
    :param pactverify_json:
    :return:
    '''
    try:
        mPactVerify = PactJsonVerify(pactverify_json, hard_mode=True, separator=separator)
        test_json = {'test': pactverify_json}
        pact_json = {}  # 生成的json
        # 处理like类型
        pact_json = pact_like(test_json, pact_json)
        # 基于上面的结果处理EachLike类型
        test_json = pact_json
        pact_json = {}
        pact_eachlike(test_json, pact_json)
        # Term 类处理  正则
        test_json = pact_json
        pact_json = {}
        pact_term(test_json, pact_json)
        # Enum类型处理
        test_json = pact_json
        pact_json = {}
        pact_enum(test_json, pact_json)
        # pact_Matcher类型处理
        test_json = pact_json
        pact_json = {}
        pact_matcher(test_json, pact_json, )

        pact_json = pact_json['test']
        mPactVerify.verify(pact_json)

        if mPactVerify.verify_result == True:
            return pact_json
        else:
            return {'error': 'mockjson 生成失败 ', 'verify_info': mPactVerify.verify_info}
    except Exception as e:
        return {'error': 'mockjson 生成失败 ', 'verify_info': str(e)}
