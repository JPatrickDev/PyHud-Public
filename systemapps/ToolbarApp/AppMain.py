from app.PyHudApp import PyHudApp
from ui.layout.LayoutInflator import LayoutInflator
from system.util.EventScheduler import EventScheduler
from system.util.Event import *


class ToolbarApp(PyHudApp):

    def get_version(self):
        return "1.0"

    def get_name(self):
        return "ToolbarApp"

    def on_load(self):
        self.layout = self.set_layout_file("toolbar.xml")

        dock_layout = self.get_config_value("dock_layout")

        self.layout.get_element_by_id("toolbar_dock_grid").adapter = lambda value, view: self.dock_adapter(value, view)
        self.layout.get_element_by_id("toolbar_dock_grid").set_height_value(1)
        self.layout.get_element_by_id("toolbar_dock_grid").setValues(dock_layout)
        self.layout.get_element_by_id("toolbar_dock_grid").item_click_listener = lambda item: self.handle_dock_click(item)

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
        valid = []
        for app in i:
            if app['app_name'] != "ToolbarApp":
                valid.append(app)
        dialog.get_element_by_id("app_grid_view_element").setValues(valid)

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
        app = self.parent.appLoader.load_app_from_info(app_info, self.parent)
        self.parent.show_app_dialog(app, lambda: print("Loaded"), lambda: print("Close"))

    def dock_adapter(self, value, view):
        if value['type'] == "app":
            view.get_element_by_id("image_view").set_image(self.parent.get_app_icon(value['value']))
        elif value['type'] == 'app_grid':
            view.get_element_by_id("image_view").image_width_pct = 0.8
            view.get_element_by_id("image_view").image_height_pct = -1
            view.get_element_by_id("image_view").set_image("system/resources/images/app_grid_icon.png")
        else:
            pass

    def handle_dock_click(self, value):
        if value['type'] == "app":
            self.launch_app_dialog(self.parent.appLoader.get_app_info_from_name(value['value']))
        elif value['type'] == 'app_grid':
            self.show_app_grid()
        else:
            self.parent.changePage(value['value'])