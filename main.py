"""Main file"""

import array
import copy
import math
import random
import threading
import tkinter
import typing

import tkintertools as tkt
from tkintertools import tools_3d as t3d

import cube
import definition
import evaluate
import search
import ui

__VERSION__ = "1.2"
__AUTHOR__ = "小康2022"

STOP_SHUFFLE: bool = False
STOP_SEARCH: bool = False
SEARCH_ALGO: int = 5
SEARCH_HEURISTIC: int = 5
MAXIMUM: int = 1


class Space(t3d.Space):
    """My custom Space class"""

    @typing.override
    def space_sort(self) -> None:
        self._items_3d.sort(
            key=lambda item: item._camera_distance(), reverse=True)
        for item in self._items_3d:
            self.lift(item.item)


class CustomShuffle(tkt.Toplevel):
    """A Toplevel of Customizing orders of turning Magic Cube"""

    def __init__(self) -> None:
        tkt.Toplevel.__init__(
            self, root, None, 600, 400, shutdown=self.withdraw)
        self.resizable(False, False)
        self.cv = tkt.Canvas(self, 600, 400, 0, 0, bg="#1F1F1F")
        self.echo = tkt.Canvas(self, 600, 280, 0, 60, bg="black")
        self.ops: list[definition.OP] = []
        self.cards: list[tuple[tkt.Label, tkt.Button, tkt.Switch]] = []
        self.build()

    def appear(self) -> None:
        """appear again"""
        self.deiconify()
        x, y = root.winfo_x(), root.winfo_y()
        tkinter.Toplevel.geometry(self, f'+{x+500}+{y+300}')

    def build(self) -> None:
        """build UI"""
        self.cv.create_rectangle(-1, -1, 601, 60, fill='#1F1F1F')
        self.cv.create_rectangle(-1, 401, 601, 340, fill='#1F1F1F')
        self.echo.create_line(300, 10, 300, 270, fill='grey')
        self.cv.create_text(
            10, 30, text="自定义顺序", font=(tkt.FONT, -28), anchor="w", fill="white")
        tkt.Button(
            self.cv, 490, 350, 100, 40, text="确定", command=self.ok, **ui.button)
        tkt.Button(
            self.cv, 10, 350, 40, 40, text="+", command=lambda: self.modify_cards(True), **ui.button)
        tkt.Button(
            self.cv, 60, 350, 40, 40, text="-", command=lambda: self.modify_cards(False), **ui.button)

    def create_card(self, id: int) -> None:
        """create new card"""
        x = 320 if id & 1 else 20
        y = 20 + 50 * (id // 2)
        self.cards.append((
            tkt.Label(
                self.echo, x, y+2, 40, 36, text=f"{id+1:02}", **ui.label),
            tkt.Button(
                self.echo, x+50, y+2, 120, 36, text='R',
                command=lambda: self.switch_btn(id),
                **ui.button),
            tkt.Switch(
                self.echo, x+180, y+5, 30,
                on=lambda: self.modify_ops(id, 1, True),
                off=lambda: self.modify_ops(id, 1, False),
                ** ui.switch),
        ))

    def switch_btn(self, id: int) -> None:
        """switch button text and its op"""
        op = self.cards[id][1].value
        ind = definition.WAYS.index(op) + 1
        if ind == len(definition.WAYS):
            ind = 0
        op = definition.WAYS[ind]
        self.modify_ops(id, 0, op)
        self.cards[id][1].configure(text=op)

    def modify_ops(self, id: int, ind: int, value: typing.Any) -> None:
        """modify operations list"""
        self.ops[id][ind] = value

    def modify_cards(self, add: bool) -> None:
        """modify cards"""
        if add:
            if len(self.cards) == 10:
                return
            self.ops.append(['R', False])
            self.create_card(len(self.cards))
        elif self.cards:
            self.ops.pop()
            for widget in (card := self.cards.pop()):
                widget.destroy()
            card[-1]._slider.destroy()

    def ok(self) -> None:
        """ok button"""
        if length := len(self.ops):
            count.set(str(length))
            start_shuffle(mc, length, ops=copy.deepcopy(self.ops[::-1]))
        self.withdraw()


class SearchTree(tkt.Toplevel):
    """display a tree when searching"""

    def __init__(self) -> None:
        x, y = root.winfo_x(), root.winfo_y()
        tkt.Toplevel.__init__(
            self, root, 'Search Tree', 600, 670, x+1000, y, bg="#1F1F1F", shutdown=self.close)
        self.resizable(False, False)
        self.transient(root)
        self.cv = tkt.Canvas(self, 600, 670, 0, 0, bg="#1F1F1F")
        self.num = len(mc.steps) + 1
        if self.num <= 1 or self.num >= 10:
            self.num = 10
        self.lines: list[list[int]] = [[] for _ in range(self.num)]
        self.build()

    def close(self) -> None:
        """"""
        search = config.itemcget(t_count, "text")
        steps = config.itemcget(t_steps, "text")
        if steps != "0" or search == "1" or STOP_SEARCH:
            self.destroy()

    def build(self) -> None:
        """build UI"""
        self.cv.create_image(
            -1000, 0, image=bg if switch_bg.get() else None, anchor="nw")
        self.cv.create_line(50, 20, 50, 650, fill='grey')
        self.cv.create_line(550, 20, 550, 650, fill='grey')
        self.key = self.cv.create_line(-5, 20, -5, 650, fill='#0FF')

        for depth in range(self.num):
            Y = 65 + (600 // self.num)*depth
            color = tkt.color(("#00FF00", "#FF0000"), depth / (self.num - 1))
            self.cv.create_text(25, Y, text=f"{depth+1:02}", fill=color)
            self.cv.create_text(
                585, Y, anchor="e", text=f"{definition.BASE_NUM}", fill=color)
            self.cv.create_text(
                595, Y-10, anchor="e", text=f"{depth}", fill=color, font=(tkt.FONT, -16))

            if depth == 0:
                total = definition.BASE_NUM
                delta = 480/total
            elif depth == 1:
                total = definition.BASE_NUM**2
                delta = 480/total
            else:
                total = 480
                delta = 1

            self.lines[depth] = [
                self.cv.create_line(
                    60+delta*i, Y, 60+delta*(i+1), Y, fill="#444", width=15)
                for i in range(total)
            ]

    def light(self, trace: list[definition.OP], index: int = 0, *, highlight: str = None) -> None:
        """light a point"""
        depth = len(trace) - 1
        if depth >= self.num:
            return
        for op in trace:
            index *= definition.BASE_NUM
            index += definition.OPS[::-1].index(op)
        if depth >= 2:
            index = int(index/definition.BASE_NUM**(depth+1)*480)
        color = tkt.color(("#AAAA00", "#CC00CC"), depth / (self.num - 1))
        self.cv.itemconfigure(
            self.lines[depth][index], fill=color if highlight is None else highlight)
        if highlight is not None:
            if depth == 0:
                index *= 480/definition.BASE_NUM
            elif depth == 1:
                index *= 480/definition.BASE_NUM**2
            self.cv.coords(self.key, 60+index, 20, 60+index, 650)


def wrapper(__func: typing.Callable, /, delay: int = 50) -> typing.Callable:
    """to add some delay"""
    def _wrap(*args, **kw) -> None:
        root.after(delay, lambda: __func(*args, **kw))
    return _wrap


@wrapper
def shuffle_cube(mc: cube.MagicCube, count: int, animate: bool = False, ops: list[definition.OP] = None) -> None:
    """shuffle order of the Magic Cube"""
    global STOP_SHUFFLE
    if STOP_SHUFFLE:
        STOP_SHUFFLE = False
        return
    if not math.isclose(float(count), int(count)):
        return
    op, rev = ops.pop() if ops else (
        random.choice(definition.WAYS), random.randint(0, 1))
    mc.turn(op, rev,  ms=100, animate=animate)
    if count:
        root.after(150 if animate else 1,
                   shuffle_cube, mc, count - 1, animate, ops)


def start_shuffle(mc: cube.MagicCube, count: int, *, ops: list[definition.OP]) -> None:
    """start shuffling the Magic Cube"""
    global MAXIMUM
    threading.Thread(target=shuffle_cube, args=(
        mc, count-1, ani.get(), ops), daemon=True).start()
    MAXIMUM = (definition.BASE_NUM-1)**count+1


def stop_shuffle() -> None:
    """stop shuffling the Magic Cube"""
    global STOP_SHUFFLE
    STOP_SHUFFLE = True


def stop_search() -> None:
    """stop Searching the recover method"""
    global STOP_SEARCH
    STOP_SEARCH = True


@wrapper
def recover(mc: cube.MagicCube, trace: list[str, bool], count: int = 0, animate: bool = False) -> None:
    """recover thr Magic Cube"""
    if len(trace) == count:
        mc.steps.clear()
        return
    mc.turn(*trace[count], ms=100, animate=animate)
    root.after(150 if animate else 1, recover, mc, trace, count + 1, animate)


def counter() -> bool:
    """count the times of searching"""
    count = int(config.itemcget(t_count, "text")) + 1
    config.itemconfigure(t_count, text=f'{count}')
    pb.load(count / MAXIMUM)
    return not STOP_SEARCH


def start_search() -> None:
    """start searching the recover method"""

    def func() -> None:
        global STOP_SEARCH
        STOP_SEARCH = False
        evaluate.exponent = len(mc.steps)
        match SEARCH_ALGO:
            case 0: trace = search.BFS(array.array('b', mc.data), counter, tl)
            case 1: trace = search.DFS(array.array('b', mc.data), counter, tl, depth=int(depth.get()) if depth.get().isdigit() else len(mc.steps))
            case 2: trace = search.UCS(array.array('b', mc.data), counter, tl)
            case 3: trace = search.AS(array.array('b', mc.data), counter, tl)
            case 4: trace = search.HC(array.array('b', mc.data), counter, tl)
            case _: trace = [(op, not rev) for op, rev in reversed(mc.steps)]
        if trace is None:
            return
        config.itemconfigure(t_steps, text=f'{len(trace)}')
        if tl:
            for i in range(len(trace)):
                tl(trace[:i+1], highlight="#0FF")
        recover(mc, trace, animate=ani.get())

    clear_data()
    tl = SearchTree().light if tree.get() and SEARCH_ALGO != 5 else None
    threading.Thread(target=func, daemon=True).start()


def show_axis(mc: cube.MagicCube) -> None:
    """show on/off axis"""
    axis = [mc.x, mc.y, mc.z]
    if mc.master.itemcget(axis[0].item, "fill"):
        for a in axis:
            mc.master.itemconfigure(a.item, fill="")
    else:
        for a, c in zip(axis, ['#F00', '#0F0', '#00F']):
            mc.master.itemconfigure(a.item, fill=c)


def show_ind(mc: cube.MagicCube) -> None:
    """show on/off index and position information"""
    fill = "" if mc.master.itemcget(mc.ind[0].item, "fill") else "white"
    for a in mc.ind:
        mc.master.itemconfigure(a.item, fill=fill)


def show_space(mc: cube.MagicCube, flag: bool) -> None:
    """show on/off a little of space between the blocks of Magic Cube"""
    k = 19/20 if flag else 20/19
    for block in mc.blocks:
        block.scale(k, k, k)
        block.update()


def show_bg() -> None:
    """show on/off background image"""
    if config.itemcget(bg2, "image"):
        config.itemconfigure(bg2, image="")
        space.itemconfigure(bg1, image="")
    else:
        config.itemconfigure(bg2, image=bg)
        space.itemconfigure(bg1, image=bg)


def switch_search_algo(id: int) -> None:
    """switch algorithm of searching"""
    global SEARCH_ALGO
    choose_fill = ui.navbutton["color_fill"][:]
    choose_fill[0] = "cornflowerblue"
    choose_outline = ui.navbutton["color_outline"][:]
    choose_outline[0] = "cornflowerblue"
    for btn in (buttons := [nb0, nb1, nb2, nb3, nb4, nb5]):
        btn.configure(
            color_fill=ui.navbutton["color_fill"], color_outline=ui.navbutton["color_outline"])
        btn.state()
    buttons[id].configure(color_fill=choose_fill, color_outline=choose_outline)
    buttons[id].state()
    SEARCH_ALGO = id


def switch_search_heuristic(id: int) -> None:
    """switch heuristic function of searching"""
    global SEARCH_HEURISTIC
    choose_fill = ui.navbutton["color_fill"][:]
    choose_fill[0] = "cornflowerblue"
    choose_outline = ui.navbutton["color_outline"][:]
    choose_outline[0] = "cornflowerblue"
    for btn in (buttons := [ag0, ag1, ag2, ag3, ag4, ag5]):
        btn.configure(
            color_fill=ui.navbutton["color_fill"], color_outline=ui.navbutton["color_outline"])
        btn.state()
    buttons[id].configure(color_fill=choose_fill, color_outline=choose_outline)
    buttons[id].state()
    match SEARCH_HEURISTIC := id:
        case 0: evaluate.h = evaluate.chebyshev
        case 1: evaluate.h = evaluate.euclidean
        case 2: evaluate.h = evaluate.manhattan
        case 3: evaluate.h = evaluate.hamming
        case 4: evaluate.h = evaluate.minkowski
        case _: evaluate.h = evaluate.custom


def clear_data() -> None:
    """clear up the data of searching"""
    config.itemconfigure(t_count, text="0")
    config.itemconfigure(t_steps, text="0")
    pb.load(0)


def scroll_num(entry: tkt.Entry, up: bool) -> None:
    """scroll the num of certain Entry"""
    num = int(entry.get())
    entry.set(f'{num + (1 if up else -1)}')
    if entry._state == 'click':
        entry._cursor_update()


def create_title(canvas: tkt.Canvas, x: int, y: int, text: str) -> None:
    """create a virtual title on Canvas"""
    canvas.create_rectangle(x, y, x+10, y+40, fill='orange', outline='')
    canvas.create_text(x+20, y+20, text=text, fill='white',
                       anchor='w', font=(tkt.FONT, -36))


root = tkt.Tk(f'Magic Cube v{__VERSION__}', 1600, 1000)
root.resizable(False, False)
x = (root.winfo_screenwidth() - 1600) // 2
y = (root.winfo_screenheight() - 1000) // 2
tkinter.Tk.geometry(root, f'+{x}+{y}')
(cs := CustomShuffle()).withdraw()
bg = tkt.PhotoImage('background.png')

space = Space(root, 1000, 1000, 0, 0, bg='black', keep=False)
bg1 = space.create_image(0, 0, image=bg, anchor="nw")

mc = cube.MagicCube(space)

config = tkt.Canvas(root, 600, 1000, 1000, 0, bg='#1F1F1F')
bg2 = config.create_image(-1000, 0, image=bg, anchor="nw")
config.create_line(0, 10, 0, 990, fill='grey')
config.create_text(300, 990, anchor="s", fill='grey', justify="center", font=(
    tkt.FONT, -20), text=f"Author: {__AUTHOR__}\nFramework: tkintertools v2.6.21.1")

create_title(config, 20, 20, "打乱魔方")

config.create_text(20, 100, text='转动次数', anchor="w", fill='white')
count = tkt.Entry(config, 130, 82, 150, 36, **ui.entry)
count.set('5')
tkt.Button(config, 260, 82, 18, 18, text='▲',
           command=lambda: scroll_num(count, True), **ui.small)
tkt.Button(config, 260, 100, 18, 18, text='▼',
           command=lambda: scroll_num(count, False), **ui.small)
config.create_text(20, 150, text='显示动画', anchor="w", fill='white')
ani = tkt.CheckButton(config, 130, 135, 30, value=True, **ui.checkbutton)
tkt.Button(config, 380, 80, 40, 40, text='/',
           command=cs.appear, **ui.button)
tkt.Button(config, 430, 80, 150, 40, text='随机打乱',
           command=lambda: start_shuffle(mc, int(count.get()), ops=None), **ui.button)
tkt.Button(config, 480, 130, 100, 40, text='终止',
           command=stop_shuffle, **ui.button)

create_title(config, 20, 190, "界面设置")

config.create_text(20, 270, text='显示/关闭 坐标轴', anchor="w", fill='white')
tkt.Switch(config, 520, 255, 30,
           on=lambda: show_axis(mc),
           off=lambda: show_axis(mc),
           **ui.switch)
config.create_text(20, 320, text='显示/关闭 辅助索引', anchor="w", fill='white')
tkt.Switch(config, 520, 305, 30,
           on=lambda: show_ind(mc),
           off=lambda: show_ind(mc),
           **ui.switch)
config.create_text(20, 370, text='显示/关闭 空隙', anchor="w", fill='white')
tkt.Switch(config, 520, 355, 30,
           on=lambda: show_space(mc, True),
           off=lambda: show_space(mc, False),
           **ui.switch)
config.create_text(20, 420, text='显示/关闭 背景', anchor="w", fill='white')
switch_bg = tkt.Switch(
    config, 520, 405, 30, on=show_bg, off=show_bg, default=True, **ui.switch)

create_title(config, 20, 460, "算法设置")

config.create_text(20, 540, text='选择算法', anchor="w", fill='white')
nb0 = tkt.Button(config, 130, 520, 70, 40, text='BFS',
                 command=lambda: switch_search_algo(0), **ui.navbutton)
nb1 = tkt.Button(config, 205, 520, 70, 40, text='DFS',
                 command=lambda: switch_search_algo(1),  **ui.navbutton)
nb2 = tkt.Button(config, 280, 520, 70, 40, text='UCS',
                 command=lambda: switch_search_algo(2),  **ui.navbutton)
nb3 = tkt.Button(config, 355, 520, 70, 40, text='A/A*',
                 command=lambda: switch_search_algo(3),  **ui.navbutton)
nb4 = tkt.Button(config, 430, 520, 70, 40, text='HC',
                 command=lambda: switch_search_algo(4),  **ui.navbutton)
nb5 = tkt.Button(config, 505, 520, 70, 40, text='REV',
                 command=lambda: switch_search_algo(5),  **ui.navbutton)
switch_search_algo(SEARCH_ALGO)

config.create_text(20, 590, text='最大深度', anchor="w", fill='white')
depth = tkt.Entry(config, 130, 572, 150, 36, text=('Auto',)*2, **ui.entry)
tkt.Button(config, 260, 572, 18, 18, text='▲',
           command=lambda: scroll_num(depth, True), **ui.small)
tkt.Button(config, 260, 590, 18, 18, text='▼',
           command=lambda: scroll_num(depth, False), **ui.small)
config.create_text(20, 640, text='启发函数', anchor="w", fill='white')
ag0 = tkt.Button(config, 130, 620, 70, 40, text='CBSV',
                 command=lambda: switch_search_heuristic(0), **ui.navbutton)
ag1 = tkt.Button(config, 205, 620, 70, 40, text='ECLD',
                 command=lambda: switch_search_heuristic(1),  **ui.navbutton)
ag2 = tkt.Button(config, 280, 620, 70, 40, text='MHT',
                 command=lambda: switch_search_heuristic(2),  **ui.navbutton)
ag3 = tkt.Button(config, 355, 620, 70, 40, text='HM',
                 command=lambda: switch_search_heuristic(3),  **ui.navbutton)
ag4 = tkt.Button(config, 430, 620, 100, 40, text='MKWSK',
                 command=lambda: switch_search_heuristic(4),  **ui.navbutton)
ag5 = tkt.Button(config, 535, 620, 40, 40, text='h*',
                 command=lambda: switch_search_heuristic(5),  **ui.navbutton)
switch_search_heuristic(SEARCH_HEURISTIC)

create_title(config, 20, 680, "还原魔方")

config.create_text(20, 760, text='参考搜索进度', anchor="w", fill='white')
pb = tkt.ProgressBar(config, 180, 745, 400, 30, **ui.pb)
config.create_text(20, 810, text='显示搜索树', anchor="w", fill='white')
tree = tkt.CheckButton(config, 150, 795, 30, value=True, **ui.checkbutton)
tkt.Button(config, 380, 790, 200, 40, text='开始搜索并还原',
           command=start_search, **ui.button)
config.create_text(20, 860, text='搜索次数', anchor="w", fill='white')
t_count = config.create_text(130, 860, text='0', anchor="w", fill='red')
tkt.Button(config, 480, 840, 100, 40, text='终止',
           command=stop_search, **ui.button)
config.create_text(20, 910, text='还原步数', anchor="w", fill='white')
t_steps = config.create_text(130, 910, text='0', anchor="w", fill='red')
tkt.Button(config, 430, 890, 150, 40, text='清空数据',
           command=clear_data, **ui.button)

root.mainloop()
