from app.PyHudApp import PyHudApp
from system.util.Event import *


class NavBarApp(PyHudApp):

    def get_version(self):
        return "1.0"

    def get_name(self):
        return "NavBarApp"

    def on_load(self):
        self.background_color = (40, 40, 40, 255)
        self.currentIcons = []
        layout = self.set_layout_file("navbar.xml")
        layout.get_element_by_id("navbar_icons").adapter = lambda value , view: self.icon_adapter(view, value)
        self.prev_time = ""
        update = lambda: self.updateTime()
        latest = lambda : self.fetch_latest_icons()
        time_update = RepeatEvent(update, 0.25, self)
        self.parent.event_scheduler.add_event(time_update)
        icon_update = RepeatEvent(latest, 300, self)
        self.parent.event_scheduler.add_event(icon_update)
        self.updateTime()
        self.fetch_latest_icons()

    def updateTime(self):
        if self.layout is None:
            return
        next_time = time.strftime('%H:%M')
        if self.prev_time != next_time:
            text_box = self.layout.get_element_by_id("navbar_time")
            text_box.set_text(next_time)
            self.prev_time = next_time

    def icon_adapter(self, view, value):
        view.get_element_by_id("icons_grid_view_layout_icon_image").set_image(value['image'])

    def fetch_latest_icons(self):
        result = self.parent.appLoader.get_all_icons(self.parent)
        self.currentIcons = result
        self.layout.get_element_by_id("navbar_icons").setValues(self.currentIcons)