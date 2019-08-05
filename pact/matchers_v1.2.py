"""Classes for defining request and response data that is variable."""
# dev版本
import six, re

'''
新增特性：
1. Like新增nullable属性，nullable为true时，目标值为null时校验通过
2. Like新增dict_emptiable属性，dict_emptiable为true时，目标值为{}时校验通过
'''


# 值匹配
class Matcher(object):
    """Base class for defining complex contract expectations."""
    json_class_key = 'json_class'
    contents_key = 'contents'

    def __init__(self, matcher):
        self.matcher = matcher

        valid_types = (
            type(None), list, dict, int, float, six.string_types)

        assert isinstance(matcher, valid_types), (
            "matcher must be one of '{}', got '{}'".format(
                valid_types, type(matcher)))

    def generate(self):
        """
        Get the value that the mock service should use for this Matcher.

        :rtype: any
        """
        matcher_dict = {
            'json_class': 'Matcher',
            'contents': {}
        }
        # dict类型
        if type(self.matcher) == dict:
            for k, v in self.matcher.items():
                if isinstance(v, (Like, EachLike, Term, Enum)):
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

    def __init__(self, matcher, minimum=1):
        """
        Create a new EachLike.

        :param matcher: The expected value that each item in a list should
            look like, this can be other matchers.
        :type matcher: None, list, dict, int, float, str, unicode, Matcher
        :param minimum: The minimum number of items expected.
            Must be greater than or equal to 1.
        :type minimum: int
        """
        self.matcher = matcher
        assert minimum >= 0, 'Minimum must be greater than or equal to 1'
        # EachLike中只允许嵌套基础数据类型和EachLike类型
        valid_types = (
            type(None), list, dict, int, float, six.string_types, EachLike)

        assert isinstance(matcher, valid_types), (
            "matcher must be one of '{}', got '{}'".format(
                valid_types, type(matcher)))
        self.minimum = minimum

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
            'min': self.minimum
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

    def __init__(self, matcher, nullable=False, dict_emptiable=False):
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
        else:
            self.dict_emptiable = False

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
            'dict_emptiable': self.dict_emptiable
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

    def __init__(self, matcher, example=''):
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
            'example': self.example
        }

    def _regex_test(self):
        m = re.match(self.matcher, str(self.example))
        # 没匹配到
        assert (m is not None), ('Term example regex test fail')


