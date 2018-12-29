from ui.font.fonts import Fonts
from ui.layout import XMLElementParameters
from .UIElement import UIElement
import pygame
from ast import literal_eval


class TextBox(UIElement):
    fonts = Fonts()

    def __init__(self, x, y, w, h, id, text, textWidth, textHeight, backgroundColor, parent):
        super().__init__(x, y, w, h, id, parent)
        self.text = text
        self.textWidth = textWidth
        self.textHeight = textHeight
        self.backgroundColor = backgroundColor

    def render(self):
        self.drawSurface.fill((0, 0, 0, 0), (0, 0, self.w, self.h))
        if (self.backgroundColor != None):
            pygame.draw.rect(self.drawSurface, self.backgroundColor, (0, 0, self.w, self.h))
        self.fonts.drawLine(self.text, 0, 0, self.w, self.h, self.w * self.textWidth, self.h * self.textHeight,
                            self.drawSurface)

    def set_text(self, text):
        print(text)
        self.text = text
        self.invalidated = True

    @staticmethod
    def from_XML_element_parameters(params, parent, bounds):
        assert isinstance(params, XMLElementParameters.XMLElementParameters)
        id = params.get_parameter("id",None)
        if id is None:
            # TODO: Logging system
            return None
        text = params.text
        # TODO: Gracefully handle params that exist, but are in the wrong format
        text_width = float(params.get_parameter("text_width", -1))
        text_height = float(params.get_parameter("text_height", -1))
        background_color = params.get_parameter("background_color", None)
        if background_color is not None:
            background_color = literal_eval(background_color)
        return TextBox(bounds[0], bounds[1], bounds[2], bounds[3], id, text, text_width, text_height, background_color,
                       parent)
