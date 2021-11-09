import random
from xeger import Xeger

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

    def pact_like(self, dic_json, dic):
        '''
        校验规则：类型匹配
        :param dic_json:
        :param dic:
        :return:
        '''
        if isinstance(dic_json, dict):
            for key in dic_json:
                if isinstance(dic_json[key], dict):
                    for key_down in dic_json[key]:
                        if key_down == '$Like':
                            if isinstance(dic_json[key][key_down], dict) and '$values' in dic_json[key][
                                key_down].keys():
                                dic_json[key] = make_data(dic_json[key][key_down]['$values'])
                            else:
                                dic_json[key] = make_data(dic_json[key][key_down])
                            self.pact_like(dic_json, dic)
                        else:
                            dic[key] = {}
                            self.pact_like(dic_json[key], dic[key])
                elif isinstance(dic_json[key], (list, tuple)):
                    new_key = []
                    for key_down in dic_json[key]:
                        new_dic = {}
                        self.pact_like(key_down, new_dic)
                        if new_dic:
                            new_key.append(new_dic)
                        else:
                            new_key.append(key_down)
                    dic[key] = new_key
                else:
                    if key not in ['$Matcher', '$values', '$params', '$EachLike', '$Enum', '$Term',
                                   'iterate_list', 'key_missable', 'nullable', 'dict_emptiable', 'jsonloads' 'example',
                                   'Term',
                                   'minimum', 'extra_types']:
                        dic[key] = make_data(dic_json[key])
                    else:
                        dic[key] = dic_json[key]

        return dic

    def pact_eachlike(self, dic_json, dic):
        '''
        校验规则：数组类型匹配
            EachLike 下的项目 如果没有特定，都按LIke实现
        :param dic_json:
        :param dic:
        :return:
        '''
        if isinstance(dic_json, dict):
            for key in dic_json:
                if isinstance(dic_json[key], dict):
                    if key == '$EachLike':
                        dic = [dic_json[key]]
                        return dic
                    else:
                        for key_down in dic_json[key]:
                            if key_down == '$EachLike':
                                ruest_EachLike = []
                                minimum = 1
                                if isinstance(dic_json[key][key_down], dict) and '$values' in dic_json[key][
                                    key_down].keys():
                                    # 判断是否带参数
                                    if '$params' in dic_json[key][key_down].keys():
                                        if 'minimum' in dic_json[key][key_down]['$params'].keys():
                                            minimum = dic_json[key][key_down]['$params']['minimum']
                                    old_body = dic_json[key][key_down]['$values']
                                    for x in range(random.randint(minimum, 10)):
                                        if isinstance(dic_json[key][key_down]['$values'], dict):
                                            EachLike_dic = {}
                                            self.pact_like(old_body, EachLike_dic)
                                        else:
                                            EachLike_dic = make_data(dic_json[key][key_down]['$values'])
                                        ruest_EachLike.append(EachLike_dic)
                                    dic_json[key] = ruest_EachLike
                                else:
                                    ruest_EachLike = []
                                    for x in range(random.randint(minimum, 10)):
                                        if isinstance(dic_json[key][key_down], dict):
                                            EachLike_dic = {}
                                            old_body = dic_json[key][key_down]
                                            self.pact_like(old_body, EachLike_dic)
                                            old_body = EachLike_dic
                                        else:
                                            old_body = make_data(dic_json[key][key_down])
                                        ruest_EachLike.append(old_body)
                                    dic_json[key] = ruest_EachLike

                                self.pact_eachlike(dic_json, dic, )
                            else:
                                dic[key] = {}
                                self.pact_eachlike(dic_json[key], dic[key], )

                elif isinstance(dic_json[key], (list, tuple)):
                    new_key = []
                    for key_down in dic_json[key]:
                        new_dic = {}
                        retun_dic = self.pact_eachlike(key_down, new_dic, )
                        if new_dic:
                            new_key.append(new_dic)
                        elif retun_dic:
                            new_key.append(retun_dic)
                        else:
                            new_key.append(key_down)
                    dic[key] = new_key

                else:
                    dic[key] = dic_json[key]

    def pact_matcher(self, dic_json, dic):
        '''
        校验规则：值匹配 不存在随机
        :param dic_json:
        :param dic:
        :return:
        '''
        if isinstance(dic_json, dict):
            for key in dic_json:
                if isinstance(dic_json[key], dict):  # 如果dic_json[key]依旧是字典类型
                    for key_down in dic_json[key]:
                        if key_down == '$Matcher':
                            if isinstance(dic_json[key][key_down], dict) and '$values' in dic_json[key][
                                key_down].keys():
                                dic_json[key] = dic_json[key][key_down]['$values']
                            else:
                                dic_json[key] = dic_json[key][key_down]
                            self.pact_matcher(dic_json, dic)
                        else:
                            dic[key] = {}
                            self.pact_matcher(dic_json[key], dic[key])
                elif isinstance(dic_json[key], (list, tuple)):
                    new_key = []
                    for key_down in dic_json[key]:
                        new_dic = {}
                        self.pact_matcher(key_down, new_dic)
                        if new_dic:
                            new_key.append(new_dic)
                        else:
                            new_key.append(key_down)
                    dic[key] = new_key
                else:
                    dic[key] = dic_json[key]

    def pact_enum(self, dic_json, dic):
        '''
        校验规则：枚举匹配
        :param dic_json:
        :param dic:
        :return:
        '''
        if isinstance(dic_json, dict):
            for key in dic_json:
                if isinstance(dic_json[key], dict):  # 如果dic_json[key]依旧是字典类型
                    for key_down in dic_json[key]:
                        if key_down == '$Enum':
                            if isinstance(dic_json[key][key_down], dict) and '$params' in dic_json[key][
                                key_down].keys():

                                if 'iterate_list' in dic_json[key][key_down]['$params'] and \
                                        dic_json[key][key_down]['$params']['iterate_list']:
                                    dic_json[key] = dic_json[key][key_down]['$values']
                                else:
                                    print(dic_json, 3333)
                                    dic_json[key] = random.choice(dic_json[key][key_down]['$values'])
                            else:
                                dic_json[key] = random.choice(dic_json[key][key_down])
                            self.pact_enum(dic_json, dic)
                        else:
                            dic[key] = {}
                            self.pact_enum(dic_json[key], dic[key])
                elif isinstance(dic_json[key], (list, tuple)):
                    new_key = []
                    for key_down in dic_json[key]:
                        new_dic = {}
                        self.pact_enum(key_down, new_dic)
                        if new_dic:
                            new_key.append(new_dic)
                        else:
                            new_key.append(key_down)
                    dic[key] = new_key
                else:
                    dic[key] = dic_json[key]

    def pact_term(self, dic_json, dic):
        if isinstance(dic_json, dict):
            for key in dic_json:
                if isinstance(dic_json[key], dict):
                    for key_down in dic_json[key]:
                        if key_down == '$Term':
                            if isinstance(dic_json[key][key_down], dict) and '$values' in dic_json[key][
                                key_down].keys():
                                if isinstance(dic_json[key][key_down]['$params']['example'], int):
                                    dic_json[key] = int(str_xeger.xeger(dic_json[key][key_down]['$values']))
                                elif isinstance(dic_json[key][key_down]['$params']['example'], float):
                                    dic_json[key] = float(str_xeger.xeger(dic_json[key][key_down]['$values']))
                                else:
                                    dic_json[key] = str_xeger.xeger(dic_json[key][key_down]['$values'])
                            else:
                                assert False, '契约中的Term类数据不正确'
                            self.pact_term(dic_json, dic)
                        else:
                            dic[key] = {}
                            self.pact_term(dic_json[key], dic[key])
                elif isinstance(dic_json[key], (list, tuple)):
                    new_key = []
                    for key_down in dic_json[key]:
                        new_dic = {}
                        self.pact_term(key_down, new_dic)
                        if new_dic:
                            new_key.append(new_dic)
                        else:
                            new_key.append(key_down)
                    dic[key] = new_key

                else:
                    dic[key] = dic_json[key]


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
