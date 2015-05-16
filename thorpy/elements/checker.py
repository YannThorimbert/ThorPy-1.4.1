from pygame.constants import RLEACCEL

from thorpy.elements.clickable import Clickable
from thorpy._utils.images import load_image, change_color_on_img_ip
from thorpy.miscgui import constants, functions, style, painterstyle


class Checker(Clickable):

    def __init__(self,
                 name="",
                 elements=None,
                 normal_params=None,
                 press_params=None,
                 value=False,
                 namestyle=None,
                 typ="checkbox",
                 check_img=None,
                 checked=False):
        namestyle=style.STYLE_INSERTER_NAME if namestyle is None else namestyle
        super(Checker, self).__init__("", elements, normal_params,
                                      press_params)
        self._checked = checked
        if value:
            self._checked = value
        self._name_element = self._get_name_element(name, namestyle)  # herite de setter
        self.add_elements(list([self._name_element]))
        self._type = typ
        painter = self._gen_painter()
        self.set_painter(painter, False)
        self._check_img = self._get_check_img(check_img)
        params = {"size": style.CHECK_SIZE,
                  "color": style.COLOR_HOVER_CHECK,
                  "pressed": True}
        if self._type == "checkbox":
            painter_class = painterstyle.CHECKBOX_PAINTER
        elif self._type == "radio":
            painter_class = painterstyle.RADIO_PAINTER
        self.normal_params.polite_set(
            "params hover", {
                "painter": painter_class, "params": params})
        self.normal_params.polite_set("typ hover", "redraw")

    def _get_check_img(self, check_img, colorkey=style.CHECKBOX_IMG_COLORKEY):
        """check_img can either be a path or a pygame Surface"""
        if not check_img:
            if self._type == "checkbox":
                check_img = style.CHECKBOX_IMG
            elif self._type == "radio":
                check_img = style.RADIO_IMG
            check_img = load_image(check_img)
            check_img.set_colorkey(colorkey, RLEACCEL)
            return check_img
        else:
            return check_img

    def _reaction_press(self, pygame_event):
        Clickable._reaction_press(self, pygame_event)
        if self.current_state_key == constants.STATE_PRESSED:
            self.check()

    def set_check_img(self, path, color=constants.BLACK,
                      color_src=constants.BLACK,
                      colorkey=constants.WHITE):
        img = self._get_check_img(path, colorkey=colorkey)
        if color != constants.BLACK:
            img = change_color_on_img_ip(img, color_src, color)
        self._check_img = img

    def _gen_painter(self):
        if self._type == "checkbox":
            return functions.obtain_valid_painter(
                painterstyle.CHECKBOX_PAINTER,
                color=style.DEF_COLOR2,
                size=style.CHECK_SIZE,
                pressed=True)
        elif self._type == "radio":
            return functions.obtain_valid_painter(
                painterstyle.RADIO_PAINTER,
                size=style.CHECK_SIZE, pressed=True)

    def finish(self):
        Clickable.finish(self)
        self._refresh_pos()
        self._name_element.user_func = self.check

    def check(self):
        """Check, blit and update element."""
        self._checked = not self._checked
        self.unblit()
        self.blit()
##        self.transp_blit()
        self.update()

    def solo_blit(self):
        Clickable.solo_blit(self)
        if self._checked:
            clip = self.get_clip()
            r = self._check_img.get_rect()
            r.center = clip.center
            self.surface.blit(self._check_img, r)

    def _get_name_element(self, name, namestyle):
        painter = functions.obtain_valid_painter(
            painterstyle.CHECKER_NAME_PAINTER,
            size=style.SIZE)
        el = Clickable(name)
        el.set_painter(painter)
        if namestyle:
            el.set_style(namestyle)
        el.finish()
        return el

    def unblit(self, rect=None):
        self._name_element.unblit(rect)
        Clickable.unblit(self, rect)

    def transp_blit(self):
        a = self.get_oldest_children_ancester()
        r = self.get_storer_rect()
        a.unblit(r)
        a.partial_blit(None, r)

    def _refresh_pos(self):
        l = self.get_fus_topleft()[0]
        (x, y) = self.get_fus_center()
        l -= self._name_element.get_fus_size()[0] + 5
        self._name_element.set_center((None, y))
        self._name_element.set_topleft((l, None))

    def get_storer_rect(self):
        return self.get_family_rect(constants.STATE_NORMAL)

    def get_value(self):
        return self._checked

    def set_font_color(self, color, state=None, center_title=True):
        """set font color for a given state"""
        Clickable.set_font_color(self, color, state, center_title)
        self._name_element.set_font_color(color, state, center_title)

    def set_font_size(self, size, state=None, center_title=True):
        """set font color for a given state"""
        Clickable.set_font_size(self, size, state, center_title)
        self._name_element.set_font_size(size, state, center_title)

    def set_font_effects(self, biu, state=None, center=True, preserve=False):
        """biu = tuple : (bold, italic, underline)"""
        CLickable.set_font_effects(self, bio, state, center, preserve)
        self._name_element.set_font_effects(biu, state, center, preserve)

    def get_help_rect(self):
        return self.get_family_rect()
