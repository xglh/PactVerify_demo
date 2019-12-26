"""Classes for defining request and response data that is variable."""

import six, re, json


# 值匹配
class Matcher(object):
    """Base class for defining complex contract expectations."""
    json_class_key = 'json_class'
    contents_key = 'contents'

    def __init__(self, matcher, jsonloads=False, dict_emptiable=False, key_missable=False, nullable=False,
                 dict_key_missable=False):

        valid_types = (
            type(None), list, dict, int, float, six.string_types)

        assert isinstance(matcher, valid_types), (
            "matcher must be one of '{}', got '{}'".format(
                valid_types, type(matcher)))
        self.matcher = matcher
        self.jsonloads = jsonloads
        self.key_missable = key_missable
        # matcher类型为dict时，dict_emptiable参数才有效
        if type(self.matcher) == dict:
            self.dict_emptiable = dict_emptiable
            self.dict_key_missable = dict_key_missable
        else:
            self.dict_emptiable = False
            self.dict_key_missable = False
        self.nullable = nullable

    def generate(self):
        """
        Get the value that the mock service should use for this Matcher.

        :rtype: any
        """
        matcher_dict = {
            'json_class': 'Matcher',
            'contents': {},
            'jsonloads': self.jsonloads,
            'key_missable': self.key_missable,
            'dict_emptiable': self.dict_emptiable,
            'nullable': self.nullable,
            'dict_key_missable': self.dict_key_missable
        }
        # dict类型
        if type(self.matcher) == dict:
            for k, v in self.matcher.items():
                if isinstance(v, (Matcher, Like, EachLike, Term, Enum)):
                    matcher_dict[self.contents_key][k] = v.generate()
                else:
                    matcher_dict[self.contents_key][k] = v
        # 非dict类型
        else:
            matcher_dict[self.json_class_key] = 'Matcher'
            matcher_dict[self.contents_key] = self.matcher
        return matcher_dict


# 数组值类型匹配
class EachLike(Matcher):
    """
    Expect the data to be a list of similar objects.

    Example:

    Would expect the response to be a JSON object, with a comments list. In
    that list should be at least 2 items, and each item should be a `dict`
    with the keys `name` and `text`,
    """

    def __init__(self, matcher, minimum=1, jsonloads=False, key_missable=False, nullable=False, dict_key_missable=False):
        """
        Create a new EachLike.

        :param matcher: The expected value that each item in a list should
            look like, this can be other matchers.
        :type matcher: None, list, dict, int, float, str, unicode, Matcher
        :param minimum: The minimum number of items expected.
            Must be greater than or equal to 1.
        :type minimum: int
        """
        assert minimum >= 0, 'Minimum must be greater than or equal to 1'
        # EachLike中只允许嵌套基础数据类型和EachLike类型
        valid_types = (
            type(None), list, dict, int, float, six.string_types, EachLike)

        assert isinstance(matcher, valid_types), (
            "matcher must be one of '{}', got '{}'".format(
                valid_types, type(matcher)))
        self.matcher = matcher
        self.minimum = minimum
        self.jsonloads = jsonloads
        self.key_missable = key_missable
        self.nullable = nullable
        self.dict_key_missable = dict_key_missable

    def generate(self):
        """
        Generate the value the mock service will return.

        :return: A dict containing the information about the contents of the
            list and the provided minimum number of items for that list.
        :rtype: dict
        """
        return {
            'json_class': 'EachLike',
            'contents': from_term(self.matcher),
            'min': self.minimum,
            'jsonloads': self.jsonloads,
            'key_missable': self.key_missable,
            'nullable': self.nullable,
            'dict_key_missable': self.dict_key_missable
        }


