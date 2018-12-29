from app.PyHudApp import PyHudApp
from system.util.Event import *
from ui.layout.LayoutInflator import LayoutInflator


class ClockApp(PyHudApp):

    def __init__(self):
        super().__init__()

    def render(self, surface):
        pass

    def get_version(self):
        return "1.0"

    def get_name(self):
        return "ClockApp"

    def on_load(self):
        self.prev_time = ""
        inflator = self.parent.layout_inflator
        assert isinstance(inflator, LayoutInflator)
        layout = inflator.inflate_layout("test.xml", self.w, self.h, self.parent, self)
        super().set_layout(layout)
        update = lambda: self.updateTime()
        time_update = RepeatEvent(update, 0.25, self)
        self.parent.event_scheduler.add_event(time_update)
        self.updateTime()

        self.layout.get_element_by_id("clock_text").clickListener = lambda x, y, button: self.parent.show_dialog(
            "dialog.xml", self, lambda x: print("Loaded" + str(x)), lambda: print("Closed"))

    def updateTime(self):
        if self.layout is None:
            return
        next_time = time.strftime('%H:%M')
        if self.prev_time != next_time:
            text_box = self.layout.get_element_by_id("clock_text")
            text_box.set_text(next_time)
            self.prev_time = next_time
