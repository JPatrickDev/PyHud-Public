from ui.dialogs.Dialog import Dialog
from ui.layout.UILayout import UILayout


class AppDialog(Dialog):
    def __init__(self, on_load, on_close, parent_app):
        super().__init__(on_load, on_close, parent_app)

    def load(self, display_x, display_y, display_width, display_height):
        super().load(display_x, display_y, display_width, display_height)
        self.parent_app.set_bounds(display_x, display_y, display_width, display_height - 50)
        self.parent_app.init_config()
        self.parent_app.on_load()
        inflator = self.parent_app.parent.layout_inflator

        final_layout = UILayout()


        title_bar = inflator.inflate_layout(self.parent_app.parent.get_system_resource("layouts/dialog_title.xml"),
                                            display_width, 50, self.parent_app.parent, self.parent_app)
        title_bar.get_element_by_id("dialog_title").set_text(self.parent_app.get_name())
        title_bar.get_element_by_id("dialog_close_button").clickListener = lambda x,y,b : self.parent_app.parent.close_dialog(2)

        final_layout.insert_layout_at(title_bar, 0, 0)
        final_layout.insert_layout_at(self.parent_app.layout, 0, 50)

        self.parent_app.layout = final_layout



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

    def invalidate_all(self):
        self.parent_app.invalidate_layout()

    def update(self):
        if self.parent_app.layout is not None:
            self.parent_app.layout.update(self)

    def clicked(self, x, y, button):
        if self.parent_app.layout is not None:
            self.parent_app.layout.clicked(x - self.display_x, y - self.display_y, button)

    def dragged(self, x, y, button, delta):
        if self.parent_app.layout is not None:
            self.parent_app.layout.dragged(x - self.display_x, y - self.display_y, button, delta)
