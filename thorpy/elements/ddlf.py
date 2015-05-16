from pygame import MOUSEMOTION, Rect

from thorpy.elements._explorerutils._dirviewer import _DirViewer, _HeavyDirViewer
from thorpy.elements.element import Element
from thorpy.miscgui.reaction import Reaction
from thorpy.miscgui import constants, functions, parameters, style, painterstyle


class DropDownListFast(Element):

    def __init__(self,
                 size,
                 titles,
                 elements=None,
                 normal_params=None,
                 heavy=False,
                 folders=None,
                 margins=None,
                 has_lift=True):
        margins = style.DDL_MARGINS if margins is None else margins
        self._clicked = None
        Element.__init__(self, elements=elements, normal_params=normal_params)
        painter = functions.obtain_valid_painter(painterstyle.BOX_PAINTER,
                                                 pressed=True,
##                                                 color=style.DEF_COLOR2,
                                                 size=size,
                                                 radius=style.BOX_RADIUS)
        self.set_painter(painter)
        self._margins = margins
        self._heavy = heavy
        self._dv = self._get_dirviewer(titles, size, folders)
        reac_motion= Reaction(MOUSEMOTION,
                              self._reaction_motion,
                              reac_name=constants.REAC_MOTION)
        self.add_reaction(reac_motion)
        self._cursor_pos = (-1, -1)
        self._has_lift = has_lift
        self._menu = None
        self._set_selecter()
        self._force_lift = False

    def add_lift(self, axis="vertical", typ="dv"): #! normal or dv?
        Element.add_lift(self, axis, typ)
        self._has_lift = True

    def _get_dirviewer_coords(self, pos):
        r = self.get_fus_rect()
        return pos[0] - r[0], pos[1] - r[1]

    def _reaction_motion(self, event):
        beeing_hovered = self.collide(event.pos, self.current_state_key)
        if beeing_hovered:
            self._cursor_pos = self._get_dirviewer_coords(event.pos)
            self.unblit()
            self.blit()
            self.update()
            self._cursor_pos = (-1, -1)

    def solo_blit(self):
        Element.solo_blit(self)
        self.refresh()

    def finish(self):
        Element.finish(self)
        (x, y) = self.is_family_bigger()
        if (y and self._has_lift) or self._force_lift:
            self.add_lift(typ="dv")
##            self._lift.active_wheel = True
            self._lift.active_wheel = False

    def set_main_color(self, color, state=None):
        Element.set_main_color(self, color, state)

    def _get_dirviewer(self, titles, size, folders):
        size = (size[0] - self._margins[0], size[1] - self._margins[1])
        if self._heavy:
            return _HeavyDirViewer(files=titles, size=size, folders=folders)
        else:
            return _DirViewer(files=titles, size=size, folders=folders)

    def refresh(self):
        """Blits self.dv on self.screen"""
        self_clip = self.get_clip()
        clipdv = self.surface.get_clip().clip(self_clip)
        old_clip = self.surface.get_clip()
        self.surface.set_clip(clipdv)
        self._dv.blit_on(self.surface, self._cursor_pos, self_clip.topleft)
        self.surface.set_clip(old_clip)

    def change_dirviewer(self, titles, size=None, folders=None):
        if not size:
            size = self._dv.size
        self._dv = self._get_dirviewer(titles, size, folders)
        self.refresh()

    def get_family_rect(self, state=None, only_children=False):
        fr = Element.get_family_rect(self, state, only_children)
        dv_rect = self._dv.get_real_size()
        return Rect(fr.x, fr.y, fr.w, dv_rect[1] + 2 * self._margins[1])

    def _set_selecter(self, menu=None):
        """Set the right reaction for selecting elements in dropdown list."""
        reac_pressed = Reaction(parameters.BUTTON_UNPRESS_EVENT,
                                self._ddlf_reaction_press,
                                {"button": parameters.LEFT_CLICK_BUTTON},
                                reac_name=constants.REAC_PRESSED)
        self.add_reaction(reac_pressed)
        self._clicked = None
        self._menu = menu

    def _ddlf_reaction_press(self, event):
        x, y = self._get_dirviewer_coords(event.pos)
        lift = False
        if self._lift:
            lift = self._lift.collide(event.pos)
        if x < self._dv.size[0] and not lift:
            self._clicked = self._dv.get_txt_at_pix(x, y)
            if self._clicked:
                if self._menu:
                    self._menu.set_leave()
                else:
                    return self._clicked

    def is_family_bigger(self, state=None):
        if state is None:
            state = self.current_state_key
        r = self.get_fus_rect(state)
        sw = r.width
        sh = r.height
        (w, h) = self._dv.get_real_size()
        return ((w > sw), (h > sh))
