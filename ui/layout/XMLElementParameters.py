class XMLElementParameters:
    def __init__(self, xml):
        self.xml = xml
        self.attributes = xml.attrib
        self.text = xml.text

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
