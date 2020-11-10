# 接口断言引入契约校验
目录：  
* 一.背景  
* 二.校验原则  
* 三.基本使用  
  + 【python类契约使用】  
  + 【json契约使用】 
  - 1、Matcher类 校验规则：值匹配
  - 2、Like类 校验规则：类型匹配
  - 3、EachLike类 校验规则：数组类型匹配
  - 4、Term类校验规则：正则匹配
  - 5、Enum类 校验规则：枚举匹配
* 四.复杂数据结构匹配规则
  + 1、{{}}格式
  + 2、[[]]格式
  + 3、{[]}格式
* 五. 异常场景匹配
  + 1、null匹配
  + 2、{}匹配
  + 3、json格式字符串匹配
  + 4、key不存在匹配  
  + 5、多类型匹配
  + 6、非强制字段匹配  
* 六.unittest+HTMLTestRunner+契约断言示例
* 七.根据响应结果生成json契约
* 八.优点总结
  
---
## 一.背景
公司前端吐槽后台接口有时会更改返回的数据结构，返回的字段名与字段类型与接口文档不一致，希望有一个快速检测接口返回数据的所有字段名与字段类型的方法  

以下方数据为例，要校验data数组中dict结构中的字段名与字段类型，可以写脚本遍历数据，但是由于每个接口返回的数据结构可能不一致，可能需要针对每个接口做不同的逻辑，所以需要一个比较通用的校验方法
```python
{
	"msg": "success",
	"code": 0,
	"data": [{
			"type_id": 249,
			"name": "王者荣耀",
			"order_index": 1,
			"status": 1,
			"subtitle": " ",
			"game_name": "王者荣耀"
		}, {
			"type_id": 250,
			"name": "绝地求生",
			"order_index": 2,
			"status": 1,
			"subtitle": " ",
			"game_name": "绝地求生"
		}, {
			"type_id": 251,
			"name": "刺激战场",
			"order_index": 3,
			"status": 1,
			"subtitle": " ",
			"game_name": "刺激战场"
		}
	]
}

```

