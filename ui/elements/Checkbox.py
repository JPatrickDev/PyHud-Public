from ui.layout import XMLElementParameters
from .UIElement import UIElement
import pygame
from ast import literal_eval


class Checkbox(UIElement):

    def __init__(self, x, y, w, h, id, state, parent):
        super().__init__(x, y, w, h, id, parent)
        self.state = state
        if w > h:
            self.draw_h = h - (h / 10)
            self.draw_w = self.draw_h
        else:
            self.draw_w = w - (w / 10)
            self.draw_h = self.draw_w
        self.listener = None
        self.inner_padding = self.draw_h / 4

    def render(self):
        super().render()
        pygame.draw.rect(self.drawSurface, (70, 70, 70),
                         (self.w / 2 - self.draw_w / 2, self.h / 2 - self.draw_h / 2, self.draw_w, self.draw_h), int(self.inner_padding /4))
        if self.state:
            pygame.draw.rect(self.drawSurface, (0, 255, 0),
                             (self.w / 2 - (self.draw_w - self.inner_padding) / 2,
                              self.h / 2 - (self.draw_h - self.inner_padding) / 2, self.draw_w - self.inner_padding,
                              self.draw_h - self.inner_padding))

    def set_listener(self,listener):
        self.listener = listener

    def clicked(self, x, y, button):
        self.state = not self.state
        self.invalidated = True
        if self.listener is not None:
          self.listener(self.state,self)
        return super().clicked(x, y, button)

    def set_state(self,state):
        if state == "True":
            self.state = True
        else:
            self.state = False

    @staticmethod
    def from_XML_element_parameters(params, parent, bounds):
        assert isinstance(params, XMLElementParameters.XMLElementParameters)
        id = params.get_parameter("id", None)
        return Checkbox(bounds[0], bounds[1], bounds[2], bounds[3], id, False,
                        parent)
