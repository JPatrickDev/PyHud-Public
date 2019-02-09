from ui.dialogs.Dialog import Dialog


class LayoutDialog(Dialog):
    def __init__(self, layout_file, on_load, on_close, parent_app):
        super().__init__(on_load, on_close, parent_app)
        self.layout_file = layout_file
        self.layout = None
        self.show_buttons = False

    def load(self, display_x, display_y, display_width, display_height):
        super().load(display_x, display_y, display_width, display_height)
        inflator = self.parent_app.parent.layout_inflator

        bottom_spacing = display_height / 10
        if not self.show_buttons:
            bottom_spacing = 0

        self.layout = inflator.inflate_layout(self.layout_file, display_width, display_height - bottom_spacing,
                                              self.parent_app.parent, self.parent_app)
        self.on_load(self.layout)

        if self.show_buttons:
            bottomBar = inflator.inflate_layout(self.parent_app.parent.get_system_resource("layouts/dialog_ok_cancel.xml"),
                                                display_width,bottom_spacing, self.parent_app.parent, self.parent_app)

            self.layout.insert_layout_at(bottomBar, 0, display_height -bottom_spacing)

            self.layout.get_element_by_id("dialog_ok").clickListener = lambda x, y, button: self.close(0)

        return self

    def get_all_invalidated_elements(self):
        if self.layout is None:
            return []
        else:
            return self.layout.get_all_invalidated_elements()

    def is_invalidated(self):
        if self.layout is not None:
            return self.layout.is_invalidated()
        else:
            return False

    def invalidate_all(self):
        if self.layout is not None:
           self.layout.invalidate_children()

    def update(self):
        if self.layout is not None:
            self.layout.update(self)

    def clicked(self, x, y, button):
        if self.layout is not None:
            self.layout.clicked(x - self.display_x, y - self.display_y, button)

    def dragged(self, x, y, button, delta):
        if self.layout is not None:
            self.layout.dragged(x - self.display_x, y - self.display_y, button, delta)

    def set_show_buttons(self,show_buttons):
        self.show_buttons = show_buttons