# 枚举匹配
class Enum(Matcher):
    """Base class for defining complex contract expectations."""

    def __init__(self, matcher):
        self.matcher = matcher

        # 枚举类型参数只能为列表
        valid_types = (
            list)

        assert isinstance(matcher, valid_types), (
            "matcher must be one of '{}', got '{}'".format(
                valid_types, type(matcher)))

    def generate(self):
        """
        Get the value that the mock service should use for this Matcher.

        :rtype: any
        """
        return {
            'json_class': 'Enum',
            'contents': from_term(self.matcher)
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

    def __init__(self, matcher):
        self.matcher = matcher
        self.generate_dict = matcher.generate()
        self.verify_result = True
        # key不匹配错误
        self.key_not_macth_error = []
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
        if generate_dict is None:
            generate_dict = self.generate_dict
        # 非matcher校验,严格校验
        if not self._is_matcher_json(generate_dict):
            self._normal_pact_verify(target_key, actual_data, generate_dict)
        else:
            json_class, contents = generate_dict.get(json_class_key), generate_dict.get(contents_key)

            # Matcher严格匹配
            if json_class == 'Matcher':
                if type(contents) != dict:
                    self._check_param_value(target_key, actual_data, contents)
                else:
                    for k, v in contents.items():
                        target_k = target_key
                        if self._check_param_type(target_k, actual_data, dict):
                            target_k = '{}.{}'.format(target_key, k)
                            if self._check_param_key(target_k, actual_data, k):
                                if type(v) == dict and self._is_matcher_json(v):
                                    target_data, target_generate_dict = actual_data.get(k), v
                                    self.verify(target_data, target_k, target_generate_dict)
                                else:
                                    self._check_param_value(target_k, actual_data.get(k), v)
                    # Like校验字段值类型一致
            elif json_class == 'Like':
                nullable, dict_emptiable = generate_dict.get(nullable_key), generate_dict.get(dict_emptiable_key)

                # Like(11)形式
                if type(contents) != dict:
                    self._check_param_type(target_key, actual_data, type(contents), nullable=nullable)
                else:
                    if type(actual_data) == dict:
                        if not self._check_dict_emptiable(actual_data, dict_emptiable):
                            for k, v in contents.items():
                                # contents非dict类型;contents为dict类型,没有嵌套matcher_json
                                target_k = '{}.{}'.format(target_key, k)
                                if type(v) == dict and self._is_matcher_json(v):
                                    if self._check_param_type(target_k, actual_data, dict, nullable=nullable):
                                        # 嵌套term对象,actual_data需包含k
                                        if self._check_param_key(target_k, actual_data, k):
                                            target_data, target_generate_dict = actual_data.get(k), v
                                            self.verify(target_data, target_k, target_generate_dict)
                                else:
                                    if self._check_param_key(target_k, actual_data, k):
                                        self._check_param_type(target_k, actual_data.get(k), type(v), nullable=nullable)
                    else:
                        self._check_param_type(target_key, actual_data, dict, nullable=nullable)

            # EachLike外层校验list类型
            elif json_class == 'EachLike':
                # target_data类型为list
                if self._check_param_type(target_key, actual_data, list):
                    list_min_len = generate_dict.get('min')
                    # 最小长度校验
                    self._check_param_list_len(target_key, actual_data, list_min_len)
                    for i in range(0, len(actual_data)):
                        inner_data = actual_data[i]
                        target_k = '{}.{}'.format(target_key, i)
                        # 多层EachLike嵌套场景
                        if self._is_matcher_json(contents) and contents.get(json_class_key) == 'EachLike':
                            # inner_data数据需为list
                            if self._check_param_type(target_k, inner_data, list):
                                inner_contents = contents.get(contents_key)
                                inner_min_len = contents.get('min')
                                if self._check_param_list_len(target_k, inner_data, inner_min_len):
                                    for inner_i, inner_t in enumerate(inner_data):
                                        target_k_inner = '{}.{}'.format(target_k, inner_i)
                                        target_data = inner_t
                                        target_generate_dict = {
                                            'json_class': 'Like',
                                            'contents': inner_contents
                                        }
                                        # 转Like处理
                                        self.verify(target_data, target_k_inner, target_generate_dict)

                        # 单层eachlike的场景
                        else:
                            target_data = inner_data
                            target_generate_dict = {
                                'json_class': 'Like',
                                'contents': contents
                            }
                            # 转Like处理
                            self.verify(target_data, target_k, target_generate_dict)
            # Term正则匹配
            elif json_class == 'Term':
                regex_str = contents
                example = generate_dict.get('example')
                # example类型校验
                if self._check_param_type(target_key, actual_data, type(example)):
                    self._check_param_value(target_key, actual_data, regex_str, regex_mode=True)

            elif json_class == 'Enum':
                expect_enum = contents
                self._check_enum_element(target_key, actual_data, expect_enum)

    # 正常契约校验,严格匹配
    def _normal_pact_verify(self, target_key, actual_data, generate_dict):
        try:
            for k, v in generate_dict.items():
                # key校验
                target_k = '{}.{}'.format(target_key, k)
                key_check_result = self._check_param_key(target_k, actual_data, k)
                if key_check_result:
                    # 非dict结构直接对比
                    if not (type(v) == dict and self._is_matcher_json(v)):
                        self._check_param_value(target_k, actual_data.get(k), v)
                    # dict结构递归解析
                    else:
                        target_data, target_generate_dict = actual_data.get(k), v
                        self.verify(target_data, target_k, target_generate_dict)

        except AttributeError:
            self._update_type_error(target_key, actual_data, dict)

    # nullable检查
    def _check_nullable(self, target_data, nullable):
        result = False
        # nullable为true时，target_data为None默认通过，不再进行下一步检查
        if nullable and target_data is None:
            result = True
        return result

    # emptiable
    def _check_dict_emptiable(self, target_data, emptiable):
        result = False
        # emptiable为true是，target_data为dict类型切为空是通过，不再进行下一步检查
        if emptiable and type(target_data) == dict and len(target_data) == 0:
            result = True
        return result

    # 校验参数类型
    def _check_param_type(self, target_key, target_data, expect_type, nullable=False):
        check_result = True
        if not self._check_nullable(target_data, nullable):
            if not isinstance(target_data, expect_type):
                check_result = False
                self._update_type_error(target_key, target_data, expect_type)
        return check_result

    # 校验参数key
    def _check_param_key(self, target_key, target_data, expect_key):
        check_result = True
        # target_data非dict类型报type_error
        if type(target_data) != dict:
            check_result = False
            self._update_type_error(target_key, target_data, dict)
        else:
            if expect_key not in ['json_class', 'contents', 'min'] and expect_key not in target_data:
                self.verify_result = check_result = False
                self.key_not_macth_error.append(target_key)
        return check_result

    # 校验参数值
    def _check_param_value(self, target_key, target_data, expect_value, regex_mode=False):
        check_result = True
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
        type_error_key_list = [x['actual_vaule'] for x in self.type_not_match_error]
        if target_data not in type_error_key_list:
            self.type_not_match_error.append(temp)

    # 更新key类型错误
    def _update_key_error(self, expect_key):
        self.verify_result = False
        self.key_not_macth_error.append(expect_key)

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
            'actual_value': target_data,
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
        return {
            'key_not_macth_error': self.key_not_macth_error,
            'value_not_match_error': self.value_not_match_error,
            'type_not_match_error': self.type_not_match_error,
            'list_len_not_match_error': self.list_len_not_match_error,
            'enum_not_match_error': self.enum_not_match_error
        }


# PactVerify校验异常
class PactVerifyError(Exception):

    def __init__(self, message):
        self.message = message
