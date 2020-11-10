import copy
import json
from pactverify.core import Like, EachLike


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


if __name__ == '__main__':
    resposne_data = {
        'k1': 'v1',
        'k2': None
    }
    pactverify_json = generate_pact_json_by_response(resposne_data, separator='@')
    print(pactverify_json)
