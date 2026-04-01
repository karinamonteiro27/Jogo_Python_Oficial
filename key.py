import pygame
from utils import resource_path

class Key:
    def __init__(self, x, y):
        # carrega imagem da chave
        self.image = pygame.image.load(resource_path("images/key_30x30.png")).convert_alpha()

        # tamanho da chave
        self.image = pygame.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect(topleft=(x, y))

        self.collected = False

    def draw(self, screen):
        # só desenha se ainda não foi coletada
        if not self.collected:
            screen.blit(self.image, self.rect)