import time
import xml.etree.ElementTree as tree
from ast import literal_eval

from ui.elements.SpacerView import SpacerView
from ui.elements.GridView import GridView
from ui.elements.ImageView import ImageView
from ui.elements.ListView import ListView
from ui.elements.Picklist import Picklist
from ui.elements.TextBox import TextBox
from ui.layout.UILayout import UILayout
from ui.layout.XMLElementParameters import XMLElementParameters


class LayoutInflator(object):
    def inflate_layout(self, file, width, height, parent, app):
        layout = UILayout()
        xml = None
        if "system/resources/layouts" in file:
            xml = tree.parse(file)
        else:
            xml = tree.parse(app.get_path_to_file_in_app_folder("layout/" + file))
        root = xml.getroot()
        rootDict = root.attrib
        gridW = int(rootDict['gridW'])
        gridH = int(rootDict['gridH'])
        tileWidth = width / gridW
        tileHeight = height / gridH

        for child in root:
            childDict = child.attrib
            x = int(childDict['x']) * tileWidth
            y = int(childDict['y']) * tileHeight
            w = int(childDict['w']) * tileWidth
            h = int(childDict['h']) * tileHeight

            params = XMLElementParameters(child)

            element = None
            element_id = params.get_parameter("id", None)

            if child.tag == "TextBox":
                element = TextBox.from_XML_element_parameters(params, app, (x, y, w, h))
            if child.tag == "ListView":
                params.insert_parameter("num_cols", 1)
                element = GridView.from_XML_element_parameters(params, app, (x, y, w, h))
            if child.tag == "GridView":
                element = GridView.from_XML_element_parameters(params, app, (x, y, w, h))
            if child.tag == "ImageView":
                element = ImageView.from_XML_element_parameters(params, app, (x, y, w, h))
            if child.tag == "Picklist":
                element = Picklist.from_XML_element_parameters(params, app, (x, y, w, h))
            if child.tag == "SpacerView":
                element = SpacerView.from_XML_element_parameters(params, app, (x, y, w, h))
            if element is not None:
                layout.elements[element_id] = element
        return layout
