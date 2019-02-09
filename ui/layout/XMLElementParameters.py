class XMLElementParameters:
    def __init__(self, xml):
        if xml is not None:
            self.xml = xml
            self.attributes = xml.attrib
            self.text = xml.text

    def set_dict(self,dict):
        self.attributes = dict
        self.text = ""

    def __init(self,xml , mode):
        self.attributes = xml
        self.text = ""
    def has_parameter(self, key):
        return key in self.attributes

    def get_parameter(self, key):
        return self.get_parameter(key, None)

    def get_parameter(self, key, default):
        if key in self.attributes:
            return self.attributes[key]
        else:
            return default

    def insert_parameter(self, key, value):
        self.attributes[key] = value
