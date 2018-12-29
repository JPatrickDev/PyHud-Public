from abc import abstractmethod
import time


class Event:
    func = None
    next_run_time = None

    def __init__(self, func, next_run_time, parent):
        self.func = func
        self.next_run_time = next_run_time
        self.parent = parent

    @abstractmethod
    def onCall(self):
        pass


class OneOffEvent(Event):
    def __init__(self, func, delay, parent):
        super().__init__(func, (time.time() + delay), parent)

    def onCall(self):
        pass


class RepeatEvent(Event):
    freq = None

    def __init__(self, func, freq, parent):
        super().__init__(func, (time.time() + freq), parent)
        self.freq = freq

    def onCall(self):
        self.next_run_time = time.time() + self.freq
