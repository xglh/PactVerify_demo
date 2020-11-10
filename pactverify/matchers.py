"""Classes for defining request and response data that is variable."""
import json
from pactverify.core import *


class PactVerify:

    def __init__(self, matcher, hard_mode=True):
        self.matcher = matcher
        # 严格匹配：实际key必须与契约可以定义完全一致;key_missable在最下层生效
        self.hard_mode = hard_mode
        # 校验数据信息
        self.generate_dict = matcher.generate()
        # 校验类
        self.verify_result = True
        # key比expect定义少
        self.key_less_than_expect_error = []
        # key比expect定义多
        self.key_more_than_expect_error = []
        # 值不匹配错误
        self.value_not_match_error = []
        # 类型不匹配错误
        self.type_not_match_error = []
        # 数组长度不匹配错误
        self.list_len_not_match_error = []
        # 枚举不匹配错误
        self.enum_not_match_error = []

    def verify(self, actual_data, target_key='root', generate_dict=None):

        if generate_dict is None:
            generate_dict = self.generate_dict

        json_class, contents = generate_dict.get(json_class_key), generate_dict.get(contents_key)
        jsonloads = generate_dict.get(jsonloads_key, False)
        nullable = generate_dict.get(nullable_key, False)
        dict_key_missable = generate_dict.get(dict_key_missable_key, False)

        extra_types = generate_dict.get(extra_types_key, [])
        # 转化json字符
        go_next, actual_data = self._jsonStr_loads(target_key, actual_data, jsonloads)

        if go_next:
            # Matcher严格匹配
            if json_class == 'Matcher':
                dict_emptiable = generate_dict.get(dict_emptiable_key, False)
                if type(contents) != dict:
                    self._check_param_value(target_key, actual_data, contents, nullable=nullable)
                else:
                    if not self._check_dict_emptiable(actual_data, dict_emptiable):
                        # 获取expect的所有key
                        self._check_param_key_hard_mode(target_key, actual_data, self.hard_mode, contents,
                                                        nullable=nullable)
                        for k, v in contents.items():
                            target_k = target_key
                            if self._check_param_type(target_k, actual_data, dict, nullable=nullable):
                                target_k = '{}.{}'.format(target_key, k)
                                if not self._skip_check_param_key(k, actual_data,
                                                                  contents.get(k, {})) and self._check_param_key(
                                    target_k,
                                    actual_data,
                                    k, dict_key_missable=dict_key_missable):
                                    if type(v) == dict and self._is_matcher_json(v):
                                        target_data, target_generate_dict = actual_data.get(k), v
                                        self.verify(target_data, target_k, target_generate_dict)
                                    else:
                                        # dict_key_missable为true是跳过key校验
                                        if not (k not in actual_data and dict_key_missable):
                                            self._check_param_value(target_k, actual_data.get(k), v, nullable=nullable)
                    # Like校验字段值类型一致
            elif json_class == 'Like':
                dict_emptiable = generate_dict.get(dict_emptiable_key, False)
                # Like(11)形式
                if type(contents) != dict:
                    self._check_param_type(target_key, actual_data, type(contents), nullable=nullable,
                                           extra_types=extra_types)
                else:
                    if type(actual_data) == dict:
                        if not self._check_dict_emptiable(actual_data, dict_emptiable):
                            # 获取expect的所有key
                            self._check_param_key_hard_mode(target_key, actual_data, self.hard_mode, contents,
                                                            nullable=nullable)

                            for k, v in contents.items():
                                # contents非dict类型;contents为dict类型,没有嵌套matcher_json
                                target_k = '{}.{}'.format(target_key, k)
                                if type(v) == dict and self._is_matcher_json(v):
                                    if self._check_param_type(target_k, actual_data, dict, nullable=nullable):
                                        # 嵌套term对象,actual_data需包含k
                                        if not self._skip_check_param_key(k, actual_data,
                                                                          contents.get(k,
                                                                                       {})) and self._check_param_key(
                                            target_k, actual_data, k, dict_key_missable=dict_key_missable):
                                            target_data, target_generate_dict = actual_data.get(k), v
                                            self.verify(target_data, target_k, target_generate_dict)
                                else:
                                    if not self._skip_check_param_key(k, actual_data,
                                                                      contents.get(k, {})) and self._check_param_key(
                                        target_k, actual_data, k, dict_key_missable=dict_key_missable) and not (
                                            k not in actual_data and dict_key_missable):
                                        self._check_param_type(target_k, actual_data.get(k), type(v),
                                                               nullable=nullable)
                    else:
                        # 非字典类型校验
                        self._check_param_type(target_key, actual_data, dict, nullable=nullable)

            # EachLike外层校验list类型
            elif json_class == 'EachLike':
                # target_data类型为list
                if self._check_param_type(target_key, actual_data, list, nullable=nullable):
                    list_min_len = generate_dict.get(mininum_key)
                    # 最小长度校验
                    self._check_param_list_len(target_key, actual_data, list_min_len)
                    for i in range(0, len(actual_data)):
                        inner_data = actual_data[i]
                        target_k = '{}.{}'.format(target_key, i)
                        # 多层EachLike嵌套场景
                        if self._is_matcher_json(contents) and contents.get(json_class_key) == 'EachLike':
                            # inner_data数据需为list
                            if self._check_param_type(target_k, inner_data, list, nullable=nullable):
                                inner_contents = contents.get(contents_key)
                                inner_min_len = contents.get(mininum_key)
                                inner_nullable = contents.get(nullable_key)
                                inner_dict_key_missable = contents.get(dict_key_missable_key, False)
                                if self._check_param_list_len(target_k, inner_data, inner_min_len):
                                    for inner_i, inner_t in enumerate(inner_data):
                                        target_k_inner = '{}.{}'.format(target_k, inner_i)
                                        target_data_inner = inner_t
                                        target_generate_dict = {
                                            json_class_key: 'Like',
                                            contents_key: inner_contents,
                                            nullable_key: inner_nullable,
                                            dict_key_missable_key: inner_dict_key_missable

                                        }
                                        # 转Like处理
                                        self.verify(target_data_inner, target_k_inner, target_generate_dict)

                        # 单层eachlike的场景
                        else:
                            target_data = inner_data
                            target_generate_dict = {
                                json_class_key: 'Like',
                                contents_key: contents,
                                nullable_key: nullable,
                                dict_key_missable_key: dict_key_missable
                            }
                            if extra_types:
                                target_generate_dict.update({
                                    extra_types_key: extra_types
                                })
                            # 转Like处理
                            self.verify(target_data, target_k, target_generate_dict)
            # Term正则匹配
            elif json_class == 'Term':
                regex_str = contents
                example, type_strict = generate_dict.get(example_key), generate_dict.get(type_strict_key)
                # example类型校验
                if self._check_param_type(target_key, actual_data, type(example), nullable=nullable,
                                          type_strict=type_strict):
                    self._check_param_value(target_key, actual_data, regex_str, regex_mode=True)

            elif json_class == 'Enum':
                expect_enum, iterate_list = contents, generate_dict.get(iterate_list_key, False)
                if not self._check_nullable(actual_data, nullable):
                    # 遍历目标数组中的元素
                    if iterate_list and self._check_param_type(target_key, actual_data,
                                                               list) and self._check_param_list_len(target_key,
                                                                                                    actual_data, 1):
                        for i, v in enumerate(actual_data):
                            target_k = '{}.{}'.format(target_key, i)
                            self._check_enum_element(target_k, v, expect_enum)
                    else:
                        self._check_enum_element(target_key, actual_data, expect_enum)

    # 将json字符串转化为json对象
    def _jsonStr_loads(self, target_key, target_data, jsonloads):
        go_next, load_data = True, target_data
        # str类型才转化
        if jsonloads and type(target_data) == str:
            try:
                load_data = json.loads(target_data)
            except Exception:
                temp = {
                    'actual_key': target_key,
                    'actual_value': target_data,
                    'err_msg': 'json format error'
                }
                self.verify_result = False
                self.value_not_match_error.append(temp)
                go_next = False
        return go_next, load_data

    # nullable检查
    def _check_nullable(self, target_data, nullable):
        result = False
        # nullable为true时，target_data为None默认通过，不再进行下一步检查
        if nullable and target_data is None:
            result = True
        return result

    # emptiable
    def _check_dict_emptiable(self, target_data, dict_emptiable):
        result = False
        # emptiable为true是，target_data为dict类型切为空是通过，不再进行下一步检查
        if dict_emptiable and type(target_data) == dict and len(target_data) == 0:
            result = True
        return result

    # 校验参数类型
    def _check_param_type(self, target_key, target_data, expect_type, nullable=False, type_strict=True, extra_types=[]):
        check_result = True
        # nullable校验不通过继续校验
        if not self._check_nullable(target_data, nullable):
            if type_strict and not (
                    self._check_param_type_base(target_data, expect_type) or self._check_extra_keys(target_data,
                                                                                                    extra_types)):
                check_result = False
                self._update_type_error(target_key, target_data, expect_type, extra_types=extra_types)
        # nullable校验通过不继续校验
        else:
            check_result = False
        return check_result

    # 检查参数类型基础方法
    def _check_param_type_base(self, target_data, expect_type):
        result = True

        # bool为int instance，单独判断
        if type(target_data) == bool and type(target_data) != expect_type:
            result = False
        # int16 int32 int64型数据判断实例类型判断
        elif not (isinstance(target_data, expect_type) or (
                type(target_data) in [int, float] and issubclass(expect_type, type(target_data)))):
            result = False
        return result

    def _check_extra_keys(self, actual_data, extra_types):
        result = False
        for extra_key in extra_types:
            extra_type = type(extra_key)
            if self._check_param_type_base(actual_data, extra_type):
                result = True
                break
        return result

    # 跳过参数key校验   result=True时跳过校验   target_key为实际key，不加拼接路径
    def _skip_check_param_key(self, target_key, target_data, generate_dict):
        result = False
        # skip key校验
        if self._is_matcher_json(generate_dict) and generate_dict.get(key_missable_key, False) == True:
            if type(target_data) == dict and target_key not in target_data:
                result = True
        return result

    # 校验参数key
    def _check_param_key(self, target_key, target_data, expect_key, dict_key_missable=False):
        check_result = True
        # target_data非dict类型报type_error
        if type(target_data) != dict:
            check_result = False
            self._update_type_error(target_key, target_data, dict)
        else:
            if not dict_key_missable and expect_key not in [json_class_key, contents_key,
                                                            mininum_key] and expect_key not in target_data:
                self.verify_result = check_result = False
                self._update_key_error(target_key, key_error_type='less')
        return check_result

    # hard_mode下检验key_more场景
    def _check_param_key_hard_mode(self, target_key, target_data, hard_mode, contents: dict, nullable=False):
        # target_data类型必须为dict
        # 兼容key_missable和nullable；非此情况下必须为dict结构
        if not self._check_nullable(target_data, nullable) and self._check_param_type(target_key, target_data,
                                                                                      dict):
            # pact占用key
            pact_keys_set = set([json_class_key, contents_key, mininum_key])
            expect_keys_set, actual_keys_set, missable_keys_set = set(), set(), set()
            for key in contents:
                value = contents.get(key)
                # 非key_missable
                if self._skip_check_param_key(target_key, target_data, value):
                    missable_keys_set.add(key)
            expect_keys_set = set([key for key in contents]) - pact_keys_set - missable_keys_set
            actual_keys_set = set([x[0] for x in target_data.items()]) - pact_keys_set - missable_keys_set
            actual_key_more_set = actual_keys_set - expect_keys_set
            # hard_mode下校验key_more场景
            if hard_mode and len(actual_key_more_set) > 0:
                self.verify_result = False
                for actual_key in actual_key_more_set:
                    target_k = '{}.{}'.format(target_key, actual_key)
                    self._update_key_error(target_k, key_error_type='more')

    # 校验参数值
    def _check_param_value(self, target_key, target_data, expect_value, regex_mode=False, nullable=False):
        check_result = True
        if not self._check_nullable(target_data, nullable):
            # 非正则匹配
            if not regex_mode:
                if not (target_data == expect_value and type(target_data) == type(expect_value)):
                    self._update_vaule_error(target_key, target_data, expect_value)
            # 正则匹配
            else:
                m = re.match(expect_value, str(target_data))
                # 没匹配到
                if not m:
                    self._update_vaule_error(target_key, target_data, expect_value, regex_mode=True)
        return check_result

    # 校验数组最小长度
    def _check_param_list_len(self, target_key, target_data, len_min):
        check_result = True
        # target_data非list类型报type_error
        if type(target_data) != list:
            self._update_type_error(target_key, target_data, list)
        else:
            if len(target_data) < len_min:
                self._update_len_error(target_key, target_data, len_min)
        return check_result

    # 校验枚举元素
    def _check_enum_element(self, target_key, target_data, expect_enum):
        check_result = True
        try:
            if target_data not in expect_enum:
                check_result = False
        except Exception:
            check_result = False

        if not check_result:
            self._update_enum_error(target_key, target_data, expect_enum)
        return check_result

    # 更新type类型错误
    def _update_type_error(self, target_key, target_data, expect_type, extra_types=[]):
        self.verify_result = False
        temp = {
            'actual_key': target_key,
            'actual_vaule': target_data,
            'expect_type': expect_type.__name__
        }
        if extra_types:
            temp.update({
                extra_types_key: extra_types
            })
        if temp not in self.type_not_match_error:
            self.type_not_match_error.append(temp)

    # 更新key类型错误,默认错误类型为key_less_than_expect_error
    def _update_key_error(self, expect_key, key_error_type='less'):
        self.verify_result = False
        target_error_key_list = []
        if key_error_type == 'more':
            target_error_key_list = self.key_more_than_expect_error
        elif key_error_type == 'less':
            target_error_key_list = self.key_less_than_expect_error

        if expect_key not in target_error_key_list:
            target_error_key_list.append(expect_key)

    # 更新vaule类型错误
    def _update_vaule_error(self, target_key, target_data, expect_value, regex_mode=False):
        temp = {}
        if not regex_mode:
            temp = {
                'actual_key': target_key,
                'actual_value': target_data,
                'expect_value': expect_value
            }
        else:
            temp = {
                'actual_key': target_key,
                'actual_value': target_data,
                'expect_regex': expect_value
            }
        self.verify_result = False
        if temp not in self.value_not_match_error:
            self.value_not_match_error.append(temp)

    def _update_len_error(self, target_key, target_data, len_min):
        self.verify_result = False
        temp = {
            'actual_key': target_key,
            'actual_len': len(target_data),
            'min_len': len_min
        }
        if temp not in self.list_len_not_match_error:
            self.list_len_not_match_error.append(temp)

    def _update_enum_error(self, target_key, target_data, expect_enum):
        self.verify_result = False
        temp = {
            'actual_key': target_key,
            'actual_value': target_data,
            'expect_enum': expect_enum
        }
        if temp not in self.enum_not_match_error:
            self.enum_not_match_error.append(temp)

    # 检查是否是matcher匹配的json
    def _is_matcher_json(self, target_json):
        result = False
        try:
            if json_class_key in target_json and contents_key in target_json:
                result = True
        except Exception:
            result = False
        return result

    # 校验错误信息
    @property
    def verify_info(self):
        info = {}
        if len(self.key_less_than_expect_error) > 0:
            info['key_less_than_expect_error'] = self.key_less_than_expect_error

        if len(self.key_more_than_expect_error) > 0:
            info['key_more_than_expect_error'] = self.key_more_than_expect_error

        if len(self.value_not_match_error) > 0:
            info['value_not_match_error'] = self.value_not_match_error

        if len(self.type_not_match_error) > 0:
            info['type_not_match_error'] = self.type_not_match_error

        if len(self.list_len_not_match_error) > 0:
            info['list_len_not_match_error'] = self.list_len_not_match_error

        if len(self.enum_not_match_error) > 0:
            info['enum_not_match_error'] = self.enum_not_match_error
        return info


# json校验类
class PactJsonVerify(PactVerify):

    def __init__(self, pact_json, hard_mode=True, separator='$'):
        pact_json = pact_json
        matcher = change_pact_json_to_obj(pact_json, separator=separator)
        super().__init__(matcher, hard_mode=hard_mode)
