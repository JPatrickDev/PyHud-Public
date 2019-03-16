import datetime
import json
import urllib

from app.PyHudApp import PyHudApp
from ui.layout.LayoutInflator import LayoutInflator
from system.util.EventScheduler import EventScheduler
from system.util.Event import *
from nrewebservices.ldbws import Session




class WeatherApp(PyHudApp):


    def __init__(self, headless):
        super().__init__(headless)


    def render(self, surface):
        pass

    def get_version(self):
        return "1.0"

    def get_name(self):
        return "WeatherApp"

    def on_init(self):
        super().on_init()
        self.location = self.get_config_value("location")
        self.api_key = self.get_config_value("api_key")

        update = RepeatEvent(lambda: self.fetch_latest_weather_data(),
                                   float(self.get_config_value("refresh_rate")), self)
        self.parent.event_scheduler.add_event(update)
        self.fetch_latest_weather_data()


    def on_load(self):


        layout = self.set_layout_file("home.xml")
        self.fetch_latest_weather_data()


    def fetch_latest_weather_data(self):
        try:
            with urllib.request.urlopen("https://api.openweathermap.org/data/2.5/weather?id=" + self.location + "&appid=" + self.api_key + "&units=metric") as url:
                data = json.loads(url.read().decode())
                self.latest_data = data
                self.update_ui()
        except Exception:
            pass

    def update_ui(self):
        if self.layout is None:
            return
        if self.latest_data is None:
            return
        if self.headless:
            return
        self.layout.get_element_by_id("location_name").set_text(self.latest_data['name'])

        data = self.latest_data['main']
        self.temp_data = data

        self.layout.get_element_by_id("temp_min").set_text("Min:" + str(self.temp_data['temp_min']) + "°")
        self.layout.get_element_by_id("temp_max").set_text("Max:" + str(self.temp_data['temp_max'])  + "°")
        self.layout.get_element_by_id("temp_current").set_text(str(self.temp_data['temp']) + "°")


    def get_icons_headless(self):
        return []