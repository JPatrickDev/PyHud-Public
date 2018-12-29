from app.PyHudApp import PyHudApp
from ui.layout.LayoutInflator import LayoutInflator
from system.util.EventScheduler import EventScheduler
from system.util.Event import *


class ToolbarApp(PyHudApp):
    def __init__(self):
        super().__init__()

    def render(self, surface):
        pass

    def get_version(self):
        return "1.0"

    def get_name(self):
        return "ToolbarApp"

    def on_load(self):
        inflator = self.parent.layout_inflator
        assert isinstance(inflator, LayoutInflator)
        layout = inflator.inflate_layout("toolbar.xml", self.w, self.h, self.parent, self)
        super().set_layout(layout)

        self.layout.get_element_by_id("home_button").clickListener = lambda x, y, button: self.changePage("home")
        self.layout.get_element_by_id("trains_button").clickListener = lambda x, y, button: self.changePage(
                                                                                                            "trains")
        self.layout.get_element_by_id("app_grid_button").clickListener = lambda x, y, button: self.show_app_grid()

    def changePage(self, name):
        self.parent.changePage(name)

    def show_app_grid(self):
        self.parent.show_dialog(
            "dialog.xml", self, lambda x: self.initDialog(x), lambda: print("Closed"))

    def initDialog(self, dialog):
        dialog.get_element_by_id("app_grid_view_element").adapter = lambda value, view: self.adapter(value, view)
        dialog.get_element_by_id("app_grid_view_element").item_click_listener = lambda item: self.launch_app_dialog(
            item)
        i = self.parent.appLoader.get_app_info()
        dialog.get_element_by_id("app_grid_view_element").setValues(i)

    def adapter(self, value, view):
        icon = ""
        if "app_icon" in value:
            icon = value['app_icon']
            icon = self.parent.get_app_resource(value, icon)
        else:
            icon = "system/resources/images/default_app_icon.png"
        view.get_element_by_id("image_view").set_image(icon)
        view.get_element_by_id("app_name").set_text(value['app_name'])

    def launch_app_dialog(self, app_info):
        app = self.parent.appLoader.load_app_from_info(app_info,self.parent)
        self.parent.show_app_dialog(app, lambda: print("Loaded"), lambda: print("Close"))
