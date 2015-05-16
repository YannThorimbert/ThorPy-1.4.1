from thorpy.elements.element import Element
from thorpy.elements.clickable import Clickable
from thorpy.miscgui import style

def make_button(text, func=None, params=None):
    button = Clickable(text)
    button.finish()
    button.scale_to_title()
    if func:
        button.user_func = func
    if params:
        button.user_params = params
    return button

def make_text(text, font_size=style.FONT_SIZE, font_color=style.FONT_COLOR):
    params = {"font_color":font_color, "font_size":font_size}
    button = Element(text, normal_params=params)
    if not "\n" in text:
        button.set_style("text")
    button.finish()
    if "\n" in text:
        button.scale_to_title()
        button.set_main_color((0,0,0,0))
    return button
