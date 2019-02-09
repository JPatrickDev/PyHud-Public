import random

import pygame
from abc import abstractmethod

from ui.interfaces.Clickable import Clickable


class UIElement(Clickable, object):

    def __init__(self, x, y, w, h, id, parent):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.id = id
        self.debug_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
        self.clickListener = None
        self.invalidated = True
        self.disposed = False
        self.parent = parent

        self.drawSurface = pygame.Surface((int(w), int(h)), pygame.SRCALPHA, 32)
        self.drawSurface = self.drawSurface.convert_alpha()

    def render(self):
        self.drawSurface.fill(self.parent.background_color)
        if self.parent.parent.is_debug():
            self.drawSurface.fill((255,0,0))


    def clicked(self, x, y, button):
        if self.clickListener is not None:
            self.invalidated = True
            return self.clickListener(x, y, button)
        return False

    def dragged(self, x, y, button, delta):
        return False

    def dispose(self):
        self.drawSurface = None
        self.disposed = True

    @abstractmethod
    def update(self, parent):
        pass
