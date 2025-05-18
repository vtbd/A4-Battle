import pygame
import gui
import sys
import constants
import battle


size = width, height = constants.SCREENSIZE
screen = pygame.display.set_mode(size)
pygame.display.set_caption('A4 Battle')
pygame.display.set_icon(pygame.image.load('res/icon.png'))

pygame.font.init()
root = gui.RootObj(*size)
bg = gui.ImageObj(screen, root, 'res/background.png', (0, 0), size=size)


font_big = pygame.font.Font('zcool.ttf', int(round(48*constants.S)))
font_small = pygame.font.Font('zcool.ttf', int(round(32*constants.S)))

game = battle.Game(screen, root, font_big, font_small)

clock = pygame.time.Clock()

game.update()
while 1:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pass
        if event.type == pygame.MOUSEBUTTONUP:
            game.detectclick(event.pos)
            pass
    if game.new == True:
        game = battle.Game(screen, root, font_big, font_small)
        

    bg.draw()
    game.updateanimations()
    game.update()

    clock.tick(30)
    pygame.display.flip()