# 值类型匹配
class Like(Matcher):
    """
    Expect the type of the value to be the same as matcher.

    Would expect the response body to be a JSON object, containing the key
    `number`, which would contain an integer. When the consumer runs this
    contract, the value `1111222233334444` will be returned by the mock
    service, instead of a randomly generated value.
    """

    def __init__(self, matcher, nullable=False, dict_emptiable=False, jsonloads=False, key_missable=False,
                 dict_key_missable=False):
        """
        Create a new SomethingLike.

        :param matcher: The object that should be expected. The mock service
            will return this value. When verified against the provider, the
            type of this value will be asserted, while the value will be
            ignored.
        :type matcher: None, list, dict, int, float, str, unicode, Matcher
        """
        # Like中只允许嵌套基础数据类型和Term类型
        valid_types = (
            type(None), list, dict, int, float, six.string_types, Term)

        assert isinstance(matcher, valid_types), (
            "matcher must be one of '{}', got '{}'".format(
                valid_types, type(matcher)))

        self.matcher = matcher
        self.nullable = nullable
        # matcher类型为dict时，dict_emptiable参数才有效
        if type(self.matcher) == dict:
            self.dict_emptiable = dict_emptiable
            self.dict_key_missable = dict_key_missable
        else:
            self.dict_emptiable = False
            self.dict_key_missable = False
        self.jsonloads = jsonloads
        self.key_missable = key_missable

    def generate(self):
        """
        Return the value that should be used in the request/response.

        :return: A dict containing the information about what the contents of
            the response should be.
        :rtype: dict
        """
        return {
            'json_class': 'Like',
            'contents': from_term(self.matcher),
            'nullable': self.nullable,
            'dict_emptiable': self.dict_emptiable,
            'jsonloads': self.jsonloads,
            'key_missable': self.key_missable,
            'dict_key_missable': self.dict_key_missable
        }


# 正则匹配
class Term(Matcher):
    """
    Expect the response to match a specified regular expression.

    Example:


    Would expect the response body to be a JSON object, containing the key
    `name`, which will contain the value `tester`, and `theme` which must be
    one of the values: light, dark, or legacy. When the consumer runs this
    contract, the value `dark` will be returned by the mock service.
    """

    def __init__(self, matcher, example='', key_missable=False, nullable=False, type_strict=True):
        """
        Create a new Term.

        :param matcher: A regular expression to find.
        :type matcher: basestring
        :param generate: A value to be returned by the mock service when
            generating the response to the consumer.
        :type generate: basestring
        """
        self.matcher = matcher
        self.example = example
        self.key_missable = key_missable
        self.nullable = nullable
        self.type_strict = type_strict
        # Term对象matcher只能为string类型
        valid_types = (six.string_types)

        assert isinstance(matcher, valid_types), (
            "matcher must be one of '{}', got '{}'".format(
                valid_types, type(matcher)))
        self._regex_test()

    def generate(self):
        """
        Return the value that should be used in the request/response.

        :return: A dict containing the information about what the contents of
            the response should be, and what should match for the requests.
        :rtype: dict
        """
        return {
            'json_class': 'Term',
            'contents': from_term(self.matcher),
            'example': self.example,
            'key_missable': self.key_missable,
            'nullable': self.nullable,
            'type_strict': self.type_strict
        }

    def _regex_test(self):
        m = re.match(self.matcher, str(self.example))
        # 没匹配到
        assert (m is not None), ('Term example regex test fail')


# 枚举匹配
class Enum(Matcher):
    """Base class for defining complex contract expectations."""

    def __init__(self, matcher, iterate_list=False, jsonloads=False, key_missable=False, nullable=False):
        # 枚举类型参数只能为列表
        valid_types = (
            list)

        assert isinstance(matcher, valid_types), (
            "matcher must be one of '{}', got '{}'".format(
                valid_types, type(matcher)))
        self.matcher = matcher
        self.iterate_list = iterate_list
        self.jsonloads = jsonloads
        self.key_missable = key_missable
        self.nullable = nullable

    def generate(self):
        """
        Get the value that the mock service should use for this Matcher.

        :rtype: any
        """
        return {
            'json_class': 'Enum',
            'contents': from_term(self.matcher),
            'iterate_list': self.iterate_list,
            'jsonloads': self.jsonloads,
            'key_missable': self.key_missable,
            'nullable': self.nullable
        }


