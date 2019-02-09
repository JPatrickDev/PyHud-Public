class Dialog:
    def __init__(self, on_load, on_close, parent_app):
        self.on_load = on_load
        self.on_close = on_close
        self.parent_app = parent_app
        self.display_width = -1
        self.display_height = -1
        self.display_x = -1
        self.display_y = -1
        self.background_color = (40, 40, 40, 255)
        self.padding_ratio = 20

    def load(self, display_x, display_y, display_width, display_height):
        self.display_x = display_x
        self.display_y = display_y
        self.display_width = display_width
        self.display_height = display_height
        self.padding_x = self.display_width / self.padding_ratio
        self.padding_y = self.display_height / self.padding_ratio

    def get_all_invalidated_elements(self):
        pass

    def is_invalidated(self):
        pass

    def show(self):
        pass

    def update(self):
        pass

    def invalidate_all(self):
        pass

    def clicked(self, x, y, button):
        pass

    def dragged(self, x, y, button, delta):
        pass

    def close(self, result):
        # TODO
        self.parent_app.parent.close_dialog(result)

    def set_background_color(self,color):
        self.background_color = color