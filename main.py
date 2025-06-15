import pygame
import pygame_gui
import main_interface
import in_game_interface
import gui
import os
import constants
import battle

pygame.mixer.init()


size = width, height = constants.SCREENSIZE
screen = pygame.display.set_mode(size)
pygame.display.set_caption('A4 Battle')
pygame.display.set_icon(pygame.image.load('res/icon.png'))

pygame.font.init()
root = gui.RootObj(*size)
bg = gui.ImageObj(screen, root, 'res/background.png', (0, 0), size=size)


font_big = pygame.font.Font('res/zcool.ttf', int(round(48*constants.S)))
font_small = pygame.font.Font('res/zcool.ttf', int(round(32*constants.S)))


clock = pygame.time.Clock()

# pygame_gui elements
manager_mainface = pygame_gui.UIManager(size, theme_path=constants.THEME)
main_interface_obj = main_interface.MainInterface(screen, manager_mainface)
manager_in_game = pygame_gui.UIManager(size, theme_path=constants.THEME)
in_game_interface_obj = in_game_interface.GameInterface(screen, manager_in_game)

interface = 1
stack = ["base"]
running = True

def switch_interface(intf):
    global interface
    global stack
    interface = intf
    stack = ["base"]


def newgame():
    global game
    game = battle.Game(screen, root, font_big, font_small)
    return game

def main_interface_update():
    time_delta = clock.tick(30) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
        
        manager_mainface.process_events(event)
        result = main_interface_obj.process_events(event)
        if result == "start":
            switch_interface(2)
            newgame()
            return
        elif result == "settings":
            if os.path.exists("settings.exe"):
                os.system("start settings.exe")
            elif os.path.exists("settings.py"):
                os.system("python settings.py")
        elif result == "choose":
            if os.path.exists("choose.exe"):
                os.system("start choose.exe")
            elif os.path.exists("choose.py"):
                os.system("python choose.py")
            
    bg.draw()
    manager_mainface.update(time_delta)
    main_interface_obj.update(time_delta)
    main_interface_obj.draw()

def in_game_update():
    time_delta = clock.tick(30) / 1000.0
    events = pygame.event.get()
    global game
    for event in events:
        if event.type == pygame.QUIT:
            global running
            running = False
        if event.type == pygame.MOUSEMOTION:
            pass
        if event.type == pygame.MOUSEBUTTONUP:
            game.detectclick(event.pos)
            pass
        
        manager_in_game.process_events(event)
        result = in_game_interface_obj.process_events(event)
        if result == "back":
            switch_interface(1)
            del game
            return
    if game.new == True:
        newgame()
    

    bg.draw()
    game.updateanimations()
    game.update()
    manager_in_game.update(time_delta)
    in_game_interface_obj.update(time_delta)
    in_game_interface_obj.draw()


while running:
    match interface:
        case 1:
            main_interface_update()
        case 2:
            in_game_update()
    pygame.display.flip()
pygame.quit()