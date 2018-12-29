import json
from threading import Thread

import pygame
import sys

from app.internal.AppLoader import AppLoader
from ui.dialogs.AppDialog import AppDialog
from ui.dialogs.Dialog import Dialog
from ui.dialogs.LayoutDialog import LayoutDialog
from ui.layout.LayoutInflator import LayoutInflator
from .util.EventScheduler import *


class PyHud(object):

    VERSION = "1.0"

    def __init__(self):
        self.screen = None
        self.running = False
        self.event_scheduler = None
        self.width = 800
        self.height = 600
        self.firstRun = True
        self.firstDialogRun = True
        self.mouseDown = False
        self.mouseDownTime = -1
        self.mouseDragging = False
        self.draggingApp = None
        self.previousMousePos = (-1, -1)
        self.page = "home"
        self.dialog = None

        self.gridTWidth = 10
        self.gridTHeight = 10
        self.gridPWidth = 0
        self.gridPHeight = 0

        self.layout_inflator = LayoutInflator()
        self.appLoader = AppLoader()

        self.runningApps = []

    def start(self):
        try:
            with open("system/display_config.json") as f:
                print("Config File Found")
                data = json.load(f)
                self.width = int(data['width'])
                self.height = int(data['height'])
                self.fullScreen = data['fullscreen']
        except FileNotFoundError:
            print("No config file found")
            sys.exit()

        self.gridPWidth = self.width / self.gridTWidth
        self.gridPHeight = self.height / self.gridTHeight
        self.background = pygame.image.load("background.jpg")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        pygame.init()
        self.event_scheduler = EventScheduler(self)
        size = self.width, self.height
        if self.fullScreen == "False":
            self.screen = pygame.display.set_mode(size)
        else:
            self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        apps = self.appLoader.load_apps(self, self.page)
        self.runningApps = apps
        for a in self.runningApps:
            a.on_load()
        print(apps)
        self.run()

    def run(self):
        self.running = True
        last_time = time.time()
        last_update = time.time()
        last_render = time.time()
        counter = 0
        fps = 60
        ups = 0

        fpsWait = 60

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouseDown = False
                    self.mouseDragging = False
                    self.draggingApp = None
                    diff = time.time() - self.mouseDownTime
                    if diff <= 0.5:
                        pos = pygame.mouse.get_pos()
                        if self.dialog is None:
                            for app in self.runningApps:
                                if app.x < pos[0] < app.x + app.w:
                                    if app.y < pos[1] < app.y + app.h:
                                        app.clicked(pos[0], pos[1], 0)
                        else:
                            found = False
                            if self.dialog.display_x < pos[0] < self.dialog.display_x + self.dialog.display_width:
                                if self.dialog.display_y < pos[1] < self.dialog.display_y + self.dialog.display_width:
                                    self.dialog.clicked(pos[0], pos[1], 0)
                                    found = True
                            if not found:
                                self.close_dialog(-1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseDown = True
                    self.mouseDownTime = time.time()
                if event.type == pygame.MOUSEMOTION:
                    if self.mouseDown:
                        self.mouseDragging = True
                        pos = pygame.mouse.get_pos()
                        if self.previousMousePos[0] is not -1:
                            diffX = pos[0] - self.previousMousePos[0]
                            diffY = pos[1] - self.previousMousePos[1]
                            # TODO
                            if self.dialog is None:
                                if self.draggingApp is None or True:
                                    for app in self.runningApps:
                                        if app.x < pos[0] < app.x + app.w:
                                            if app.y < pos[1] < app.y + app.h:
                                                app.dragged(pos[0], pos[1], 0, (diffX, diffY))
                                                self.draggingApp = app
                                else:
                                    self.draggingApp.dragged(pos[0], pos[1], 0, (diffX, diffY))
                            else:
                                if self.dialog.display_x < pos[0] < self.dialog.display_x + self.dialog.display_width:
                                    if self.dialog.display_y < pos[
                                        1] < self.dialog.display_y + self.dialog.display_width:
                                        self.dialog.dragged(pos[0], pos[1], 0, (diffX, diffY))
                        self.previousMousePos = pos

            currentTime = time.time()
            if currentTime - last_update >= (1 / 30):
                self.update()
                last_update = time.time()
                ups += 1

            # if time.time() - last_render >= (1 / fpsWait):
            self.render()
            last_render = time.time()
            fps += 1

            counter += (time.time() - last_time)

            if counter >= 1:
                if fps > 60:
                    fpsWait -= 1
                elif fps < 60:
                    fpsWait += 1
                print("FPS:", fps, "UPS:", ups)
                fps = 0
                ups = 0
                counter = 0

            last_time = time.time()

    def update(self):
        self.event_scheduler.update()
        for app in self.runningApps:
            app.update(self)
        if self.dialog is not None:
            self.dialog.update()

    x = 0

    def render(self):
        if self.firstRun:
            print("First run")
            self.firstRun = False
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, self.background.get_rect())
            pygame.display.flip()

        toUpdate = []

        if self.dialog is None:
            for app in self.runningApps:
                if app.is_invalidated():
                    elements = app.get_all_invalidated_elements()
                    for element in elements:
                        element.invalidated = False
                        elementX = app.x + element.x
                        elementY = app.y + element.y
                        element.render()
                        self.screen.blit(self.background, (elementX, elementY),
                                         (elementX, elementY, element.w, element.h))
                        self.screen.blit(element.drawSurface, (elementX, elementY))
                        toUpdate.append((elementX, elementY, element.w, element.h))

        if self.dialog is not None:
            dialogX = self.width / 2 - self.dialog.display_width / 2
            dialogY = self.height / 2 - self.dialog.display_height / 2
            if self.firstDialogRun:
                pygame.draw.rect(self.screen, (40, 40, 40, 10),
                                 (dialogX, dialogY, self.dialog.display_width, self.dialog.display_height))
            if self.dialog.is_invalidated():
                elements = self.dialog.get_all_invalidated_elements()
                for element in elements:
                    element.invalidated = False
                    elementX = dialogX + element.x
                    elementY = dialogY + element.y
                    element.render()
                    pygame.draw.rect(self.screen, (40, 40, 40, 10), (elementX, elementY, element.w, element.h))
                    self.screen.blit(element.drawSurface, (elementX, elementY))
                    toUpdate.append((elementX, elementY, element.w, element.h))

            if self.firstDialogRun:
                pygame.display.flip()
                self.firstDialogRun = False
            else:
                pygame.display.update(toUpdate)

        pygame.display.update(toUpdate)

    def changePage(self, name):
        self.page = name
        for app in self.runningApps:
            app.dispose()
        apps = self.appLoader.load_apps(self, self.page)
        self.runningApps = apps
        for a in self.runningApps:
            a.on_load()
        self.firstRun = True

    def run_on_new_thread(self, function):
        Thread(target=function).start()

    def show_dialog(self, layout_file, parent_app, on_load, on_close):
        dialog = LayoutDialog(layout_file, on_load, on_close, parent_app)
        display_width = self.width - ((self.width / 10) * 2)
        display_height = self.height - ((self.height / 10) * 2)
        dialogX = self.width / 2 - display_width / 2
        dialogY = self.height / 2 - display_height / 2
        dialog.load(dialogX, dialogY, display_width, display_height)
        self.dialog = dialog

    def show_app_dialog(self,app,on_load,on_close):
        app.set_parent(self)
        dialog = AppDialog(on_load, on_close, app)
        display_width = self.width - ((self.width / 30) * 2)
        display_height = self.height - ((self.height / 30) * 2)
        dialogX = self.width / 2 - display_width / 2
        dialogY = self.height / 2 - display_height / 2
        dialog.load(dialogX, dialogY, display_width, display_height)
        self.dialog = dialog

    def get_system_resource(self, file):
        return "system/resources/" + file

    def get_app_resource(self, app_data, file):
        app_name = app_data['app_name']
        is_system_app = app_data['systemapp'] == "True"
        if is_system_app:
            return "systemapps/" + app_name + "/resources/" + file
        else:
            return "apps/" + app_name + "/resources/" + file

    def close_dialog(self, result):
        self.dialog = None
        for app in self.runningApps:
            app.invalidate_layout()
        self.firstRun = True
        self.firstDialogRun = True
