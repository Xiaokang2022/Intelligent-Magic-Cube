"""All definition"""

import array
import typing

WAYS = 'R', 'U', 'F', 'L', 'D', 'B',  # 'LR', 'UD', 'FB'
"""all ways methods"""

REVERSES = True, False
"""all options of parameter `reserse`"""

OPS = tuple((op, rev) for op in WAYS for rev in REVERSES)
"""all ops of search"""

TARGET = array.array('b', range(27))
"""target state of data"""

BASE_NUM = len(OPS)
"""Base num of search size"""

ALGOS: list[str] = ['BFS', 'DFS', 'UCS', 'AS', 'HC']
"""All searching algorithms"""

SIDES: list[int] = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
"""index of side blocks"""

CORNERS: list[int] = [0, 2,  6, 8, 18, 20, 24, 26]
"""index of corner blocks"""

type Algos = typing.Literal['BFS', 'DFS', 'UCS', 'AS', 'HC']

type Ways = typing.Literal[
    'R', 'L', 'U', 'D', 'F', 'B', 'LR', 'UD', 'FB']

type OP = tuple[Ways, bool]

type Node = tuple[OP, Node]
"""now state and father Node"""