def from_term(term):
    """
    Parse the provided term into the JSON for the mock service.

    :param term: The term to be parsed.
    :type term: None, list, dict, int, float, str, unicode, Matcher
    :return: The JSON representation for this term.
    :rtype: dict, list, str
    """
    if term is None:
        return term
    elif isinstance(term, (six.string_types, int, float)):
        return term
    elif isinstance(term, dict):
        return {k: from_term(v) for k, v in term.items()}
    elif isinstance(term, list):
        return [from_term(t) for i, t in enumerate(term)]
    elif issubclass(term.__class__, (Matcher,)):
        return term.generate()
    else:
        raise ValueError('Unknown type: %s' % type(term))


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
        json_class_key, contents_key = 'json_class', 'contents'

        nullable_key, dict_emptiable_key = 'nullable', 'dict_emptiable'

        iterate_list_key = 'iterate_list'

        jsonloads_key = 'jsonloads'
        dict_key_missable_key = 'dict_key_missable'

        if generate_dict is None:
            generate_dict = self.generate_dict

        json_class, contents = generate_dict.get(json_class_key), generate_dict.get(contents_key)
        jsonloads = generate_dict.get(jsonloads_key, False)
        nullable = generate_dict.get(nullable_key, False)
        dict_key_missable = generate_dict.get(dict_key_missable_key, False)

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
                    self._check_param_type(target_key, actual_data, type(contents), nullable=nullable)
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
                        self._check_param_type(target_key, actual_data, dict, nullable=nullable)

            # EachLike外层校验list类型
            elif json_class == 'EachLike':
                # target_data类型为list
                if self._check_param_type(target_key, actual_data, list, nullable=nullable):
                    list_min_len = generate_dict.get('min')
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
                                inner_min_len = contents.get('min')
                                inner_nullable = contents.get('nullable')
                                inner_dict_key_missable = contents.get('dict_key_missable', False)
                                if self._check_param_list_len(target_k, inner_data, inner_min_len):
                                    for inner_i, inner_t in enumerate(inner_data):
                                        target_k_inner = '{}.{}'.format(target_k, inner_i)
                                        target_data_inner = inner_t
                                        target_generate_dict = {
                                            'json_class': 'Like',
                                            'contents': inner_contents,
                                            'nullable': inner_nullable,
                                            'dict_key_missable': inner_dict_key_missable

                                        }
                                        # 转Like处理
                                        self.verify(target_data_inner, target_k_inner, target_generate_dict)

                        # 单层eachlike的场景
                        else:
                            target_data = inner_data
                            target_generate_dict = {
                                'json_class': 'Like',
                                'contents': contents,
                                'nullable': nullable,
                                'dict_key_missable': dict_key_missable
                            }
                            # 转Like处理
                            self.verify(target_data, target_k, target_generate_dict)
            # Term正则匹配
            elif json_class == 'Term':
                regex_str = contents
                example, type_strict = generate_dict.get('example'), generate_dict.get('type_strict')
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
    def _check_param_type(self, target_key, target_data, expect_type, nullable=False, type_strict=True):
        check_result = True
        # nullable校验不通过继续校验
        if not self._check_nullable(target_data, nullable):
            if type_strict and type(target_data) != expect_type:
                check_result = False
                self._update_type_error(target_key, target_data, expect_type)
        # nullable校验通过不继续校验
        else:
            check_result = False
        return check_result

    # 跳过参数key校验   result=True时跳过校验   target_key为实际key，不加拼接路径
    def _skip_check_param_key(self, target_key, target_data, generate_dict):
        result = False
        # skip key校验
        if self._is_matcher_json(generate_dict) and generate_dict.get('key_missable', False) == True:
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
            if not dict_key_missable and expect_key not in ['json_class', 'contents',
                                                            'min'] and expect_key not in target_data:
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
            pact_keys_set = set(['json_class', 'contents', 'min'])
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
                if target_data != expect_value:
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
    def _update_type_error(self, target_key, target_data, expect_type):
        self.verify_result = False
        temp = {
            'actual_key': target_key,
            'actual_vaule': target_data,
            'expect_type': expect_type.__name__
        }
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
        self.value_not_match_error.append(temp)

    def _update_len_error(self, target_key, target_data, len_min):
        self.verify_result = False
        temp = {
            'actual_key': target_key,
            'actual_len': len(target_data),
            'min_len': len_min
        }
        self.list_len_not_match_error.append(temp)

    def _update_enum_error(self, target_key, target_data, expect_enum):
        self.verify_result = False
        temp = {
            'actual_key': target_key,
            'actual_value': target_data,
            'expect_enum': expect_enum
        }
        self.enum_not_match_error.append(temp)

    # 检查是否是matcher匹配的json
    def _is_matcher_json(self, target_json):
        result = False
        try:
            json_class, contents = 'json_class', 'contents'
            if json_class in target_json and contents in target_json:
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


# PactVerify校验异常
class PactVerifyError(Exception):

    def __init__(self, message):
        self.message = message
