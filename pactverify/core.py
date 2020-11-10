import six, re

json_class_key = 'json_class'
contents_key = 'contents'
mininum_key = 'mininum'
nullable_key = 'nullable'
key_missable_key = 'key_missable'
dict_emptiable_key = 'dict_emptiable'
iterate_list_key = 'iterate_list'
extra_types_key = 'extra_types'
jsonloads_key = 'jsonloads'
dict_key_missable_key = 'dict_key_missable'
example_key = 'example'
type_strict_key = 'type_strict'


# 值匹配
class Matcher(object):
    """Base class for defining complex contract expectations."""

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
            json_class_key: 'Matcher',
            contents_key: {},
            jsonloads_key: self.jsonloads,
            key_missable_key: self.key_missable,
            dict_emptiable_key: self.dict_emptiable,
            nullable_key: self.nullable,
            dict_key_missable_key: self.dict_key_missable
        }
        # dict类型
        if type(self.matcher) == dict:
            for k, v in self.matcher.items():
                if isinstance(v, (Matcher, Like, EachLike, Term, Enum)):
                    matcher_dict[contents_key][k] = v.generate()
                else:
                    matcher_dict[contents_key][k] = v
        # 非dict类型
        else:
            matcher_dict[json_class_key] = 'Matcher'
            matcher_dict[contents_key] = self.matcher
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

    def __init__(self, matcher, minimum=1, jsonloads=False, key_missable=False, nullable=False,
                 dict_key_missable=False, extra_types=[]):
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

        assert type(extra_types) == list, 'extra_types must be list'
        self.extra_types = []
        # matcher为基础数据才有效
        if type(self.matcher) in [type(None), bool, int, float, str]:
            for extra_type in extra_types:
                if type(extra_type) in [type(None), bool, int, float, str]:
                    self.extra_types.append(extra_type)

    def generate(self):
        """
        Generate the value the mock service will return.

        :return: A dict containing the information about the contents of the
            list and the provided minimum number of items for that list.
        :rtype: dict
        """
        return {
            json_class_key: 'EachLike',
            contents_key: from_term(self.matcher),
            mininum_key: self.minimum,
            jsonloads_key: self.jsonloads,
            key_missable_key: self.key_missable,
            nullable_key: self.nullable,
            dict_key_missable_key: self.dict_key_missable,
            extra_types_key: self.extra_types
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
                 dict_key_missable=False, extra_types=[]):
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

        assert type(extra_types) == list, 'extra_types must be list'
        self.extra_types = []
        # matcher为基础数据才有效
        if type(self.matcher) in [type(None), bool, int, float, str]:
            for extra_type in extra_types:
                if type(extra_type) in [type(None), bool, int, float, str]:
                    self.extra_types.append(extra_type)

    def generate(self):
        """
        Return the value that should be used in the request/response.

        :return: A dict containing the information about what the contents of
            the response should be.
        :rtype: dict
        """
        return {
            json_class_key: 'Like',
            contents_key: from_term(self.matcher),
            nullable_key: self.nullable,
            dict_emptiable_key: self.dict_emptiable,
            jsonloads_key: self.jsonloads,
            key_missable_key: self.key_missable,
            dict_key_missable_key: self.dict_key_missable,
            extra_types_key: self.extra_types
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
            json_class_key: 'Term',
            contents_key: from_term(self.matcher),
            example_key: self.example,
            key_missable_key: self.key_missable,
            nullable_key: self.nullable,
            type_strict_key: self.type_strict
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
            json_class_key: 'Enum',
            contents_key: from_term(self.matcher),
            iterate_list_key: self.iterate_list,
            jsonloads_key: self.jsonloads,
            key_missable_key: self.key_missable,
            nullable_key: self.nullable
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


def change_pact_json_to_obj(pact_json, separator='$'):
    """
    json格式数据转换为可执行对象
    :param pact_json:
    :return:
    """
    # 断言关键字
    machers = []
    origin_machers = [Matcher.__name__, EachLike.__name__, Like.__name__, Term.__name__, Enum.__name__]
    # 拼接自定义分割符
    values_key = separator + 'values'
    params_key = separator + 'params'

    for origin_macher in origin_machers:
        machers.append(separator + origin_macher)

    def generate_pactverify_obj(contents):
        if isinstance(contents, dict) and len(contents.keys()) > 0:
            key = list(contents.keys())[0]
            # 断言关键字
            if key in machers:
                item = contents[key]
                params = item.get(params_key) if isinstance(item, dict) and params_key in item else None
                values = item.get(values_key) if isinstance(item, dict) and values_key in item else item
                # 去掉separator标志
                class_name = key.replace(separator, '')
                key_obj = eval(class_name)
                new_values = generate_pactverify_obj(values)
                return key_obj(new_values, **params) if params else key_obj(new_values)
            # 非断言关键字的字典类型
            else:
                new_values = {}
                for k, v in contents.items():
                    new_values[k] = generate_pactverify_obj(v)
                return new_values
        else:
            return contents

    try:
        # 值是字典类型并且关键字是断言关键字
        if isinstance(pact_json, dict) and list(pact_json.keys())[0] in machers:
            res_obj = generate_pactverify_obj(pact_json)
            return res_obj
        else:
            raise Exception("断言关键字{}暂不支持！".format(pact_json.keys()[0]))
    except Exception as e:
        raise Exception('断言数据格式有误！{}'.format(e))


# PactVerify校验异常
class PactVerifyError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