在研究了[契约测试](https://www.pact.net.cn/documentation/what_is_pact.html)后，抽取[pact-python](https://github.com/pact-foundation/pact-python)部分代码，实现：自定义接口返回数据格式(【契约定义】)-实际响应数据格式校验(【契约校验】)的功能

备注：这里的【契约】等同于接口响应数据结构  

-------------
## 二.校验原则

>1.实际返回字段要**严格等于**或者**含契约定义字段**(根据不同匹配模式来确定)  
>2.字段值可以值相等或类型相等  

目标：对返回数据进行**全量(字段名-值/类型)** 校验   
契约定义方式：支持python类契约和json契约
-------------

## 三.基本使用
### 安装：  
```python
pip install pactverify
```
### python类契约示例：
```python
from pactverify.matchers import Matcher, Like, EachLike, Enum, Term, PactVerify

# 定义契约格式
expect_format = Matcher({
    'code': 0,  # code key存在,值相等,code==0
    'msg': 'success',  # msg key存在,值相等,msg=='success'
    # [{}]结构
    'data': EachLike({
        "type_id": 249,  # type_id key存在,值类型相等,type(type_id) == type(249)
        "name": "王者荣耀",  # name key存在,值类型相等,type(name) == type("王者荣耀")
    }),
    'type': Enum([11,22]),
    'list': EachLike(11,minimum=2)
})

# 实际返回数据
actual_data = {
    "msg": "success",
    "code": 1,
    'type': 12,
    "data": [{
        # type_id类型不匹配
        "type_id": '249',
        "name": "王者荣耀"
    }, {
        # 缺少name
        "type_id": 250,
    }, {
        # 比契约定义多index字段
        "type_id": 251,
        "name": "刺激战场",
        "index": 111
    }
    ],
    'list': [11]
}
# hard_mode默认为true,hard_mode = True时,实际返回key必须严格等于预期key;hard_mode = False时,实际返回key包含预期key即可
mPactVerify = PactVerify(expect_format, hard_mode=True)
# 校验实际返回数据
mPactVerify.verify(actual_data)
# 校验结果  False
print(mPactVerify.verify_result)
''' 校验错误信息
错误信息输出actual_key路径：root.data.0.name形式
root为根目录,dict类型拼接key,list类型拼接数组下标(从0开始)
{   
    # 实际key少于预期key错误
	'key_less_than_expect_error': ['root.data.1.name'],
	# 实际key多与预期key错误,只在hard_mode = True时才报该错误
	'key_more_than_expect_error': ['root.data.2.index'],
	# 值不匹配错误
	'value_not_match_error': [{
			'actual_key': 'root.code',
			'actual_value': 1,
			'expect_value': 0
		}
	],
	# 类型不匹配错误
	'type_not_match_error': [{
			'actual_key': 'root.data.0.type_id',
			'actual_vaule': '249',
			'expect_type': 'int'
		}
	],
	# 数组长度不匹配错误
	'list_len_not_match_error': [{
			'actual_key': 'root.list',
			'actual_len': 1,
			'min_len': 2
		}
	],
	# 元祖不匹配错误
	'enum_not_match_error': [{
			'actual_key': 'root.type',
			'actual_value': 12,
			'expect_enum': [11, 22]
		}
	]
}

'''
print(mPactVerify.verify_info)
```

### json契约示例：
```python
from pactverify.matchers import PactJsonVerify

# 定义json契约格式
expect_format = {
    '$Matcher': {
        'code': 0,  # code key存在,值相等,code==0
        'msg': 'success',  # msg key存在,值相等,msg=='success'
        # [{}]结构
        'data': {
            '$EachLike': {
                "type_id": 249,  # type_id key存在,值类型相等,type(type_id) == type(249)
                "name": "王者荣耀",  # name key存在,值类型相等,type(name) == type("王者荣耀")
            }},
        'type': {
            '$Enum': [11, 22]
        },
        'list': {
            '$EachLike': {
                # $values,$params形式传递额外参数
                '$values': 11,
                '$params': {
                    'minimum': 2
                }
            }
        }
    }
}

# 实际返回数据
actual_data = {
    "msg": "success",
    "code": 1,
    'type': 12,
    "data": [{
        # type_id类型不匹配
        "type_id": '249',
        "name": "王者荣耀"
    }, {
        # 缺少name
        "type_id": 250,
    }, {
        # 比契约定义多index字段
        "type_id": 251,
        "name": "刺激战场",
        "index": 111
    }
    ],
    'list': [11]
}
# hard_mode默认为true,hard_mode = True时,实际返回key必须严格等于预期key;hard_mode = False时,实际返回key包含预期key即可
# separator可自定义指定json关键字标识符，默认为$
mPactJsonVerify = PactJsonVerify(expect_format, hard_mode=True, separator='$')
# 校验实际返回数据
mPactJsonVerify.verify(actual_data)
# 校验结果  False
print(mPactJsonVerify.verify_result)
''' 校验错误信息
错误信息输出actual_key路径：root.data.0.name形式
root为根目录,dict类型拼接key,list类型拼接数组下标(从0开始)
{   
    # 实际key少于预期key错误
	'key_less_than_expect_error': ['root.data.1.name'],
	# 实际key多与预期key错误,只在hard_mode = True时才报该错误
	'key_more_than_expect_error': ['root.data.2.index'],
	# 值不匹配错误
	'value_not_match_error': [{
			'actual_key': 'root.code',
			'actual_value': 1,
			'expect_value': 0
		}
	],
	# 类型不匹配错误
	'type_not_match_error': [{
			'actual_key': 'root.data.0.type_id',
			'actual_vaule': '249',
			'expect_type': 'int'
		}
	],
	# 数组长度不匹配错误
	'list_len_not_match_error': [{
			'actual_key': 'root.list',
			'actual_len': 1,
			'min_len': 2
		}
	],
	# 元祖不匹配错误
	'enum_not_match_error': [{
			'actual_key': 'root.type',
			'actual_value': 12,
			'expect_enum': [11, 22]
		}
	]
}
'''
print(mPactJsonVerify.verify_info)
```

##### 说明：
>1. PactVerify与PactJsonVerify校验类只是契约数据不同，其他逻辑保持一致
>2. PactJsonVerify关键字标志符可用PactJsonVerify(separator='$')自定义

### 1. Matcher类  
#### 校验规则：值匹配
```python
# 预期11  python类契约格式
expect_format_1 = Matcher(11)
# 预期11  json契约格式
expect_format_json_1 = {
    '$Matcher': 11
}

# 预期1.0 python类契约格式
expect_format_2 = Matcher(1.0)
# 预期1.0 json契约格式
expect_format_json_2 = {
    '$Matcher': 1.0
}

# 预期'11' python类契约格式
expect_format_3 = Matcher('11')
# 预期'11' json契约格式
expect_format_json_3 = {
    '$Matcher': '11'
}

# 预期返回数据actual为dict结构,actual['k1'] == 'v1'   python类契约格式
expect_format_4 = Matcher({'k1': 'v1'})
# 预期返回数据actual为dict结构,actual['k1'] == 'v1'   json契约格式
expect_format_json_4 = {
    '$Matcher': {'k1': 'v1'}
}
```  
### 2. Like类  
#### 校验规则：类型匹配
```python
# 预期type(11)  python类契约
expect_format_1 = Like(11)
# 预期type(11)  json契约
expect_format_json_1 = {
    '$Like': 11
}

# 预期type(1.0)  python类契约
expect_format_2 = Like(1.0)
# 预期type(1.0)  json契约
expect_format_json_2 = {
    '$Like': 1.0
}


# 预期type('11')  python类契约
expect_format_3 = Like('11')
# 预期type('11')  json契约
expect_format_json_3 = {
    '$Like': '11'
}

# 预期返回数据actual为dict结构，actual['k1'] == type('v1')   python类契约
expect_format_4 = Like({'k1':'v1'})
# 预期返回数据actual为dict结构，actual['k1'] == type('v1')   json契约
expect_format_json_4 =  {
    '$Like': {'k1':'v1'}
}
```
### 3. EachLike类  
#### 校验规则：数组类型匹配
```python
# 预期[type(11)]  python类契约
expect_format_1 = EachLike(11)
# 预期[type(11)]  json契约
expect_format_json_1 = {
    '$EachLike': 11
}

# 预期[type(1.0)]  python类契约
expect_format_2 = EachLike(1.0)
# 预期[type(1.0)]  json契约
expect_format_json_2 = {
    '$EachLike': 1.0
}

# 预期[type('11')]  python类契约
expect_format_3 = EachLike('11')
# 预期[type('11')]  json契约
expect_format_json_3 = {
    '$EachLike': '11'
}

# 预期[Like{'k1':'v1'}]  python类契约
expect_format_4 = EachLike({'k1': 'v1'})
# 预期[Like{'k1':'v1'}]  json契约
expect_format_json_4 = {
    '$EachLike': {'k1': 'v1'}
}

# 预期[Like{'k1':'v1'}]或[],minimum为数组最小长度,默认minimum=1   python类契约
expect_format_5 = EachLike({'k1': 'v1'}, minimum=0)
# 预期[Like{'k1':'v1'}]或[],minimum为数组最小长度,默认minimum=1   python类契约
expect_format_json_5 = {
    '$EachLike': {
        # $values,$params结构用于额外传参
        '$values': {'k1': 'v1'},
        '$params': {'minimum': 0}
    }
}

```

### 4. Term类  
#### 校验规则：正则匹配
```python
# 预期r'^\d{2}$'，并且type(actual_data) == type(example)，example也用来测试正则表达式  python类契约
expect_format_1 = Term(r'^\d{2}$', example=11)
# 预期r'^\d{2}$'，并且type(actual_data) == type(example)，example也用来测试正则表达式  json契约
expect_format_json_1 = {
    '$Term': {
        '$values': r'^\d{2}$',
        '$params': {'example': 11}
    }
}

# 预期r'^\d{2}$'，example用来测试正则表达式，type_strict = False时跳过对example参数类型校验   python类契约
expect_format_2 = Term(r'^\d{2}$', example="11", type_strict=False)
# 预期r'^\d{2}$'，example用来测试正则表达式，type_strict = False时跳过对example参数类型校验   json契约
expect_format_json_2 = {
    '$Term': {
        '$values': r'^\d{2}$',
        '$params': {'example': 11, 'type_strict': False}
    }
}
```

### 5. Enum类  
#### 校验规则：枚举匹配
```python
# 预期11或22  python类契约
expected_format_1 = Enum([11, 22])
# 预期11或22  json契约
expected_format_json_1 = {
    '$Enum': [11, 22]
}

# iterate_list为true时，当目标数据为数组时，会遍历数组中每个元素是否in [11, 22]  python类契约
expected_format_2 = Enum([11, 22], iterate_list=True)
# iterate_list为true时，当目标数据为数组时，会遍历数组中每个元素是否in [11, 22]  json契约
expected_format_json_2 = {
    '$Enum': {
        '$values': [11, 22],
        '$params': {'iterate_list': True}
    }
}

```

-------------

## 四.复杂规则匹配
### 4.1 {{}}格式
```python
actual_data = {
    'code': 0,
    'msg': 'success',
    'data': {
        "id": 1,
        "name": 'lili'
    }
}

# python类契约
expect_format = Like({
    'code': 0,
    'msg': 'success',
    'data': Like({
        "id": 1,
        "name": 'lili'
    })
})

# json契约
expect_format_json = {
	'$Like': {
		'code': 0,
		'msg': 'success',
		'data': {
			'$Like': {
				"id": 1,
				"name": 'lili'
			}
		}
	}
}
```  
### 4.2 [[]]格式
```python
actual_data = [[{
    "id": 1,
    "name": 'lili'
}]]

# python类契约
expect_format = EachLike(EachLike({
    "id": 1,
    "name": 'lili'
}))

# json契约
expect_format_json = {
    '$EachLike': {
        '$EachLike': {
            "id": 1,
            "name": 'lili'
        }
    }
}
```
### 4.3 {[]}格式
```python
actual_data = {
    'code': 0,
    'msg': 'success',
    'data': [{
        "id": 1,
        "name": 'lili'
    },{
        "id": 2,
        "name": 'lilei'
    }]
}

# python类契约
expect_format = Like({
    'code': 0,
    'msg': 'success',
    'data': EachLike({
        "id": 1,
        "name": 'lili'
    })
})

# json契约
expect_format_json = {
    '$Like': {
        'code': 0,
        'msg': 'success',
        'data': {
            '$EachLike': {
                "id": 1,
                "name": 'lili'
            }
        }
    }
}

```
### 4.4 Like-Term嵌套
```python
actual_data = {
    'code': 0,
    'msg': 'success',
    'data': {
        "id": 1,
        "name": 'lili'
    }
}

# python类契约
expect_format = Like({
    'code': 0,
    'msg': 'success',
    'data': Like({
        "id": 1,
        "name": Term(r'\w*', example='lili')
    })
})

# json契约
expect_format = {
    '$Like': {
        'code': 0,
        'msg': 'success',
        'data': {
            '$Like': {
                "id": 1,
                "name": {
                    '$Term': {
                        '$values': r'\w*',
                        '$params': {
                            'example': 'lili'
                        }
                    }
                }
            }
        }
    }
}
```
### 4.5 Like-Matcher嵌套
```python
actual_data = {
    'name': 'lilei',
    'age': 12
}

# python类契约
expect_format = Like({
    # name字段值类型匹配
    'name': 'lilei',
    # age字段值匹配
    'age': Matcher(12),
})

# json契约
expect_format_json = {
    '$Like': {
        # name字段值类型匹配
        'name': 'lilei',
        # age字段值匹配
        'age': {
            '$Matcher': 12
        },
    }
}
```  
#### 说明：
>1. Matcher，Like和EachLike类可以不限层级嵌套，Term和Enum则不能嵌套其他规则
>2. 匹配规则多层嵌套时，内层规则优先生效


-------------

## 五.异常场景匹配
### 5.1 null匹配  
```python
# nullable为true时允许返回null，预期null和（actual为dict结构，actual['k1'] == 'v1' or null）形式   python类契约
expect_format = Matcher({'k1': 'v1'}, nullable=True)
# nullable为true时允许返回null，预期null和（actual为dict结构，actual['k1'] == 'v1' or null）形式   json契约
expect_format_json = {
    '$Matcher': {
        '$values': {'k1': 'v1'},
        '$params': {'nullable': True}
    }
}

# nullable为true时允许返回null，预期null和（actual为dict结构，actual['k1'] == type('v1') or null）形式   python类契约
expect_format = Like({'k1': 'v1'}, nullable=True)
# nullable为true时允许返回null，预期null和（actual为dict结构，actual['k1'] == type('v1') or null）形式   json契约
expect_format_json = {
    '$Like': {
        '$values': {'k1': 'v1'},
        '$params': {'nullable': True}
    }
}

# nullable为true时允许返回null，预期null和[null,{'k1':null}]形式   python类契约
expect_format = EachLike({'k1': 'v1'}, nullable=True)
# nullable为true时允许返回null，预期null和[null,{'k1':null}]形式   json契约
expect_format_json = {
    '$EachLike': {
        '$values': {'k1': 'v1'},
        '$params': {'nullable': True}
    }
}

# nullable为true时允许返回null，预期null和11形式   python类契约
expect_format = Term(r'^\d{2}$', example=11, nullable=True)
# nullable为true时允许返回null，预期null和11形式   json契约
expect_format_json = {
    '$Term': {
        '$values': r'^\d{2}$',
        '$params': {'example': 11, 'nullable': True}
    }
}

# nullable为true时允许返回null，预期null和11/22/33形式   python类契约
expect_format = Enum([11, 22, 33], nullable=True)
# nullable为true时允许返回null，预期null和11/22/33形式   json契约
expect_format_json = {
    '$Enum': {
        '$values': [11, 22, 33],
        '$params': {'nullable': True}
    }
}
```
>**备注：nullable参数在hard_mode = True时也生效**  
### 5.2 {}匹配  
```python
# dict_emptiable为true时，允许返回{}，预期{}和（actual为dict结构，actual['k1'] == 'v1'）形式   python类契约
expect_format = Matcher({'k1': 'v1'}, dict_emptiable=True)
# dict_emptiable为true时，允许返回{}，预期{}和（actual为dict结构，actual['k1'] == 'v1'）形式   json契约
expect_format_json = {
    '$Matcher': {
        '$values': {'k1': 'v1'},
        '$params': {'dict_emptiable': True}
    }
}

# dict_emptiable为true时，允许返回{}，预期{}和（actual为dict结构，actual['k1'] == type('v1')）形式   python类契约
expect_format = Like({'k1': 'v1'}, dict_emptiable=True)
# dict_emptiable为true时，允许返回{}，预期{}和（actual为dict结构，actual['k1'] == type('v1')）形式   json契约
expect_format_json = {
    '$Like': {
        '$values': {'k1': 'v1'},
        '$params': {'dict_emptiable': True}
    }
}
```
>**备注：dict_emptiable在hard_mode = True时也生效**  
### 5.3 json格式字符串匹配  
```python
# actual为"{\"k1\":\"v1\"}"json字符串格式时，先进行json.loads再校验   python类契约
expect_format = Matcher({'k1': 'v1'}, jsonloads=True)
# actual为"{\"k1\":\"v1\"}"json字符串格式时，先进行json.loads再校验   json契约
expect_format_json = {
    '$Matcher': {
        '$values': {'k1': 'v1'},
        '$params': {'jsonloads': True}
    }
}

# actual为"{\"k1\":\"v1\"}"json字符串格式时，先进行json.loads再校验   python类契约
expect_format = Like({'k1': 'v1'}, jsonloads=True)
# actual为"{\"k1\":\"v1\"}"json字符串格式时，先进行json.loads再校验   json契约
expect_format_json = {
    '$Like': {
        '$values': {'k1': 'v1'},
        '$params': {'jsonloads': True}
    }
}

# actual为"[{\"k1\":\"v1\"}]"json字符串格式时，先进行json.loads再校验  python类契约
expect_format = EachLike({'k1': 'v1'}, jsonloads=True)
# actual为"[{\"k1\":\"v1\"}]"json字符串格式时，先进行json.loads再校验  json契约
expect_format = {
    '$EachLike': {
        '$values': {'k1': 'v1'},
        '$params': {'jsonloads': True}
    }
}

# actual为"[11,22]"json字符串格式时，先进行json.loads再校验   python类契约
expected_format = Enum([11, 22], jsonloads=True)
# actual为"[11,22]"json字符串格式时，先进行json.loads再校验   json契约
expected_format_json = {
    '$Enum': {
        '$values': {'k1': 'v1'},
        '$params': {'jsonloads': True}
    }
}
```

### 5.4 key不存在匹配  
```python
# key_missable为true时，允许key不存在，key存在时走正常校验；Matcher,Like,EachLike,Term和Enum类都可使用该属性   python类契约
expect_format = Matcher({
    'code': Like(0, key_missable=True),
    'msg': Matcher('success', key_missable=True),
    'data': EachLike(11, key_missable=True),
    'age': Term(r'^\d{2}$', example=11, key_missable=True),
    'num': Enum([11, 22, 33], key_missable=True)
})
# key_missable为true时，允许key不存在，key存在时走正常校验；Matcher,Like,EachLike,Term和Enum类都可使用该属性   json契约
expect_format_json = {
    '$Matcher': {
        'code': {
            '$Like': {
                '$values': 0,
                '$params': {'key_missable': True}
            }
        },
        'msg': {
            '$Matcher': {
                '$values': 'success',
                '$params': {'key_missable': True}
            }
        },
        'data': {
            '$EachLike': {
                '$values': 11,
                '$params': {'key_missable': True}
            }
        },
        'age': {
            '$Term': {
                '$values': r'^\d{2}$',
                '$params': {'example': 11, 'key_missable': True}
            }
        },
        'num': {
            '$Enum': {
                '$values': [11, 22, 33],
                '$params': {'key_missable': True}
            }
        },
    }}

# dict_key_missable为true时，允许dict结构中的key不存在，但key不能多(hard_mode=true时)，key存在时正常校验  python类契约
expected_format = Matcher({
    'name': 'lilei',
    'age': 12,
    'sex': 'man'
}, dict_key_missable=True)
# dict_key_missable为true时，允许dict结构中的key不存在，但key不能多(hard_mode=true时)，key存在时正常校验  json契约
expected_format_json = {
    '$Matcher': {
        '$values': {
            'name': 'lilei',
            'age': 12,
            'sex': 'man'
        },
        '$params': {'dict_key_missable': True}
    }
}

# dict_key_missable为true时，允许dict结构中的key不存在，但key不能多(hard_mode=true时)，key存在时正常校验   python类契约
expected_format = Like({
    'name': 'lilei',
    'age': 12,
    'sex': 'man'
}, dict_key_missable=True)
# dict_key_missable为true时，允许dict结构中的key不存在，但key不能多(hard_mode=true时)，key存在时正常校验   json契约
expected_format_json = {
    '$Like': {
        '$values': {
            'name': 'lilei',
            'age': 12,
            'sex': 'man'
        },
        '$params': {'dict_key_missable': True}
    }
}

# dict_key_missable为true时，允许dict结构中的key不存在，但key不能多(hard_mode=true时)，key存在时正常校验   python类契约
expected_format = EachLike({
    'name': 'lilei',
    'age': 12,
    'sex': 'man'
}, dict_key_missable=True)
# dict_key_missable为true时，允许dict结构中的key不存在，但key不能多(hard_mode=true时)，key存在时正常校验   json契约
expected_format_json = {
    '$EachLike': {
        '$values': {
            'name': 'lilei',
            'age': 12,
            'sex': 'man'
        },
        '$params': {'dict_key_missable': True}
    }
}
```

### 5.5 多类型匹配  
```python
# actual数据为type(11)或type('11'),extra_types可以添加多个示例数据,对基础数据类型(int,float,boolean,str,None)示例有效,对list dict等类型无效  python类契约
expect_format = Like(11, extra_types=['11'])
# actual数据为type(11)或type('11'),extra_types可以添加多个示例数据,对基础数据类型(int,float,boolean,str,None)示例有效,对list dict等类型无效  json契约
expect_format_json = {
    '$Like': {
        '$values': 11,
        '$params': {'extra_types': ['11']}
    }
}

# actual数据为[type(11)]或[type('11')],extra_types可以添加多个示例数据,对基础数据类型示例(int,float,boolean,str,None)有效,对list dict等类型无效  python类契约
expect_format = EachLike(11, extra_types=['11'])
# actual数据为[type(11)]或[type('11')],extra_types可以添加多个示例数据,对基础数据类型示例(int,float,boolean,str,None)有效,对list dict等类型无效  json契约
expect_format_json = {
    '$EachLike': {
        '$values': 11,
        '$params': {'extra_types': ['11']}
    }
}

```
>**备注：**  
>**1. key_missable在hard_mode = True时也生效**  
>**2. key_missable针对actual_data本身的key，dict_key_missable针对actual_data字典中的key，可以同时生效**  

#### 注意：异常匹配场景越多,代表接口数据格式越不规范
-------------

## 六.配合unittest+requests使用
```python
import unittest, requests, HtmlTestRunner, os
from pactverify.matchers import Matcher, Like, EachLike, Term, Enum, PactVerify


class PactTest(unittest.TestCase):

    def test_config_2(self):
        url = 'http://127.0.0.1:8080/configV2'
        config_rsp = requests.get(url)
        config_contract_format = Matcher({
            "msg": "success",
            "code": 200,
            'name': Enum(['lili', 'xiaohei']),
            'addr': Term(r'深圳*', example='深圳宝安'),
            "data": EachLike({
                "type_id": 249,
                "name": "王者荣耀",
                "order_index": 1,
                "status": 1,
                "subtitle": " ",
                "game_name": "王者荣耀"
            }),
            'data_2':
                EachLike({
                    "type_id": 249,
                    "name": "王者荣耀",
                    "order_index": 1,
                    "status": 1,
                    "subtitle": " ",
                    "game_name": "王者荣耀"
                }, minimum=1)
        })

        mPactVerify = PactVerify(config_contract_format)

        try:
            actual_rsp_json = config_rsp.json()
            mPactVerify.verify(actual_rsp_json)
            assert mPactVerify.verify_result == True
        except Exception:
            # 自定义错误信息,输出到HTMLTestRunner中
            err_msg = 'PactVerify_fail,verify_result:{},verify_info:{}'.format(mPactVerify.verify_result,
                                                                               mPactVerify.verify_info)
            self.fail(err_msg)


if __name__ == '__main__':
    current_path = os.path.abspath(__file__)
    current_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    suite = unittest.defaultTestLoader.discover(current_dir, pattern="test_*.py")
    runner = HtmlTestRunner.HTMLTestRunner(combine_reports=True, report_name="MyReport", add_timestamp=False)
    runner.run(suite)
```

## 七.根据响应结果生成json契约
```python
from pactverify.utils import generate_pact_json_by_response

if __name__ == '__main__':
    response_json = {
        "msg": "success",
        "code": 0,
        "data": [{
            "type_id": 249,
            "name": "王者荣耀",
            "order_index": 1,
            "status": 1,
            "subtitle": " ",
            "game_name": "王者荣耀"
        }, {
            "type_id": 250,
            "name": "绝地求生",
            "order_index": 2,
            "status": 1,
            "subtitle": " ",
            "game_name": "绝地求生"
        }, {
            "type_id": 251,
            "name": "刺激战场",
            "order_index": 3,
            "status": 1,
            "subtitle": " ",
            "game_name": "刺激战场"
        }
        ]
    }
    # 参数说明：响应json数据,契约关键字标识符(默认$)
    pact_json = generate_pact_json_by_response(response_json, separator='$')
    print(pact_json)
    '''
    # 模板生成只会包含$EachLike、$Like,可以根据具体校验需求更改,数组取第一个元素为模板来生成
    {
        '$Like': {
            'msg': 'success',
            'code': 0,
            'data': {
                '$EachLike': {
                    'type_id': 249,
                    'name': '王者荣耀',
                    'order_index': 1,
                    'status': 1,
                    'subtitle': ' ',
                    'game_name': '王者荣耀'
                }
            }
        }
    }
    '''
```  

## 八.优点总结  
>1.显式定义接口断言格式，接口断言更加直观  
>2.可复用接口实际响应数据来定义契约  
>3.能根据响应数据生成json契约