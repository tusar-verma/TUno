import pygame
import pygame_gui

from src.TUnoClient.TUnoClientFunctions import *

class Card(pygame.sprite.Sprite):

    def __init__(self):
        super(Card, self).__init__()

    def update(self):
        pass

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        
    def update(self):
        pass


class First_container(pygame_gui.elements.UIPanel):
    ref_server_conn = None
    ref_manager = None

    def __init__(self, rect, manager, start_height, server_con):
        super(First_container, self).__init__(
            relative_rect = rect,
            manager = manager,
            starting_layer_height = start_height,)
        self.create_elements(manager)
        self.ref_manager = manager
        self.ref_server_conn = server_con
            
   
    def create_elements(self, manager):
        first_button_rect = pygame.Rect(self.get_relative_rect().width / 2 - 250,500,500,40)

        self.first_button = pygame_gui.elements.UIButton(
            #relative_rect = pygame.Rect((main_wind|ow.get_rect().centerx - (first_button_size[0] / 2) ,main_window.get_rect().centery - (first_button_size[1] / 2)),first_button_size),
            relative_rect = first_button_rect,
            manager = manager,
            container= self,
            text = "Join"
        )
        self.first_button.disable()
        
        self.first_textentry = pygame_gui.elements.UITextEntryLine(
            relative_rect= pygame.Rect(first_button_rect.move(0,-100)),        
            manager = manager,
            container= self
        )
        self.first_textentry.set_text("Please enter a nickname") 

        self.first_image = pygame_gui.elements.UIImage(
            relative_rect = pygame.Rect(self.get_relative_rect().width / 2 - 250, 100, 500, 250),
            image_surface = pygame.image.load("C:\\Users\\Programador\\Documents\\TUno\\bunny.jpg"),
            manager = manager,
            container = self
        )

    def create_message_pop_up(self, message, title = "TUno"):                             
        pygame_gui.windows.ui_message_window.UIMessageWindow(
            rect = pygame.Rect(self.get_relative_rect().width / 2 - 125, self.get_relative_rect().height / 2 - 80,250,160),
            manager = self.ref_manager,
            html_message = message,
            window_title= title
        )

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.first_textentry.get_relative_rect().collidepoint(event.pos):
                    self.first_textentry.set_text("")
                    self.first_button.enable()
                    return True 
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.first_button:
                    # Hay un bug que al tocar el boton se detecta como que se hicieron 2 clicks en el y hace que
                    # se procesen el evento 2 veces, resultando en 2 pop ups (por ejemplo).
                    # Para evitarlo se checkea que si en el ultimo ciclo se presiono el boton, desactivarlo. Asi
                    # cuando se vuelve a procesar dicho evento, sale como que el boton no fue presionado porque estaba
                    # deshabilitado
                    if self.first_button.check_pressed():
                        self.first_button.disable()
                        if self.first_textentry.get_text().strip() == "":                            
                            self.create_message_pop_up("You cant use this nickname")
                            return True

                        if not self.ref_server_conn.connected:
                            self.ref_server_conn.connectToServer()
                            
                        if self.ref_server_conn.connected:
                            self.ref_server_conn.send_message(firstCommand(self.first_textentry.get_text().strip()))
                            data = self.ref_server_conn.serverMessages.get()
                            if data == "Added gamer":
                                self.kill()
                            else:
                                self.create_message_pop_up("You cant use this nickname")
                        else:       
                            self.create_message_pop_up("Couldn't connect to server")
                        self.first_button.enable()
                        return True                     
                
