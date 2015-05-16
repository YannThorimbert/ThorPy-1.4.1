from thorpy.elements.slider import SliderX
from thorpy.elements.element import Element
from thorpy.miscgui import functions, style, painterstyle


class SliderXSetter(SliderX):
    """Like a slider, but has a get_value method"""

    def __init__(self,
                 length,
                 limvals=None,
                 text="",
                 elements=None,
                 normal_params=None,
                 namestyle=None,
                 valuestyle=None,
                 typ=float,
                 initial_value=None):

        namestyle = style.STYLE_SLIDER_NAME if namestyle is None else namestyle
        valuestyle=style.STYLE_SLIDER_VALUE if valuestyle is None else valuestyle
        SliderX.__init__(self, length, limvals, "", elements, normal_params,
                         initial_value)
        self._value_type = typ
        self._round_decimals = 2
        self._name_element = self._get_name_element(text, namestyle)  # herite de setter
        self._value_element = self._get_value_element(valuestyle)
        self.add_elements([self._name_element, self._value_element])

    def finish(self):
        SliderX.finish(self)
        self._refresh_pos()
        self._drag_element.set_setter()
        value = str(self.get_value())
        self._value_element.set_text(value)
##        self.set_prison()

    def set_value(self, value):
        self.get_dragger().place_at(value)
        self.refresh_value()

    def show_value(self, show_value):
        self._value_element.visible = show_value

    def _get_name_element(self, name, namestyle):
        painter = functions.obtain_valid_painter(
            painterstyle.CHECKER_NAME_PAINTER,
            size=style.SIZE)
        el = Element(name)
        el.set_painter(painter)
        if namestyle:
            el.set_style(namestyle)
        el.finish()
        return el

    def _get_value_element(self, valuestyle):
        painter = functions.obtain_valid_painter(
            painterstyle.CHECKER_VALUE_PAINTER,
            size=style.CHECK_SIZE)
        el = Element(str(self.get_value()))
        el.set_painter(painter)
        if valuestyle:
            el.set_style(valuestyle)
        el.finish()
        return el

    def _refresh_pos(self):
        l = self.get_fus_topleft()[0]
        (x, y) = self.get_fus_center()
        l -= self._name_element.get_fus_size()[0] + style.MARGINS[0]
        self._name_element.set_center((None, y))
        self._name_element.set_topleft((l, None))
        w = self.get_fus_rect().right + style.MARGINS[0]
        self._value_element.set_center((None, y))
        self._value_element.set_topleft((w, None))

    def refresh_value(self):
        self._value_element.unblit()
        self._value_element.update()
        value = str(self.get_value())
        self._value_element.set_text(value)
        self._value_element.blit()
        self._value_element.update()

    def get_value(self):
        value = SliderX.get_value(self)
        return self._value_type(value)

    def set_font_color(self, color, state=None, center_title=True):
        """set font color for a given state"""
        SliderX.set_font_color(self, color, state, center_title)
        self._name_element.set_font_color(color, state, center_title)

    def set_font_size(self, size, state=None, center_title=True):
        """set font size for a given state"""
        SliderX.set_font_size(self, size, state, center_title)
        self._name_element.set_font_size(size, state, center_title)

    def set_font_effects(self, biu, state=None, center=True, preserve=False):
        """biu = tuple : (bold, italic, underline)"""
        SliderX.set_font_effects(self, bio, state, center, preserve)
        self._name_element.set_font_effects(biu, state, center, preserve)

    def pix_to_val(self, pix, x0):
        value = SliderX.pix_to_val(self, pix, x0)
        if self._value_type is float:
            return round(value, self._round_decimals)
        elif self._value_type is int:
            return int(round(value))

    def get_help_rect(self):
        return self._name_element.get_help_rect()
