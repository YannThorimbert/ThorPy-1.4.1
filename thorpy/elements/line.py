from thorpy.elements.element import Element
from thorpy.painting.painters.classicframe import ClassicFrame

class Line(Element):
    """Vertical or horizontal graphical Line."""

    def __init__(self, size, type_, color=None, pressed=True):
        """Set type_ to 'horizontal' or 'vertical' in order to produce a graphi-
        cal line of desired, color, size [px].
        """
        Element.__init__(self)
        self.size = size
        self.type = type_
        if type_ == "horizontal" or type_ == "h":
            size = (size, 2)
        elif type_ == "vertical" or type_ == "v":
            size = (2, size)
        painter = ClassicFrame(size, color, pressed)
        self.set_painter(painter)