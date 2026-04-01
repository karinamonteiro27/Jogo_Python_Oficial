import pygame
from utils import resource_path

class Enemy:
    def __init__(self, x, y):

        # carrega imagem
        self.image = pygame.image.load(resource_path("images/enemy_42x58.png")).convert_alpha()

        # tamanho do inimigo
        self.image = pygame.transform.scale(self.image, (42, 58))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # diminui o hitbox
        self.rect.inflate_ip(-20, -30)

        self.speed = 1

        # controla velocidade
        self.move_delay = 50  # quanto maior, mais lento
        self.last_move = pygame.time.get_ticks()

    def update(self, player, walls):
        current_time = pygame.time.get_ticks()

        # só move após o tempo definido
        if current_time - self.last_move > self.move_delay:
            self.last_move = current_time

            # diferença entre player e inimigo
            dx = player.rect.x - self.rect.x
            dy = player.rect.y - self.rect.y

            # se move na horizontal
            if dx > 0:
                self.rect.x += self.speed
            elif dx < 0:
                self.rect.x -= self.speed

            # colisão horizontal
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dx > 0:
                        self.rect.right = wall.rect.left
                    elif dx < 0:
                        self.rect.left = wall.rect.right

            # se move na vertical
            if dy > 0:
                self.rect.y += self.speed
            elif dy < 0:
                self.rect.y -= self.speed

            # colisão vertical
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dy > 0:
                        self.rect.bottom = wall.rect.top
                    elif dy < 0:
                        self.rect.top = wall.rect.bottom

    def draw(self, screen):
        screen.blit(self.image, self.rect)