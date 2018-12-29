import datetime

from app.PyHudApp import PyHudApp
from ui.layout.LayoutInflator import LayoutInflator
from system.util.EventScheduler import EventScheduler
from system.util.Event import *
from nrewebservices.ldbws import Session


class TrainApp(PyHudApp):

    def __init__(self):
        super().__init__(self)
        self.lastKnown = None
        self.lastUpdateTime = ""
        self.session = None

    def render(self, surface):
        pass

    def get_version(self):
        return "1.0"

    def get_name(self):
        return "TrainApp"

    def on_load(self):
        # TODO: Add a set_layout(filename) method to AppMain to reduce this boilerplate code:
        # The 4 lines below should be replaced with just set_layout("test.xml")
        inflator = self.parent.layout_inflator
        assert isinstance(inflator, LayoutInflator)
        layout = inflator.inflate_layout("test.xml", self.w, self.h, self.parent, self)
        super().set_layout(self, layout)

        layout.get_element_by_id("station_code").set_text(self.get_config_value(self, "station_code"))
        self.listLayout = layout.get_element_by_id("train_list_view")
        self.listLayout.adapter = lambda value, view: self.adapter(self,value, view)

        train_update = RepeatEvent(lambda: self.updateTrainData(self),
                                   float(self.get_config_value(self, "refresh_rate")), self)
        self.parent.event_scheduler.add_event(train_update)
        self.updateTrainData(self)

    def adapter(self, value, view):
        view.get_element_by_id("dest").set_text(
            str(value.destination))
        view.get_element_by_id("std").set_text(
            str(value.std))
        view.get_element_by_id("etd").set_text(str(value.etd))

    def updateTrainData(self):
        if self.session is None:
            self.initWSDL(self)
        if self.session is None:
            return
        board = self.session.get_station_board(self.get_config_value(self, "station_code"), rows=25,
                                               include_departures=True,
                                               include_arrivals=False, time_offset=0, time_window=120)
        self.lastKnown = board.train_services
        self.lastUpdateTime = self.getCurrentTime(self)
        self.listLayout.setValues(self.lastKnown)

    def initWSDL(self):
        try:
            API_URL = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01'
            self.session = Session(API_URL, self.get_config_value(self, "api_key"))
        except Exception as e:
            print(e)
            print("Error connecting to Darwin")

    def getCurrentTime(self):
        return datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
import datetime

from app.PyHudApp import PyHudApp
from ui.layout.LayoutInflator import LayoutInflator
from system.util.EventScheduler import EventScheduler
from system.util.Event import *
from nrewebservices.ldbws import Session


class TrainApp(PyHudApp):

    def __init__(self):
        super().__init__()
        self.lastKnown = None
        self.lastUpdateTime = ""
        self.session = None

    def render(self, surface):
        pass

    def get_version(self):
        return "1.0"

    def get_name(self):
        return "TrainApp"

    def on_load(self):
        # TODO: Add a set_layout(filename) method to AppMain to reduce this boilerplate code:
        # The 4 lines below should be replaced with just set_layout("test.xml")
        inflator = self.parent.layout_inflator
        assert isinstance(inflator, LayoutInflator)
        layout = inflator.inflate_layout("test.xml", self.w, self.h, self.parent, self)
        super().set_layout(layout)

        layout.get_element_by_id("station_code").set_text(self.get_config_value("station_code"))
        self.listLayout = layout.get_element_by_id("train_list_view")
        self.listLayout.adapter = lambda value, view: self.adapter(value, view)

        train_update = RepeatEvent(lambda: self.start_update_thread() ,
                                   float(self.get_config_value("refresh_rate")), self)
        self.parent.event_scheduler.add_event(train_update)
        self.start_update_thread()

    def adapter(self, value, view):
        view.get_element_by_id("dest").set_text(
            str(value.destination))
        view.get_element_by_id("std").set_text(
            str(value.std))
        view.get_element_by_id("etd").set_text(str(value.etd))

    def start_update_thread(self):
        self.parent.run_on_new_thread(lambda : self.updateTrainData())


    def updateTrainData(self):
        if self.session is None:
            self.initWSDL()
        if self.session is None:
            return
        board = self.session.get_station_board(self.get_config_value("station_code"), rows=25,
                                               include_departures=True,
                                               include_arrivals=False, time_offset=0, time_window=120)
        self.lastKnown = board.train_services
        self.lastUpdateTime = self.getCurrentTime()
        self.listLayout.setValues(self.lastKnown)

    def initWSDL(self):
        try:
            API_URL = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01'
            self.session = Session(API_URL, self.get_config_value("api_key"))
        except Exception as e:
            print(e)
            print("Error connecting to Darwin")

    def getCurrentTime(self):
        return datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
