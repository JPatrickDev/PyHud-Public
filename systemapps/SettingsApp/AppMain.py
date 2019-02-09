import os

from app.PyHudApp import PyHudApp
from ui.layout.LayoutInflator import LayoutInflator
import urllib

class SettingsApp(PyHudApp):

    def get_version(self):
        return "1.0"

    def get_name(self):
        return "SettingsApp"

    def on_load(self):
        inflator = self.parent.layout_inflator
        assert isinstance(inflator, LayoutInflator)
        layout = inflator.inflate_layout("settings.xml", self.w, self.h, self.parent, self)
        all_fonts = next(os.walk('fonts/'))[1]
        layout.get_element_by_id("font_picklist").set_values(all_fonts)
        layout.get_element_by_id("font_picklist").listener = lambda font : self.set_font(font)
        super().set_layout(layout)


    def set_font(self,font):
        self.parent.set_display_config_value("font",font)

    @staticmethod
    def get_icons():
        value = []
        net = SettingsApp.check_net_connection()
        if net:
            value.append({"image": "system/resources/images/icons_wifi_on.png"})
        else:
            value.append({"image": "system/resources/images/icons_wifi_off.png"})
        return value

    @staticmethod
    def check_net_connection():
        try:
            url = "https://www.google.com"
            urllib.request.urlopen(url)
            return True
        except:
            return False
