from thorpy.elements.element import Element
from thorpy.painting.painters.imageframe import ImageFrame
from thorpy.painting.painters.basicframe import BasicFrame
from thorpy.miscgui import functions


class Background(Element):

    def __init__(self, color=None, image=None, elements=None,
                 normal_params=None, mode="scale to screen"):
        """Mode:
            None : if an image is passed, its original size is kept. Otherwise,
        a <color> (white by default) rect of the size of the screen is used as
        background image.
            'scale to screen' : if an image is passed, it is scaled to fit
        screen. Otherwise, see behaviour for None.
            'cut to screen' : if an image is passed, it is shrinked to fit
        screen. Otherwise, see behaviour for None.
        """
        super(Background, self).__init__("", elements, normal_params)
        W, H = functions.get_screen_size()
        if image:
            painter = ImageFrame(image, mode=mode)
        else:
            if color:
                painter = BasicFrame((W, H), color)
            else:
                painter = BasicFrame((W, H), (255, 255, 255))
        self.set_painter(painter)