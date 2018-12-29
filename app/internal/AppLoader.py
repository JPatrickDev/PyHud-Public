from os import listdir
import os
import importlib
import json


class AppLoader(object):
    def load_app_internal(self, moduleName, name):
        module = importlib.import_module(moduleName + ".AppMain")
        class_ = getattr(module, name)
        instance = class_()
        return instance

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

    def load_app_from_info(self, info, parent):
        if info['systemapp'] == "True":
            return self.load_app("systemapps", info['app_name'], {"xPos": 0, "yPos": 0, "width": 1, "height": 1},parent)
        else:
            return self.load_app("apps", info['app_name'], {"xPos": 0, "yPos": 0, "width": 1, "height": 1},parent)

    def load_app(self, folder, name, appMeta, parent):
        try:
            module = folder + "." + name
            name = name
            app = self.load_app_internal(module, name)
            app.set_parent(parent)
            app.set_bounds(appMeta['xPos'] * parent.gridPWidth, appMeta['yPos'] * parent.gridPHeight,
                           appMeta['width'] * parent.gridPWidth, appMeta['height'] * parent.gridPHeight)
            app.isSystemApp = True
            app.init_config()
            return app
        except KeyError:
            return None

    def loadFolder(self, folder):
        return listdir(folder)

