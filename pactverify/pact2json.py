import random
from xeger import Xeger

from pactverify.core import PactVerifyError

str_xeger = Xeger(limit=30)


class Pact2Json:

    def __init__(self, separator='$'):
        self.separator = separator

        # pact类key值
        self.pact_key_matcher = self.separator + 'Matcher'
        self.pact_key_like = self.separator + 'Like'
        self.pact_key_eachLike = self.separator + 'EachLike'
        self.pact_key_enum = self.separator + 'Enum'
        self.pact_key_term = self.separator + 'Term'

        self.pact_key_values = self.separator + 'values'
        self.pact_key_params = self.separator + 'params'

        self.json = {}

    def unpack_pact(self, pact_json, parent_json=None):
        if not parent_json:
            parent_json = self.json

        if type(pact_json) not in [list, dict]: return

        if type(pact_json) == dict:
            if self._is_pact_class_json(pact_json):
                for key, value in pact_json:
                    if self._is_pact_class_json(value):
                        raise PactVerifyError('非法pact_json结构:pact类嵌套')
                    # 抽取values值
                    if self._is_params_json(value):
                        target_values = value.get(self.pact_key_values)
                    else:
                        target_values = value
                    if key not in parent_json:
                        parent_json[key] = {}
                    self.unpack_pact(target_values, parent_json)
        else:
            pass

    def _is_pact_class_json(self, target_pact_json):
        '''
        判断是否为pac class结构
        :param target_pact_json:
        :return:
        '''
        result = False
        pact_class_keys = [self.pact_key_matcher, self.pact_key_like, self.pact_key_eachLike, self.pact_key_enum,
                           self.pact_key_term]
        if type(target_pact_json) == dict:
            inner_keys = target_pact_json.keys()
            # 只包含一个key，并且key为
            if inner_keys.length == 1 and inner_keys[0] in pact_class_keys:
                result = True
        return result

    def _is_params_json(self, target_pact_json):
        '''
        判断json是否为params_json结构
        :return:
        '''
        result = False
        pact_params_keys = [self.pact_key_values, self.pact_key_params]
        if type(target_pact_json) == dict:
            inner_keys = target_pact_json.keys()
            if inner_keys.length == 2 and sorted(pact_params_keys) == sorted(inner_keys):
                result = True
        return result


def generate_char():
    # gbk2312对字符的编码采用两个字节相组合, 第一个字节的范围是0xB0 - 0xF7, 第二个字节的范围是0xA1 - 0xFE.在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
    temp = '{0:x} {1:x}'.format(random.randint(0xb0, 0xf7), random.randint(0xa1, 0xf9))
    char = bytes.fromhex(temp).decode('gb2312')
    return char


def make_data(data_type):
    if isinstance(data_type, int):
        old_body = int(str_xeger.xeger(r'[0-9]{%d}' % random.randint(1, 10)))
    elif isinstance(data_type, str):
        old_body = str_xeger.xeger(r'[a-zA-Z0-9%s]{%d}' % (generate_char(), random.randint(1, 10)))
    elif isinstance(data_type, float):
        old_body = float(str_xeger.xeger(
            r'[0-9]{%d}' % random.randint(1, 5)) + '.' + str_xeger.xeger(
            r'[0-9]{%d}' % random.randint(1, 10)))
    else:
        old_body = data_type
    return old_body


pactverify_json = {
    "$Like": {
        "a": {"$EachLike": 11},
        "b": {"$Matcher": 22},
        "c": {"$Like": 22},
        "d": {'$Term': {'$values': r'^\d{1}$', '$params': {'example': 1}}},
        'e': {'$Enum': [11, 22]},
        'f': 23,
        'g': 'rrr',
        "aa": {"$EachLike": {'k1': 'v1'}},
        "aaa": {"$EachLike": ['k1', 'v1']},
        'code': 0,
        'msg': {'$Like': {"id": 1, "name": 'lili'}},
        'ms122g': {'$Like': {"id": 1, "name": 'lili', '999': {"$EachLike": 11}}},
        '9232': {'$Like': {"id": 1, "name": 'lili', '999': {
            "$EachLike": {'k1': {'$Like': {'$values': {'k1': 'v1'}, '$params': {'nullable': True}}}}}}},
        '19232': {'$Like': {"id": 1, "name": 'lili', '999': {"$EachLike": ['k11', 'v1']}}},
        '192232': {'$Like': {"id": 1, "name": 'lili', '999': {"$EachLike": {'$EachLike': {"id": 1, "name": 'lili'}}}}},
        'old_data': {'$Like': {
            'msg': 'success',
            'code': {'$Matcher': {'k': '3'}},
            'aa': {'$Enum': [11, 22]},
            'shuzi': {
                '$Term': {
                    '$values': r'^\d{1}$',
                    '$params': {'example': 1}
                }},
            'data': {
                '$Like': {
                    'type_id': {'$EachLike': 2222},
                    'name': {'$Like': '9999999'},
                    'order_index': {'$Enum': [111, 1223, 166, 121]},
                    'status': 1,
                    'subtitle': {
                        '$Like': {
                            'te22st': 555,
                            '331113': {'$Enum': [11, 223, 66, 21]},
                            '9983': {'$EachLike': {'k1': '11111'}}
                        }
                    },
                    'game_name': {'$EachLike': {'test': {'$Enum': [191, 5223, 626, 21111]},
                                                'test2': {'$Like': '9999999'},

                                                }},
                    'user_name': {'$EachLike': {
                        '$values': {'k2231': 'v1'},
                        '$params': {'minimum': 0}
                    }},
                    'kkkk': {'$Enum': {
                        '$values': [99, 88],
                        '$params': {'iterate_list': True}
                    }
                    }

                }
            }
        }},
        'gg': {'$Enum': {'$values': [11, 22], '$params': {'iterate_list': True}}},
        'dde': {'$EachLike': {'$values': {'k1': 'v1'}, '$params': {'minimum': 0}}},
        "a111a": {"$EachLike": {'k1': {'$Enum': {'$values': [11, 22], '$params': {'iterate_list': True}}},
                                '232s': {'$Matcher': 12}, '3s': {"$Like": 22}}},
        "768833": {"$EachLike": {'k1': {'$Enum': {'$values': [11, 22], '$params': {'iterate_list': True}}},
                                 '2228s': {'$Matcher': 12}, '3333s': {"$Like": 22}}},
        '8322': {'$Like': {'$values': {'k1': 'v1'}, '$params': {'nullable': True}}},
        'age': {
            '$Term': {
                '$values': r'^\d{1}$',
                '$params': {'example': 1, 'key_missable': True}
            }
        },
        'm1sg': {
            '$Matcher': {
                '$values': 'success',
                '$params': {'key_missable': True}
            }
        },
        'cod9999e': {
            '$Like': {
                '$values': 0,
                '$params': {'key_missable': True}
            }
        },
    }
}
