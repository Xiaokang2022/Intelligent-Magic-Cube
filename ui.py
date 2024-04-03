"""All themes of the ui"""

from tkintertools import constants

entry = {
    "color_fill": constants.COLOR_NONE,
    "color_outline": ["grey", "#AAA", "white"],
    "color_text": ["white", "white", "white"],
}

func = {
    "color_fill": constants.COLOR_NONE,
    "color_outline": ["grey", "#AAA", "white"],
    "color_text": ["white", "white", "white"],
    "font": "Cambria Math"
}

button = {
    "color_fill": ["", "#333", "#2F2F2F"],
    "color_outline": constants.COLOR_OUTLINE_BUTTON,
    "color_text": ["#AAA", "white", "white"],
}

small = {
    "color_fill": constants.COLOR_NONE,
    "color_outline": constants.COLOR_NONE,
    "color_text": ["#AAA", "white", "white"],
    "font": (constants.FONT, -18)
}

checkbutton = {
    "color_fill": constants.COLOR_NONE,
    "color_outline": ["grey", "#AAA", "white"],
    "color_text": ["#0D0", "#0F0", "#0F0"],
}

navbutton = {
    "color_fill": ["", "royalblue", "blue"],
    "color_outline": ["", "royalblue", "blue"],
    "color_text": ["#DDD", "white", "white"],
}

pb = {
    "color_fill": ["", "olive"],
    "color_outline": constants.COLOR_OUTLINE_BUTTON,
    "color_text": ["white", "white", "white"],
}

switch = {
    "color_fill_on": ["indigo", "indigo", "indigo"],
    "color_fill_off": constants.COLOR_NONE,
    "color_outline_on": ["grey", "#AAA", "white"],
    "color_outline_off": ["grey", "#AAA", "white"],
    "color_fill_slider": ["#DDD", "#DDD", "white"],
    "color_outline_slider": ["#DDD", "#DDD", "white"],
}

label = {
    "color_fill": ["#444", "#444", "#444"],
    "color_outline": ["#444", "#444", "#444"],
    "color_text": ["yellow", "yellow", "yellow"],
}
