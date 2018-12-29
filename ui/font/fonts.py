import pygame
import pygame.freetype


class Fonts(object):
    fontsDict = {}

    def __init__(self):
        pygame.freetype.init()
        for i in range(8, 240, 8):
            self.fontsDict[str(i)] = pygame.freetype.Font("AnonymousPro-Regular.ttf", i)

    def drawLine(self, text, x, y, parentWidth, parentHeight, targetWidth, targetHeight, surface):
        validFonts = []
        isCustomWidth = targetWidth <= 0
        isCustomHeight = targetHeight <= 0
        if targetWidth <= 0:
            targetWidth = parentWidth
        if targetHeight <= 0:
            targetHeight = parentHeight
        for key in self.fontsDict:
            k = self.fontsDict[key]
            size = k.get_rect(text)
            wT = size[2]
            hT = size[3]
            if (wT <= targetWidth and hT <= targetHeight):
                validFonts.append(key)
        validFonts = list(reversed(validFonts))
        font = validFonts[0]
        font = self.fontsDict[font]
        textData = font.render(text, (255, 255, 255))
        rect = textData[1]
        textSurface = textData[0]
        if isCustomWidth:
            targetWidth = rect[2]
        if isCustomHeight:
            targetHeight = rect[3]
        textSurface = pygame.transform.scale(textSurface, (int(targetWidth), int(targetHeight)))
        drawX = x + ((parentWidth / 2) - (targetWidth / 2))
        drawY = y + ((parentHeight / 2) - (targetHeight / 2))
        surface.blit(textSurface, (drawX, drawY))
