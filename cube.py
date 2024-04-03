"""Magic Cube"""

import array
import math

import tkintertools as tkt
from tkintertools import constants
from tkintertools import tools_3d as t3d

import definition


class Block(t3d.Cuboid):
    """One block of the magic cube"""

    def __init__(
        self,
        canvas: t3d.Canvas3D | t3d.Space,
        x: float,
        y: float,
        z: float,
        length: float,
        width: float,
        height: float
    ) -> None:
        t3d.Cuboid.__init__(
            self, canvas, x, y, z, length, width, height,
            color_fill_up="#DD0",
            color_fill_down="#DDD",
            color_fill_left="orange",
            color_fill_right="#C00",
            color_fill_front="dodgerblue",
            color_fill_back="green",
            boardwidth=2
        )


class MagicCube:
    """powerful magic cube"""

    def __init__(self, canvas: t3d.Canvas3D | t3d.Space) -> None:
        s = 120
        self.master = canvas
        self.x = t3d.Line(canvas, (s*3/2, 0, 0), (999, 0, 0), fill='', width=3)
        self.y = t3d.Line(canvas, (0, s*3/2, 0), (0, 999, 0), fill='', width=3)
        self.z = t3d.Line(canvas, (0, 0, s*3/2), (0, 0, 999), fill='', width=3)
        self.blocks: list[Block] = []
        self.ind: list[t3d.Text3D] = []
        self.data = list(range(27))
        self.steps: list[definition.OP] = []

        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    self.ind.append(
                        t3d.Text3D(
                            canvas, [i*s*1.65, j*s*1.65, k*s*1.65], fill='', text=f'{count:02}\n{(i, j, k)}'))
                    self.blocks.append(
                        Block(canvas, i*s-s/2, j*s-s/2, k*s-s/2, s, s, s))
                    count += 1

        canvas.space_sort()

    @classmethod
    def get(
        cls,
        way: definition.Ways,
        reverse: bool = False
    ) -> list[int] | None:
        """get key information of operation"""
        match way:
            case 'R': ans = [16, 15, 24, 25, 26, 17, 8, 7, 6]
            case 'L': ans = [10, 9, 18, 19, 20, 11, 2, 1, 0]
            case 'U': ans = [14, 2, 5, 8, 17, 26, 23, 20, 11]
            case 'D': ans = [12, 0, 3, 6, 15, 24, 21, 18, 9]
            case 'F': ans = [22, 18, 19, 20, 23, 26, 25, 24, 21]
            case 'B': ans = [4, 0, 1, 2, 5, 8, 7, 6, 3]
            case 'LR': ans = [13, 12, 21, 22, 23, 14, 5, 4, 3]
            case 'UD': ans = [13, 1, 4, 7, 16, 25, 22, 19, 10]
            case 'FB': ans = [13, 9, 10, 11, 14, 17, 16, 15, 12]
            case _: raise ValueError(way)
        return ans[:1] + ans[-1:0:-1] if reverse else ans

    @classmethod
    def set(
        cls,
        data: array.array[int],
        way: definition.Ways,
        reverse: bool = False
    ) -> None:
        """set data with key information"""
        keys = cls.get(way, reverse)
        data[keys[1]], data[keys[3]], data[keys[5]], data[keys[7]] = \
            data[keys[3]], data[keys[5]], data[keys[7]], data[keys[1]]
        data[keys[2]], data[keys[4]], data[keys[6]], data[keys[8]] = \
            data[keys[4]], data[keys[6]], data[keys[8]], data[keys[2]]

    def _turn(
        self,
        blocks: list[Block],
        delta: float,
        axis: tuple[tuple[float, float, float], tuple[float, float, float]],
    ) -> None:
        """turn without any animation almost"""
        for block in blocks:
            block.rotate(delta, axis=axis)
            block.update()
        self.master.space_sort()

    def turn(
        self,
        way: definition.Ways,
        reverse: bool = False,
        *,
        ms: int = 250,
        animate: bool = True
    ) -> None:
        """turn the Magic Cube"""
        delta = -math.pi / 2 if reverse else math.pi / 2
        if animate:
            delta /= (ms * constants.FPS // 1000)
        match way:
            case 'L' | 'R' | 'LR': axis = self.y.coordinates
            case 'U' | 'D' | 'UD': axis = self.z.coordinates
            case 'F' | 'B' | 'FB': axis = self.x.coordinates
        self.steps.append((way, reverse))
        self.set(self.blocks, way, reverse)
        self.set(self.data, way, reverse)
        blocks = [self.blocks[ind] for ind in self.get(way, reverse)]
        if animate:
            tkt.Animation(
                self.master, ms, controller=(math.sin, 0, math.pi),
                callback=lambda _: self._turn(blocks, delta, axis)
            ).run()
        else:
            self._turn(blocks, delta, axis)
