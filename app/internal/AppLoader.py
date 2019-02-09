from os import listdir
import os
import importlib
import json


class AppLoader(object):
    def load_app_internal(self, moduleName, name, headless):
        module = importlib.import_module(moduleName + ".AppMain")
        class_ = getattr(module, name)
        instance = class_(headless)
        return instance

    def load_app_static(self, moduleName, name):
        module = importlib.import_module(moduleName + ".AppMain")
        class_ = getattr(module, name)
        return class_

    def load_apps(self, parent, name):
        # s   assert isinstance(parent,PyHud)
        json_data = open("app/internal/appLayout.json").read()

        data = json.loads(json_data)
        data = data[name]
        apps = self.loadFolder("apps")
        systemapps = self.loadFolder("systemapps")
        finalApps = []

        for a in apps:
            if os.path.isdir(os.path.join("apps/", a)) and not a.startswith("__") and not a.startswith("."):
                if a in data:
                    app = self.load_app("apps", a, data[a], parent)
                    if app is not None:
                        finalApps.append(app)
        for a in systemapps:
            if os.path.isdir(os.path.join("systemapps/", a)) and not a.startswith("__") and not a.startswith("."):
                if a in data:
                    app = self.load_app("systemapps", a, data[a], parent)
                    if app is not None:
                        finalApps.append(app)
        return finalApps

    def get_app_info(self):
        # s   assert isinstance(parent,PyHud)
        apps = self.loadFolder("apps")
        systemapps = self.loadFolder("systemapps")
        finalApps = []

        for a in apps:
            if os.path.isdir(os.path.join("apps/", a)) and not a.startswith("__") and not a.startswith("."):
                json_data = json.loads(open(os.path.join("apps/", a + "/app.json")).read())
                json_data['systemapp'] = "False"
                finalApps.append(json_data)
        for a in systemapps:
            if os.path.isdir(os.path.join("systemapps/", a)) and not a.startswith("__") and not a.startswith("."):
                json_data = json.loads(open(os.path.join("systemapps/", a + "/app.json")).read())
                json_data['systemapp'] = "True"
                finalApps.append(json_data)
        return finalApps

    def get_app_info_from_name(self, app_name):
        for app in self.get_app_info():
            if app['app_name'] == app_name:
                return app
        return None

    def load_app_from_info(self, info, parent, headless=False):
        folder = ""
        if info['systemapp'] == "True":
            folder = "systemapps"
        else:
            folder = "apps"
        if headless:
            return self.load_headless_app(folder, info['app_name'], parent)
        else:
            return self.load_app(folder, info['app_name'], {"xPos": 0, "yPos": 0, "width": 1, "height": 1}, parent)

    def load_app(self, folder, name, appMeta, parent):
        try:
            module = folder + "." + name
            name = name
            app = self.load_app_internal(module, name, False)
            app.set_parent(parent)
            app.set_bounds(appMeta['xPos'] * parent.gridPWidth, appMeta['yPos'] * parent.gridPHeight,
                           appMeta['width'] * parent.gridPWidth, appMeta['height'] * parent.gridPHeight)
            app.isSystemApp = folder == "systemapps"
            app.init_config()
            return app
        except KeyError:
            return None

    def load_headless_app(self, folder, name, parent):
        try:
            module = folder + "." + name
            name = name
            app = self.load_app_internal(module, name, True)
            app.set_parent(parent)
            app.isSystemApp = folder == "systemapps"
            app.init_config()
            return app
        except KeyError:
            return None

    def load_headless_apps(self, parent):
        all_apps = self.get_app_info()

        toLoad = []
        for app in all_apps:
            if "requires_headless" in app:
                if app['requires_headless'] == "True":
                    toLoad.append(app)

        finalApps = []
        for app in toLoad:
            app = self.load_app_from_info(app,parent,True)
            finalApps.append(app)
        return finalApps

    def is_headless(self, app_info):
        if "requires_headless" in app_info:
            if app_info['requires_headless'] == "True":
                return True
        return False

    def get_all_icons(self, parent):
        all = []
        all_apps = self.get_app_info()  #
        for app in all_apps:
            folder = "apps"
            if app['systemapp'] == "True":
                folder = "systemapps"

            module = folder + "." + app['app_name']
            icons = []
            if self.is_headless(app):
                icons = parent.get_headless_instance(app['app_name']).get_icons_headless()
            else:
                static = self.load_app_static(module, app['app_name'])
                icons = static.get_icons()
            all.append(icons)
        flattened = [item for sublist in all for item in sublist]
        return flattened

    def loadFolder(self, folder):
        return listdir(folder)
