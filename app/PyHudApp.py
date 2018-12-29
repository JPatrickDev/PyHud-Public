import json
import random
import shutil
import string
from abc import ABCMeta, abstractmethod

import pygame


class PyHudApp(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.parent = None
        self.layout = None
        self.isSystemApp = False

        self.drawSurface = None

        #Used for debugging
        self.uid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))

    def init_config(self):
        self.config = None
        try:
            with open(self.get_path_to_file_in_app_folder("config.json")) as f:
                data = json.load(f)
                self.config = data
        except FileNotFoundError:
            self.clone_default_config()

    def set_parent(self, parent):
        self.parent = parent

    def set_bounds(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.drawSurface = pygame.Surface((int(w), int(h)), pygame.SRCALPHA, 32)
        self.drawSurface = self.drawSurface.convert_alpha()

    def request_draw(self):
        self.drawSurface.fill((0, 0, 0, 0), (0, 0, self.w, self.h))
        if self.layout is not None:
            self.layout.render(self.drawSurface)
        self.render(self, self.drawSurface)

    @abstractmethod
    def render(self, surface):
        pass

    def update(self, parent):
        if self.layout is not None:
            self.layout.update(self)

    @abstractmethod
    def get_version(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def on_load(self):
        pass

    def clicked(self, x, y, button):
        if self.layout is not None:
            self.layout.clicked(x - self.x, y - self.y, button)

    def dragged(self, x, y, button, delta):
        if self.layout is not None:
            self.layout.dragged(x - self.x, y - self.y, button, delta)

    def set_layout(self, layout):
        self.layout = layout
        self.invalidate_layout()

    def is_invalidated(self):
        if self.layout is not None:
            return self.layout.is_invalidated()
        else:
            return False

    def dispose(self):
        if self.layout is not None:
            self.layout.dispose()
        self.parent.event_scheduler.remove_app_events(self)

    def clone_default_config(self):
        try:
            with open(self.get_path_to_file_in_app_folder("default_config.json")) as f:
                shutil.copy(self.get_path_to_file_in_app_folder("default_config.json"),
                            self.get_path_to_file_in_app_folder("config.json"))
                self.init_config(self)
        except FileNotFoundError:
            pass

    def get_config_value(self, key):
        if key in self.config:
            return self.config[key]
        else:
            return ""

    def get_all_invalidated_elements(self):
        if self.layout is None:
            return []
        else:
            return self.layout.get_all_invalidated_elements()

    def invalidate_layout(self):
        if self.layout is not None:
            self.layout.invalidate_children()

    def get_path_to_file_in_app_folder(self, file):
        if self.isSystemApp:
            return "systemapps/" + self.get_name() + "/" + str(file)
        else:
            return "apps/" + self.get_name() + "/" + str(file)

    def get_path_to_resource(self, file):
        if "system/resources" in file:
            return file
        else:
            return self.get_path_to_file_in_app_folder(file)

    def get_app_icon_path(self):
        return "system/resources/images/default_app_icon.png"
