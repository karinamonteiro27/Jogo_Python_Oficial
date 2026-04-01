import pygame
from utils import resource_path

class Player:
    def __init__(self, x, y):
        # carrega imagem do player
        self.image = pygame.image.load(resource_path("images/hero_50x75.png")).convert_alpha()

        # ajuste do tamanho
        self.image = pygame.transform.scale(self.image, (50, 75))

        # posição do player - cria o rentângulo
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # diminui o hitbox - o retângulo(rect) está um pouco maior que o personagem em si
        self.rect.inflate_ip(-10, -10)

        self.speed = 5

    def update(self, keys, walls):
        old_rect = self.rect.copy()

        # movimento
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # colisão com paredes
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect = old_rect

    def draw(self, screen):
        # desenha o player na tela
        screen.blit(self.image, self.rect)