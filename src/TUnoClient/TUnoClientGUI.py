import pygame
import pygame_gui
import time
from TUnoClientSprites import *
from TUnoClientSocket import *

SCREEN_WIDTH = 16*75
SCREEN_HEIGHT = 9*75


def main():
    
    pygame.init()
    running = True

    server_conn = TUnoClient()

    clock = pygame.time.Clock()

    main_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    manager = pygame_gui.UIManager(main_window.get_rect().size)

    main_window2 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    manager2 = pygame_gui.UIManager(main_window.get_rect().size)
    pygame.display.set_caption("TUno")

    # fc = pygame.Surface(main_window.get_rect().size)
    # fc.fill((255,0,0))
    
    # # fc = pygame_gui.elements.UIPanel(
    # #     relative_rect = main_window.get_rect(),
    # #     manager = manager,
    # #     starting_layer_height = 0,
    # #     visible=True
    # # )
    # first_button_rect = pygame.Rect(fc.get_rect().width / 2 - 250,500, 500,40)
    
    # first_button = pygame_gui.elements.UIButton(
    #     #relative_rect = pygame.Rect((main_wind|ow.get_rect().centerx - (first_button_size[0] / 2) ,main_window.get_rect().centery - (first_button_size[1] / 2)),first_button_size),
    #     relative_rect = first_button_rect,
    #     manager = manager,
    #     container= fc.get_rect(),
    #     text = "Join"
    # )
    
    # first_textentry = pygame_gui.elements.UITextEntryLine(        
    #     relative_rect= pygame.Rect(first_button_rect.move(0,-100)),        
    #     manager = manager,
    #     container= fc,
    # )
    # first_textentry.set_text("Please enter a nickname")

    pygame_gui.windows.UIColourPickerDialog(
        rect = pygame.Rect(100,100,400,400),
        manager = manager,
        initial_colour= pygame.Color(0,0,0),
        window_title= "Color picker",
        visible=True
    )
    

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                server_conn.quit_game()

            # if event.type == pygame.USEREVENT:
            #     if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            #         print("asd")
            #         if event.ui_element == first_button:
            #             if not server_conn.connected:
            #                 server_conn.connectToServer()

            #             if server_conn.connected:
            #                 server_conn.send_message(firstCommand(first_textentry.get_text()))
            #                 data = server_conn.serverMessages.get()
            #                 if data == "Added gamer":
            #                     fc.kill()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 1:
            #         if pygame.Rect.collidepoint(first_textentry.get_relative_rect(), event.pos):
            #             first_textentry.set_text("")
            #         if pygame.Rect.collidepoint(fc.get_relative_rect(), event.pos):
            #             #first_textentry.set_text("Please enter a nickname")
            #             print("caca")



            manager.process_events(event)
        
        main_window.fill((41, 49, 138))
        #main_form.fill((29, 34, 89))
        
        pygame.draw.line(main_window, (0,0,0), main_window.get_rect().midtop, main_window.get_rect().midbottom, 1)
        pygame.draw.line(main_window, (0,0,0), main_window.get_rect().midleft, main_window.get_rect().midright, 1)

        manager.update(time_delta)
        manager.draw_ui(main_window)
        manager2.update(time_delta)
        manager2.draw_ui(main_window2)
        pygame.display.update()

    pygame.quit()
 

# class first_container(pygame_gui.elements.UIPanel):
#     def init(self, rect, manager, start_height):
#         super(first_container, self).__init__(relative_rect = rect,starting_layer_height = start_height, manager= manager,
#         )
   
#     def create_elements(self, manager):
#         first_button_rect = pygame.Rect(100,100,500,40)

#         self.first_button = pygame_gui.elements.UIButton(
#             #relative_rect = pygame.Rect((main_wind|ow.get_rect().centerx - (first_button_size[0] / 2) ,main_window.get_rect().centery - (first_button_size[1] / 2)),first_button_size),
#             relative_rect = first_button_rect,
#             manager = manager,
#             container= self,
#             text = "Join"
#         )
        
#         self.first_textentry = pygame_gui.elements.UITextEntryLine(
#             relative_rect= pygame.Rect(first_button_rect.move(0,-100)),        
#             manager = manager,
#             container= self
#         )
#         self.first_textentry.set_text("Please enter a nickname") 

#     def process_event(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             print("Donde esta el rectangulo: ",self.first_textentry.get_relative_rect())
#             print("Donde clickee: ", event.pos)
#             if self.first_textentry.get_relative_rect().collidepoint(event.pos):
#                 print("caca")


if __name__ == "__main__":
    main()