from pygame import RLEACCEL, Surface
from pygame.transform import scale

from thorpy._utils.images import load_image
from thorpy.painting.painters.painter import Painter
from thorpy.miscgui import functions


class ImageFrame(Painter):

    def __init__(self, img_path, alpha=255, colorkey=None, clip=None,
                 pressed=False, mode=None, hovered=False):
        self.alpha = alpha
        self.img_path = img_path
        self.colorkey = colorkey
        self.mode = mode
        size = list(self.init_get_img().get_size())
        W, H = functions.get_screen_size()
        if self.mode == "cut":
            if W < size[0]:
                size[0] = W
            if H < size[1]:
                size[1] = H
        Painter.__init__(self, size=size, clip=clip, pressed=pressed,
                         hovered=hovered)
        self._resized = False

    def set_size(self, size):
        # define a way to resize (deform or cut)
        # refresh self.size
        W, H = functions.get_screen_size()
        if self.mode == "cut":
            if W < size[0]:
                size[0] = W
            if H < size[1]:
                size[1] = H
        Painter.set_size(self, size)
        self._resized = size


    def init_get_img(self):
        """Only to find size of image during initialization."""
        if isinstance(self.img_path, str):
            return load_image(self.img_path)
        else:
            return self.img_path

    def get_surface(self):
        W, H = functions.get_screen_size()
        if isinstance(self.img_path, str):  # load image
            surface = load_image(self.img_path)
        else:  # take image
            surface = self.img_path
        if 0 < self.alpha < 255:
            surface.set_alpha(self.alpha, RLEACCEL)
        if self.mode == "scale to screen":
            surface = scale(surface, (W, H))
            self.size = (W, H)
        elif self.mode == "cut to screen":
            new_surface = Surface((W, H))
            new_surface.blit(surface, (0, 0))
            self.size = (W, H)
        elif self._resized:
            surface = scale(surface, self._resized)
        elif self.mode:
            functions.debug_msg("Unrecognized mode : ", self.mode)
##        elif self._resized:
##            surface = scale(surface, self._resized)
        if self.colorkey:
            surface.set_colorkey(self.colorkey, RLEACCEL)
        surface.set_clip(self.clip)
        if self.alpha < 255:
            return surface.convert_alpha()
        else:
            return surface.convert()
