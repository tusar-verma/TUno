import pygame
import pygame_gui
import time

from src.TUnoClient.TUnoClientSocket import *
from src.TUnoClient.TUnoClientComponents import *

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
    
    fc = First_container(main_window.get_rect(),manager,1,server_conn)

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                if server_conn.connected:
                    server_conn.quit_game()
            fc.process_event(event)
            print(fc.is_enabled)
            print("asd")
                
            manager.process_events(event)
        
        main_window.fill((41, 49, 138))
        
        pygame.draw.line(main_window, (0,0,0), main_window.get_rect().midtop, main_window.get_rect().midbottom, 1)
        pygame.draw.line(main_window, (0,0,0), main_window.get_rect().midleft, main_window.get_rect().midright, 1)

        manager.update(time_delta)
        manager.draw_ui(main_window)

        pygame.display.update()

    pygame.quit()
 



if __name__ == "__main__":
    main()