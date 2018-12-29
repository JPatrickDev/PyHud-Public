from ui.elements.UIElement import UIElement

import pygame


class ImageView(UIElement):
    def __init__(self, x, y, w, h, id, image_width_pct, image_height_pct, image_path, parent):
        super().__init__(x, y, w, h, id, parent)
        self.image_width_pct = image_width_pct
        self.image_height_pct = image_height_pct
        self.image_height_pixels = -1
        self.image_width_pixels = -1
        self.image_path = image_path
        self.image = None
        self.set_image(self.image_path)
        self.draw_x = 0
        self.draw_y = 0

    def set_image(self, path):
        self.invalidated = True
        self.image = pygame.image.load(path)
        self.calculate_size()
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image_width_pixels), int(self.image_height_pixels)))

    def render(self):
        self.drawSurface.fill((0, 0, 0, 0), (0, 0, self.w, self.h))
        if self.image is not None:
            self.drawSurface.blit(self.image, (self.draw_x, self.draw_y))

    def calculate_size(self):
        self.image_width_pixels = self.w
        self.image_height_pixels = self.h
        if self.image_width_pct != -1 and self.image_height_pct != -1:
            return
        if self.image is None:
            return
        if self.image_height_pct == -1:
            image_width = self.w * self.image_width_pct
            ratio = image_width / self.image.get_width()
            image_height = self.image.get_height() * ratio
            self.image_width_pixels = image_width
            self.image_height_pixels = image_height
        if self.image_width_pct == -1:
            image_height = self.h * self.image_height_pct
            ratio = image_height / self.image.get_height()
            image_width = self.image.get_width() * ratio
            self.image_width_pixels = image_width
            self.image_height_pixels = image_height
        self.draw_x = self.w / 2 - self.image_width_pixels / 2
        self.draw_y = self.h / 2 - self.image_height_pixels / 2

    @staticmethod
    def from_XML_element_parameters(params, parent, bounds):
        id = params.get_parameter("id", None)
        if id is None:
            # TODO: Logging system
            return None

        image_path = params.get_parameter("image_path", None)
        if image_path is None:
            return None

        childDict = params.attributes
        pWidth = 1
        pHeight = 1
        if "image_width" in childDict:
            pWidth = childDict['image_width']
            if "image_height" in childDict:
                pHeight = childDict['image_height']
            else:
                pHeight = -1
        if "image_height" in childDict:
            pHeight = childDict['image_height']
            if "image_width" in childDict:
                pWidth = childDict['image_width']
            else:
                pWidth = -1

        return ImageView(bounds[0], bounds[1], bounds[2], bounds[3], id, float(pWidth), float(pHeight), image_path,
                         parent)