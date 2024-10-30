import pygame
class GameButton: 
        def __init__(self, x, y, image, allow):
            self.image = image
            self.rect = self.image.get_rect(topleft=(x, y))
            self.clicked = False
            self.allow = allow
            self.initial_click_processed = False

        def draw(self, surface):
            surface.blit(self.image, self.rect)
            action = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()[0]  

            if not self.initial_click_processed: # gia na katharisei sto prwto click
                if mouse_click == 0:
                    self.initial_click_processed = True
                return action

            if self.rect.collidepoint(mouse_pos) and mouse_click == 1 and not self.clicked:
                action = True
                if not self.allow:
                    self.clicked = True

            if mouse_click == 0:
                self.clicked = False
            return action