from app.PyHudApp import PyHudApp
from system.util.Event import *
from ui.layout.LayoutInflator import LayoutInflator


class ClockApp(PyHudApp):

    def get_version(self):
        return "1.0"

    def get_name(self):
        return "ClockApp"

    def on_load(self):
        self.prev_time = ""
        self.set_layout_file("test.xml")
        update = lambda: self.updateTime()
        time_update = RepeatEvent(update, 0.25, self)
        self.parent.event_scheduler.add_event(time_update)
        self.updateTime()

    def updateTime(self):
        if self.layout is None:
            return
        next_time = time.strftime('%H:%M')
        if self.prev_time != next_time:
            text_box = self.layout.get_element_by_id("clock_text")
            text_box.set_text(next_time)
            self.prev_time = next_time
