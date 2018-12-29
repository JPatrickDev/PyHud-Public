from ui.elements.GridView import GridView

class ListView(GridView):

    def __init__(self, x, y, w, h, id, layout_file, parent):
        super().__init__(x, y, w, h, id, layout_file, 1, parent)

