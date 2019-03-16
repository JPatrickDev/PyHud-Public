import pygame
import pygame.freetype


class FontSystem(object):

    def __init__(self, parent):
        self.fontsDict = {}
        pygame.freetype.init()
        for i in range(32, 640, 32):
            self.fontsDict[str(i)] = pygame.freetype.Font("fonts/" + parent.get_display_config_value("font") + "/1.ttf",
                                                          i)

    def drawLine(self, text, x, y, parentWidth, parentHeight, targetWidth, targetHeight, surface, font_size = -1):
        finalWidth = -1
        finalHeight = -1
        validFonts = []

        if targetWidth > 0:
            finalWidth = parentWidth * targetWidth
        if targetHeight > 0:
            finalHeight = parentHeight * targetHeight

        if finalWidth == -1 and finalHeight == -1:
            finalWidth = parentWidth
            finalHeight = parentHeight

        isCustomWidth = finalWidth == -1
        isCustomHeight = finalHeight == -1

        if isCustomWidth:
            finalWidth = parentWidth
        if isCustomHeight:
            finalHeight = parentHeight

        for key in self.fontsDict:
            font = self.fontsDict[key]
            dim = font.get_rect(text)
            if dim[2] <= finalWidth and dim[3] <= finalHeight:
                validFonts.append(font)
        if isCustomWidth:
            finalWidth = -1
        if isCustomHeight:
            finalHeight = -1
        if validFonts.__len__() == 0:
            validFonts.append(self.fontsDict['32'])
        validFonts = list(reversed(validFonts))

        finalFont = validFonts[0]
       # finalFont = self.fontsDict['32']
        font_data = finalFont.render(text, (255, 255, 255))
        dim = font_data[1]
        text_surface = font_data[0]
        if finalWidth == -1:
            finalWidth = dim[2]
        if finalHeight == -1:
            finalHeight = dim[3]

        finalSurface = pygame.transform.scale(text_surface, (int(finalWidth), int(finalHeight)))
        drawX = x + ((parentWidth / 2) - (finalWidth / 2))
        drawY = y + ((parentHeight / 2) - (finalHeight / 2))

        surface.blit(finalSurface, (drawX, drawY))