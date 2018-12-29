from ui.dialogs.Dialog import Dialog


class AppDialog(Dialog):
    def __init__(self, on_load, on_close, parent_app):
        super().__init__(on_load, on_close, parent_app)

    def load(self, display_x, display_y, display_width, display_height):
        super().load(display_x, display_y, display_width, display_height)
        self.parent_app.set_bounds(display_x, display_y, display_width, display_height)
        self.parent_app.init_config()
        self.parent_app.on_load()
        return self

    def get_all_invalidated_elements(self):
        if self.parent_app.layout is None:
            return []
        else:
            return self.parent_app.layout.get_all_invalidated_elements()

    def is_invalidated(self):
        if self.parent_app.layout is not None:
            return self.parent_app.layout.is_invalidated()
        else:
            return False

    def update(self):
        if self.parent_app.layout is not None:
            self.parent_app.layout.update(self)

    def clicked(self, x, y, button):
        if self.parent_app.layout is not None:
            self.parent_app.layout.clicked(x - self.display_x, y - self.display_y, button)

    def dragged(self, x, y, button, delta):
        if self.parent_app.layout is not None:
            self.parent_app.layout.dragged(x - self.display_x, y - self.display_y, button, delta)
