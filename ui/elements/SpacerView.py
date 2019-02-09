from ui.layout import XMLElementParameters
from .UIElement import UIElement
import pygame
from ast import literal_eval


class SpacerView(UIElement):

    def __init__(self, x, y, w, h, id, backgroundColor, parent):
        super().__init__(x, y, w, h, id, parent)
        self.backgroundColor = backgroundColor

    def render(self):
        super().render()
        if (self.backgroundColor != None):
            print("Filling")
            self.drawSurface.fill(self.backgroundColor, (0, 0, self.w, self.h))


    @staticmethod
    def from_XML_element_parameters(params, parent, bounds):
        assert isinstance(params, XMLElementParameters.XMLElementParameters)
        id = params.get_parameter("id",None)
        if id is None:
            # TODO: Logging system
            return None
        background_color = params.get_parameter("background_color", None)
        if background_color is not None:
            background_color = literal_eval(background_color)
        return SpacerView(bounds[0], bounds[1], bounds[2], bounds[3], id, background_color,
                       parent)
