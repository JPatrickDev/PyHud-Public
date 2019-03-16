import math
import time

from ui.layout.UILayout import UILayout
from .UIElement import UIElement
import pygame


class GridView(UIElement):
    def __init__(self, x, y, w, h, id, layout_file, num_cols, parent):
        super().__init__(x, y, w, h, id, parent)
        self.layout_file = layout_file
        self.values = []
        self.currentViews = []
        self.cachedSurfaces = []
        self.scrollPos = 0.0
        self.gravity = 0
        self.i = 0

        self.num_cols = num_cols

        self.scroll_start_time = -1

        self.item_click_listener = None

        self.col_width = w / num_cols

        self.heightValue = 1
        self.row_height = h / self.heightValue

        self.set_height_value(1)

    def set_height_value(self, value):
        self.heightValue = 3
        self.row_height = self.h / self.heightValue
        self.surface = pygame.Surface((int(self.w), int(self.row_height)), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()

    def setValues(self, values):
        self.parent.parent.run_on_new_thread(lambda: self._internal_set_values(values))

    def _internal_set_values(self, values):
        self.values = values
        self.currentViews = []
        # TODO: Should be an easy way to get the current inflator from anywhere
        inflator = self.parent.parent.layout_inflator
        for value in values:
            layout = inflator.inflate_layout(self.layout_file, self.col_width, self.row_height, self.parent.parent,
                                             self.parent)
            assert isinstance(layout, UILayout)
            if self.adapter is not None:
                self.adapter(value, layout)
                self.currentViews.append(layout)
        self.parent.parent.run_on_new_thread(lambda: self.cache_surfaces())
        self.validate_scroll_pos()

    def render(self):
        super().render()
        yPos = -self.scrollPos
        xPos = 0
        i = 0

        if self.gravity is not 0:
            self.validate_scroll_pos()
        for elementSurface in self.cachedSurfaces:
            if yPos >= self.h:
                break
            self.drawSurface.blit(elementSurface, (xPos, yPos))
            xPos += self.col_width
            i += 1
            if i >= self.num_cols:
                i = 0
                xPos = 0
                yPos += self.row_height
        self.scrollPos += self.gravity

        if self.gravity is not 0:
            self.validate_scroll_pos()

        if self.gravity is not 0:
            percent = self.scrollPos / self.getMaxScrollPos()
            yPercent = self.h * percent
            pygame.draw.rect(self.drawSurface, (255, 0, 0), (0, yPercent - 10, 5, 20))
            self.invalidated = True

    def cache_surfaces(self):
        self.cachedSurfaces = []
        for view in self.currentViews:
            view.invalidate_children()
            assert isinstance(view, UILayout)
            firstItem = list(view.elements.keys())[0]
            fill_colour = (0, 0, 0, 0)

          #      view.elements[firstItem].debug_color
            self.surface.fill(fill_colour, (0, 0, self.col_width, self.row_height))
            view.render(self.surface)
            self.cachedSurfaces.append(self.surface.copy().convert_alpha())
            self.invalidated = True

    def clicked(self, x, y, button):
        self.invalidated = True
        self.validate_scroll_pos()
        if self.gravity == 0 or self.scroll_start_time == -1:
            self.item_click(x, y)
        else:
            if abs(self.scroll_start_time - time.time()) > 0.25:
                self.gravity = 0
            else:
                print(str(self.scroll_start_time - time.time()))
        return super().clicked(x, y, button)

    def dispose(self):
        super().dispose()
        self.surface = None
        self.cachedSurfaces = None
        self.currentViews = None
        self.values = None

    def dragged(self, x, y, button, delta):
        super().dragged(x, y, button, delta)
        if self.scroll_start_time == -1:
            self.scroll_start_time = time.time()
        if delta[1] > 0:
            self.gravity = -2 * abs(delta[1])
        elif delta[1] < 0:
            self.gravity = 2 * abs(delta[1])
        self.invalidated = True

    def validate_scroll_pos(self):
        if self.scrollPos < 0:
            self.scrollPos = 0
            self.gravity = 0
            self.invalidated = True
        if self.scrollPos > self.getMaxScrollPos():
            self.scrollPos = self.getMaxScrollPos()
            self.gravity = 0
            self.invalidated = True

        if self.get_row_count() * self.row_height < self.h:
            self.scrollPos = -(self.h / 2 - self.row_height / 2)

    def update(self, parent):
        if self.gravity > 0:
            self.gravity -= 0.01
        elif self.gravity < 0:
            self.gravity += 0.01

        if -0.1 < self.gravity < 0.1:
            self.gravity = 0
            self.scroll_start_time = -1

    def get_row_count(self):
        return math.ceil(self.values.__len__() / self.num_cols)

    def getMaxScrollPos(self):
        return self.row_height * self.get_row_count() - self.h

    def item_click(self, x, y):
        x = x - self.x
        y = y - self.y
        self.validate_scroll_pos()
        grid_x = math.floor(x / self.col_width)
        grid_y = math.floor((y + self.scrollPos) / self.row_height)
        i = grid_x + grid_y * self.num_cols
        if self.values is None:
            return
        if self.item_click_listener is not None:
            if 0 <= i < self.values.__len__():
                self.item_click_listener(self.values[i])
        if 0 <= i < self.values.__len__():
            y_origin = grid_y * self.row_height
            print(str(y_origin))
            print(str((y - self.y - self.scrollPos) - y_origin))
            self.currentViews[i].clicked(x, (y + self.scrollPos) - y_origin, 0)

    @staticmethod
    def from_XML_element_parameters(params, parent, bounds):
        id = params.get_parameter("id", None)
        if id is None:
            # TODO: Logging system
            return None
        layout_file = params.get_parameter("layout_file", None)
        if layout_file is None:
            return None
        num_cols = int(params.get_parameter("num_cols", 1))

        return GridView(bounds[0], bounds[1], bounds[2], bounds[3], id, layout_file, num_cols,
                        parent)
