import random


class UILayout(object):

    def __init__(self):
        self.elements = {}
        self.debug_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)

    def render(self, surface):
       # surface.fill(self.debug_color)
        for element in self.elements.values():
            if element.invalidated and not element.disposed:
                # Invalidate first, so the element can be re-invalidated inside the render method
                element.invalidated = False
                element.render()
                surface.blit(element.drawSurface, (element.x, element.y))

    def get_element_by_id(self, id):
        if id in self.elements:
            return self.elements[id]
        return None

    def get_element_at(self, x, y):
        for id, element in self.elements.items():
            if element.x < x < element.x + element.w:
                if element.y < y < element.y + element.h:
                    return element
        return None

    def invalidate_children(self):
        for element in self.elements.values():
            element.invalidated = True

    def clicked(self, x, y, button):
        element = self.get_element_at(x, y)
        if element is None:
            return False
        else:
            return element.clicked(x, y, button)

    def dragged(self, x, y, button, delta):
        element = self.get_element_at(x, y)
        if element is None:
            return False
        else:
            return element.dragged(x, y, button, delta)

    def is_invalidated(self):
        for element in self.elements.values():
            if element.invalidated:
                return True
        return False

    def dispose(self):
        for element in self.elements.values():
            element.dispose()

    def update(self, parent):
        for element in self.elements.values():
            element.update(self)

    def get_all_invalidated_elements(self):
        values = []
        for element in self.elements.values():
            if element.invalidated:
                values.append(element)
        return values

    def insert_layout_at(self, layout, x, y):
        layout.invalidate_children()
        for element in layout.elements.values():
            element.x = element.x + x
            element.y = element.y + y
            self.elements[element.id] = element
