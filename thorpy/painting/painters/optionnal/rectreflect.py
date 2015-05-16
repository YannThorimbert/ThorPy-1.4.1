from thorpy.painting.painters.classicframe import ClassicFrame
from thorpy.miscgui import style
from thorpy.painting.graphics import linear_v_monogradation


class RectReflectFrame(ClassicFrame):

    def __init__(self, size=style.SIZE, color=style.DEF_COLOR, pressed=False,
                 dark=None, light=None, thick=1, clip="auto",
                 ambient=style.DEF_COLOR3, hfact=0.6):
        self.thick = 1
        if clip is "auto":
            inflation = -2 * thick
            clip = (inflation, inflation)
        ClassicFrame.__init__(self, size, color, pressed, dark, light, thick,
                              clip)
        self.ambient = ambient
        self.hfact = hfact

    def draw(self):
        surface = ClassicFrame.draw(self)
        h = int(self.hfact*self.size[1])
        linear_v_monogradation(surface, 1, h, self.light, self.ambient, 1)
        linear_v_monogradation(surface, h+1, self.size[1], self.dark, self.color, 1)
        return surface

    def get_surface(self):
        surface = self.draw()
        surface.set_clip(self.clip)
        return surface
