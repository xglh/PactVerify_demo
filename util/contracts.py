# 契约数据类
from util.matchers import Matcher, Like, EachLike, Term


class Contract:
    test_pact_1 = Matcher({
        "msg": "success",
        "code": 0,
        "data": EachLike({
            "type_id": 249,
            "name": "王者荣耀",
            "order_index": 1,
            "status": 1,
            "subtitle": " ",
            "game_name": "王者荣耀"
        })
    })
