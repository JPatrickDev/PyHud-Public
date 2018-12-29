from .Event import *
import time


# A scheduler for apps to use
class EventScheduler(object):
    parent = None
    currentEvents = []

    def __init__(self, parent):
        self.parent = parent

    def add_event(self, e):
        self.currentEvents.append(e)

    def update(self):
        current_time = time.time()
        for e in self.currentEvents:
            assert isinstance(e, Event)
            if current_time >= e.next_run_time:
                e.func()
                if isinstance(e, OneOffEvent):
                    assert isinstance(e, OneOffEvent)
                    self.currentEvents.remove(e)
                elif isinstance(e, RepeatEvent):
                    assert isinstance(e, RepeatEvent)
                    e.onCall()

    def remove_app_events(self,app):
        for currentEvent in self.currentEvents:
            if currentEvent.parent == app:
                self.currentEvents.remove(currentEvent)
