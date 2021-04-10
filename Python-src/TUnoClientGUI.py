import pygame
import pygame_gui
from TUnoClientSprites import *
from TUnoClientSocket import *

SCREEN_WIDTH = 16*75
SCREEN_HEIGHT = 9*75


def main():
    
    pygame.init()
    running = True

    try:
        server_conn = TUnoClient()
    except:
        print("Couldn't connect to server")


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

    first_button_size = (500,40)

    first_button = pygame_gui.elements.UIButton(
        relative_rect = pygame.Rect((main_window.get_rect().centerx - (first_button_size[0] / 2) ,main_window.get_rect().centery - (first_button_size[1] / 2)),first_button_size),
        manager = manager,
        container= first_container,
        text = "Join",
        anchors={
            "left":"left",
            "right": "right",
            "top": "top",
            "bottom": "bottom"
        }
    )

    first_textentry = pygame_gui.elements.UITextEntryLine(
        relative_rect= first_button.get_relative_rect().move(0,-100),
        manager = manager,
        container= first_container,
        anchors={
            "left":"left",
            "right": "right",
            "top": "top",
            "bottom": "bottom"
        }
    )
    

    first_textbox = pygame_gui.elements.UITextBox(
        html_text= "Please enter a user name",
        relative_rect= first_button.get_relative_rect().move(0,-140),
        manager= manager,
        container= first_container
    )

    while running:

        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == first_button:

                        
                        first_container.kill()
            
            manager.process_events(event)
        
        manager.update(time_delta)
        main_window.fill((41, 49, 138))
        #main_form.fill((29, 34, 89))
        
        pygame.draw.line(main_window, (0,0,0), main_window.get_rect().midtop, main_window.get_rect().midbottom, 1)
        pygame.draw.line(main_window, (0,0,0), main_window.get_rect().midleft, main_window.get_rect().midright, 1)

        manager.draw_ui(main_window)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()