import datetime

from app.PyHudApp import PyHudApp
from ui.layout.LayoutInflator import LayoutInflator
from system.util.EventScheduler import EventScheduler
from system.util.Event import *
from nrewebservices.ldbws import Session




class TrainApp(PyHudApp):
    lastKnown = []
    INSTANCE = None

    def __init__(self, headless):
        super().__init__(headless)
        self.lastUpdateTime = ""
        self.session = None
        TrainApp.INSTANCE = self

    def render(self, surface):
        pass

    def get_version(self):
        return "1.0"

    def get_name(self):
        return "TrainApp"

    def on_init(self):
        super().on_init()

        train_update = RepeatEvent(lambda: self.updateTrainData(),
                                   float(self.get_config_value("refresh_rate")), self)
        self.parent.event_scheduler.add_event(train_update)
        self.updateTrainData()

    def on_load(self):

        layout = self.set_layout_file("test.xml")

        layout.get_element_by_id("station_code").set_text(self.get_config_value("station_code"))
        self.listLayout = layout.get_element_by_id("train_list_view")
        self.listLayout.adapter = lambda value, view: self.adapter(value, view)

        self.updateTrainData()

    def adapter(self, value, view):
        view.get_element_by_id("dest").set_text(
            str(value.destination))
        view.get_element_by_id("std").set_text(
            str(value.std))
        view.get_element_by_id("etd").set_text(str(value.etd))

    def updateTrainData(self):
        if self.session is None:
            self.initWSDL()
        if self.session is None:
            return

        board = self.session.get_station_board(self.get_config_value("station_code"), rows=25,
                                               include_departures=True,
                                               include_arrivals=False, time_offset=0, time_window=120)
        TrainApp.lastKnown = board.train_services
        self.lastUpdateTime = self.getCurrentTime()
        if self.layout is None:
            return
        self.listLayout.setValues(TrainApp.lastKnown)

    def initWSDL(self):
        try:
            API_URL = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01'
            self.session = Session(API_URL, self.get_config_value("api_key"))
        except Exception as e:
            print(e)
            print("Error connecting to Darwin")

    def getCurrentTime(self):
        return datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")

    @staticmethod
    def toMinsSinceMidnight(input):
        split = input.split(":")
        hrs = int(split[0])
        mins = int(split[1])
        return hrs * 60 + mins

    def get_icons_headless(self):
        average_delay = 0
        for train in self.lastKnown:
            if train.etd == "On time":
                average_delay -= 5
            elif train.etd== "Delayed":
                average_delay += 15
            elif train.etd == "Cancelled":
                average_delay += 30
            else:
                expt = self.toMinsSinceMidnight(train.std)
                act = self.toMinsSinceMidnight(train.etd)
                average_delay += (act - expt)
        if average_delay <= 15:
            return [{"image": self.INSTANCE.get_path_to_resource("resources/icon_ok.png")}]
        if 10 < average_delay <= 60:
            return [{"image": self.INSTANCE.get_path_to_resource("resources/icon_average.png")}]
        else:
            return [{"image":self.INSTANCE.get_path_to_resource("resources/icon_bad.png")}]