import pygame
import pygame_gui
import constants as c
S = c.S

class GameInterface:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager

        self.S = S
        
        self.scaled_width, self.scaled_height = c.SCREENSIZE
        
        self.back_button = None
        self.stack_button = None
        
        self.create_ui_elements()
    
    def create_ui_elements(self):
        title_rect = pygame.Rect(0, 0, 
                                600 * self.S, 
                                200 * self.S)
        title_rect.centerx = self.scaled_width // 2
        title_rect.y = 100 * self.S
        
        #back_button_image = pygame.image.load("res/button_in_game_back.png").convert_alpha()
        back_button_rect = pygame.Rect(0, 0, *c.BACK_BUTTON_SIZE)
        back_button_rect.topleft = c.BACK_BUTTON_POS
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=back_button_rect,
            text = "返", 
            manager=self.manager, 
            object_id="button_in_game_menu"
        )
        
    
    def process_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_button:
                return "back"
        return None
    
    def update(self, time_delta):
        self.manager.update(time_delta)
    
    def draw(self):
        self.manager.draw_ui(self.screen)