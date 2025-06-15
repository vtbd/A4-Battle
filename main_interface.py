import pygame
import pygame_gui
import constants as c
S = c.S

class MainInterface:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager

        self.S = S
        
        self.scaled_width, self.scaled_height = c.SCREENSIZE
        
        # 界面元素
        self.title_image = None
        self.start_button = None
        self.settings_button = None
        self.choose_button = None
        
        self.load_resources()
        self.create_ui_elements()
    
    def load_resources(self):
        original_image = pygame.image.load('res/title.png').convert_alpha()
        new_width = int(original_image.get_width() * self.S)
        new_height = int(original_image.get_height() * self.S)
        self.title_image = pygame.transform.scale(original_image, (new_width, new_height))
    
    def create_ui_elements(self):
        title_rect = pygame.Rect(0, 0, 
                                600 * self.S, 
                                200 * self.S)
        title_rect.centerx = self.scaled_width // 2
        title_rect.y = 100 * self.S
        
        start_button_rect = pygame.Rect(0, 0, *c.START_BUTTON_SIZE)
        start_button_rect.centerx = c.START_BUTTON_POS[0]
        start_button_rect.y = c.START_BUTTON_POS[1]
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=start_button_rect,
            text='开始游戏',
            manager=self.manager
        )
        
        settings_button_rect = pygame.Rect(0, 0, *c.SETTINGS_BUTTON_SIZE)
        settings_button_rect.centerx = c.SETTINGS_BUTTON_POS[0]
        settings_button_rect.y = c.SETTINGS_BUTTON_POS[1]
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=settings_button_rect,
            text='设置',
            manager=self.manager
        )

        choose_button_rect = pygame.Rect(0, 0, *c.CHOOSE_BUTTON_SIZE)
        choose_button_rect.centerx = c.CHOOSE_BUTTON_POS[0]
        choose_button_rect.y = c.CHOOSE_BUTTON_POS[1]
        self.choose_button = pygame_gui.elements.UIButton(
            relative_rect=choose_button_rect,
            text='选择角色',
            manager=self.manager
        )
    
    def process_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                return "start"
            elif event.ui_element == self.settings_button:
                return "settings"
            elif event.ui_element is self.choose_button:
                return "choose"
        return None
    
    def update(self, time_delta):
        self.manager.update(time_delta)
    
    def draw(self):
        title_rect = self.title_image.get_rect()
        title_rect.centerx = self.scaled_width // 2
        title_rect.y = 100 * self.S
        self.screen.blit(self.title_image, title_rect)
        
        self.manager.draw_ui(self.screen)