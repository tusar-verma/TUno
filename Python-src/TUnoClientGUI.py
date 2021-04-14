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
    pygame.display.set_caption("TUno")

    first_container = pygame_gui.elements.UIPanel(
        relative_rect = main_window.get_rect(),
        manager = manager,
        starting_layer_height = 0,
        visible=True,
        anchors={
            "left":"left",
            "right": "right",
            "top": "top",
            "bottom": "bottom"
        }
    )
    first_button_rect = pygame.Rect(0,0,500,40)
    first_button_rect.bottomleft = (338,-100)

    first_button = pygame_gui.elements.UIButton(
        #relative_rect = pygame.Rect((main_wind|ow.get_rect().centerx - (first_button_size[0] / 2) ,main_window.get_rect().centery - (first_button_size[1] / 2)),first_button_size),
        relative_rect = first_button_rect,
        manager = manager,
        container= first_container,
        text = "Join",
        anchors={
            "left":"left",
            "right": "left",
            "top": "bottom",
            "bottom": "bottom"
        }
    )

    first_textentry = pygame_gui.elements.UITextEntryLine(
        relative_rect= pygame.Rect(first_button_rect.move(0,-100)),        
        manager = manager,
        container= first_container,
        anchors={
            "left":"left",
            "right": "left",
            "top": "bottom",
            "bottom": "bottom"
        }
    )
    first_textentry.set_text("Please enter a nickname") 
    

    while running:

        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                server_conn.quit_game()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == first_button:
                        if not server_conn.connected:
                            server_conn.connectToServer()

                        if server_conn.connected:
                            server_conn.send_message(firstCommand(first_textentry.get_text()))
                            data = server_conn.serverMessages.get()
                            if data == "Added gamer":
                                first_container.kill()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(event.pos)


            manager.process_events(event)
        
        main_window.fill((41, 49, 138))
        #main_form.fill((29, 34, 89))
        
        pygame.draw.line(main_window, (0,0,0), main_window.get_rect().midtop, main_window.get_rect().midbottom, 1)
        pygame.draw.line(main_window, (0,0,0), main_window.get_rect().midleft, main_window.get_rect().midright, 1)

        manager.update(time_delta)
        manager.draw_ui(main_window)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()