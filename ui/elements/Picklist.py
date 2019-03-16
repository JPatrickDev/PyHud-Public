from ui.elements.TextBox import TextBox
from ui.layout import XMLElementParameters
from .UIElement import UIElement
import pygame
from ast import literal_eval


class Picklist(TextBox):

    def __init__(self, x, y, w, h, id, text, textWidth, textHeight, layout_file,backgroundColor, parent):
        super().__init__(x, y, w, h, id, text , textWidth, textHeight, backgroundColor, False, -1, parent)
        self.values = []
        self.selected = ""
        self.listener = None

    def clicked(self, x, y, button):
        print("Clicked")
        self.parent.parent.show_picklist_dialog(
            "system/resources/layouts/picklist_dialog.xml", self.parent, lambda x: self.initDialog(x), lambda: print("Closed"))

        return super().clicked(x, y, button)

    @staticmethod
    def from_XML_element_parameters(params, parent, bounds):
        assert isinstance(params, XMLElementParameters.XMLElementParameters)
        id = params.get_parameter("id",None)
        if id is None:
            # TODO: Logging system
            return None
        text = params.text
        if text is None:
            text = ""
        # TODO: Gracefully handle params that exist, but are in the wrong format
        text_width = float(params.get_parameter("text_width", -1))
        text_height = float(params.get_parameter("text_height", -1))
        background_color = params.get_parameter("background_color", None)
        if background_color is not None:
            background_color = literal_eval(background_color)
        return Picklist(bounds[0], bounds[1], bounds[2], bounds[3], id, text, text_width, text_height, "test",background_color,
                       parent)

    def initDialog(self, x):
        self.current_dialog = x
        x.get_element_by_id("picklist_list_view").adapter = lambda value, view : self.default_adapter(value,view)
        x.get_element_by_id("picklist_list_view").setValues(self.values)
        x.get_element_by_id("picklist_list_view").item_click_listener = lambda item: self.set_selected(item)

    def default_adapter(self,value,view):
        view.get_element_by_id("picklist_list_item_text").set_text(value)

    def set_values(self, values):
        self.values = values

    def set_selected(self,item):
        print("Selected: " + item)
        self.selected = item
        if self.listener is not None:
            self.listener(item)
        if self.parent.parent.dialog.layout == self.current_dialog:
            self.parent.parent.close_dialog(0)
