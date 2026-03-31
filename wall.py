import pygame

class Wall:
    def __init__(self, x, y, width, height):
        # cria uma área de colisão (parede invisível)
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
         #desenha a parede
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)