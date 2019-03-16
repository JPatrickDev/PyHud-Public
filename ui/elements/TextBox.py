from ui.layout import XMLElementParameters
from .UIElement import UIElement
import pygame
from ast import literal_eval


class TextBox(UIElement):

    def __init__(self, x, y, w, h, id, text, textWidth, textHeight, backgroundColor, editable, font_size, parent):
        super().__init__(x, y, w, h, id, parent)
        self.text = text
        self.textWidth = textWidth
        self.textHeight = textHeight
        self.backgroundColor = backgroundColor
        self.editable = editable
        self.font_size = font_size

    def render(self):
        super().render()
        if (self.backgroundColor != None):
            pygame.draw.rect(self.drawSurface, self.backgroundColor, (0, 0, self.w, self.h))
        self.parent.parent.font_system.drawLine(self.text, 0, 0, self.w, self.h, self.textWidth,
                                                self.textHeight,
                                                self.drawSurface, self.font_size)

    def clicked(self, x, y, button):
        if not self.editable:
            return super().clicked(x, y, button)
        else:
            self.parent.parent.show_keyboard_dialog(self, self.parent)

    def set_text(self, text):
        self.text = text
        self.invalidated = True

    @staticmethod
    def from_XML_element_parameters(params, parent, bounds):
        assert isinstance(params, XMLElementParameters.XMLElementParameters)
        id = params.get_parameter("id", None)
        if id is None:
            # TODO: Logging system
            return None
        text = params.text
        if text is None:
            text = ""
        # TODO: Gracefully handle params that exist, but are in the wrong format
        text_width = float(params.get_parameter("text_width", -1))
        text_height = float(params.get_parameter("text_height", -1))

        # Legacy support
        if text_width == -1:
            text_width = float(params.get_parameter("textWidth", -1))
        if text_height == -1:
            text_height = float(params.get_parameter("textHeight", -1))

        background_color = params.get_parameter("background_color", None)
        if background_color is not None:
            background_color = literal_eval(background_color)
        editable = params.get_parameter("editable", "False")
        font_size = params.get_parameter("font_size", -1)
        print("Font_size: " + str(font_size))
        return TextBox(bounds[0], bounds[1], bounds[2], bounds[3], id, text, text_width, text_height, background_color,
                       editable == "True", font_size,
                       parent)
