"""Intelligent search algorithms"""

import array
import dataclasses
import queue
import typing
from tkinter import messagebox

import cube
import definition
import evaluate


@dataclasses.dataclass
class Node:
    """"""
    __slots__ = "op", "father"
    op: definition.OP
    father: typing.Self

    def __lt__(self, *args, **kw) -> bool:
        return True


def repeat(op: definition.OP, node: Node) -> bool:
    """judge whether the op is repeat"""
    if node and op[0] == node.op[0] and op[1] != node.op[1]:
        return True
    return False


def get_trace(node: Node) -> list[definition.OP]:
    """get trace from data"""
    trace: list[definition.OP] = []
    while node:
        trace.append(node.op)
        node = node.father
    return trace[::-1]


def BFS(
    data: array.array[int],
    counter: typing.Callable[[], bool],
    treelight: typing.Callable[[definition.OP], None] | None
) -> list[definition.OP] | None:
    """Breadth First Search"""
    open: queue.Queue[tuple[Node, list[int]]] = queue.Queue()
    node: Node = None
    while counter():
        if data == definition.TARGET:
            return get_trace(node)
        for op in definition.OPS[::-1]:
            if not repeat(op, node):
                open.put((Node(op, node), data[:]))
        node, data = open.get()
        cube.MagicCube.set(data, *node.op)
        if treelight:
            treelight(get_trace(node))


def DFS(
    data: array.array[int],
    counter: typing.Callable[[], bool],
    treelight: typing.Callable[[definition.OP], None] | None,
    *,
    depth: int
) -> list[definition.OP] | None:
    """Depth First Search"""
    open: queue.LifoQueue[tuple[int, Node, list[int]]] = queue.LifoQueue()
    node: Node = None
    while counter():
        if data == definition.TARGET:
            return get_trace(node)
        if depth:
            for op in definition.OPS:
                if not repeat(op, node):
                    open.put((depth - 1, Node(op, node), data[:]))
        depth, node, data = open.get()
        cube.MagicCube.set(data, *node.op)
        if treelight:
            treelight(get_trace(node))


def UCS(
    data: array.array[int],
    counter: typing.Callable[[], bool],
    treelight: typing.Callable[[definition.OP], None] | None,
) -> list[definition.OP] | None:
    """Uniform Cost Search"""
    open: queue.PriorityQueue[
        tuple[int, Node, list[int]]] = queue.PriorityQueue()
    node: Node = None
    ev: float = 0
    while counter():
        if data == definition.TARGET:
            return get_trace(node)
        for op in definition.OPS:
            if not repeat(op, node):
                f = evaluate.g(ev, op)
                open.put((f, Node(op, node), data[:]))
        ev, node, data = open.get()
        cube.MagicCube.set(data, *node.op)
        if treelight:
            treelight(get_trace(node))


def AS(
    data: array.array[int],
    counter: typing.Callable[[], bool],
    treelight: typing.Callable[[definition.OP], None] | None,
) -> list[definition.OP] | None:
    """A or A Star"""
    open: queue.PriorityQueue[
        tuple[int, Node, list[int]]] = queue.PriorityQueue()
    node: Node = None
    ev: float = 0
    while counter():
        if data == definition.TARGET:
            return get_trace(node)
        for op in definition.OPS:
            if not repeat(op, node):
                f = evaluate.g(ev, op) + evaluate.h(data)
                open.put((f, Node(op, node), data[:]))
        ev, node, data = open.get()
        cube.MagicCube.set(data, *node.op)
        if treelight:
            treelight(get_trace(node))


def HC(
    data: array.array[int],
    counter: typing.Callable[[], bool],
    treelight: typing.Callable[[definition.OP], None] | None,
) -> list[definition.OP] | None:
    """Hill Climbing"""
    try:
        open: queue.PriorityQueue[
            tuple[int, Node, list[int]]] = queue.PriorityQueue()
        node: Node = None
        while counter():
            if data == definition.TARGET:
                return get_trace(node)
            for op in definition.OPS:
                if not repeat(op, node):
                    f = evaluate.h(data)
                    open.put((f, Node(op, node), data[:]))
            _, node, data = open.get()
            cube.MagicCube.set(data, *node.op)
            if treelight:
                treelight(get_trace(node))
    except RecursionError as error:
        messagebox.showwarning("RecursionError", error)


def US(
    data: array.array[int],
    counter: typing.Callable[[], bool],
    treelight: typing.Callable[[definition.OP], None] | None,
    *,
    depth: int,
    algo: definition.Algos
) -> list[definition.OP] | None:
    """Universal Search"""
    open: queue.PriorityQueue[
        tuple[int, Node, list[int]]] = queue.PriorityQueue()
    node: Node = None
    ev: float = 0
    while counter():
        if data == definition.TARGET:
            return get_trace(node)
        if depth:
            for op in definition.OPS:
                if not repeat(op, node):
                    f = evaluate.f(ev, op, data, depth, algo=algo)
                    open.put((f, Node(op, node), data[:]))
        ev, node, data = open.get()
        cube.MagicCube.set(data, *node.op)
        if treelight:
            treelight(get_trace(node))
