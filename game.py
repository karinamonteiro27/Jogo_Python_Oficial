import pygame
import sys
from player import Player
from enemy import Enemy
from key import Key
from wall import Wall

# tamanho da tela
width, height = 920, 650

class Game:
    def __init__(self):
        pygame.init()

        # inicia o audio
        pygame.mixer.init()

        # carrega música de fundo
        pygame.mixer.music.load("sounds/Combat_music_wav.wav")

        # toca em loop infinito (-1)
        pygame.mixer.music.play(-1)

        # volume
        pygame.mixer.music.set_volume(0.5)

        # cria a tela
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("The Last Key: Castle Escape")

        self.state = "menu"

        # fonte
        self.font = pygame.font.SysFont(None, 48)

        self.walls = [
            # paredes externas

            Wall(0, 65, 800, 50),
            Wall(0, 550, 800, 50),
            Wall(0, 0, 50, 600),
            Wall(750, 40, 50, 150),
            Wall(750, 455, 50, 150),

            # área esquerda inferior

            Wall(0, 355, 390, 15),
            Wall(230, 355, 50, 200),

            # bloqueios centrais (escadas e divisões)
            Wall(280, 240, 110, 5),
            Wall(385, 200, 5, 78),
            Wall(480, 200, 5, 78),
            Wall(385, 360, 5, 78),
            Wall(480, 360, 5, 78),

            # corredor que chega ao portal
            Wall(480, 270, 180, 10),
            Wall(480, 360, 180, 10),

            # área arredondada final do corredor parte de cima

            Wall(660, 264, 15, 10),
            Wall(675, 260, 15, 10),
            Wall(690, 256, 15, 10),
            Wall(705, 252, 15, 10),
            Wall(715, 244, 15, 10),
            Wall(720, 236, 15, 10),
            Wall(725, 228, 15, 10),
            Wall(730, 220, 15, 10),
            Wall(735, 212, 15, 10),
            Wall(740, 204, 15, 10),
            Wall(742, 196, 15, 10),
            Wall(743, 188, 15, 10),

           # área arredondada final do corredor parte de baixo
            Wall(660, 360, 15, 10),
            Wall(675, 364, 15, 10),
            Wall(690, 368, 15, 10),
            Wall(705, 372, 15, 10),
            Wall(715, 380, 15, 10),
            Wall(720, 388, 15, 10),
            Wall(725, 396, 15, 10),
            Wall(730, 404, 15, 10),
            Wall(735, 412, 15, 10),
            Wall(740, 420, 15, 10),
            Wall(742, 428, 15, 10),
            Wall(743, 436, 15, 10),
            Wall(743, 444, 15, 10),


            #paredes em volta do portal

            Wall(840, 185, 50, 80),
            Wall(840, 380, 50, 80),
            Wall(800, 186, 50, 5),
            Wall(800, 455, 50, 5)
        ]

        self.clock = pygame.time.Clock()

        # carrega imagem do mapa
        self.map = pygame.image.load("images/map_909x638.png").convert()

        #portal inicial (lado esquerdo)
        self.start_portal = pygame.Rect(50, 170, 80, 120)

        # cria o player (posição inicial)
        self.player = Player(
            self.start_portal.x + 10,
            self.start_portal.y + 20)

        #cria inimigos e suas posições
        self.enemies = [
            Enemy(200, 100),
            Enemy(500, 200),
            Enemy(600, 400)
        ]

        # cria chaves espalhadas
        self.keys = [
            Key(150, 150),
            Key(400, 300),
            Key(700, 500),
            Key(350, 458)
        ]

        self.keys_collected = 0

        #portal final (lado direito) - finaliza o jogo
        self.end_portal = pygame.Rect(840, 284, 20, 70)

        self.running = True

    def update(self):


        keys = pygame.key.get_pressed()
        self.player.update(keys, self.walls)

        for enemy in self.enemies:
            enemy.update(self.player, self.walls)

        for key in self.keys:
            if not key.collected and self.player.rect.colliderect(key.rect):
                key.collected = True
                self.keys_collected += 1

         # bloqueia o portal se ainda não pegou todas as chaves
        if self.keys_collected < len(self.keys):
            if self.player.rect.colliderect(self.end_portal):

                 # impede o jogador de passar
                if self.player.rect.centerx < self.end_portal.centerx:
                    self.player.rect.right = self.end_portal.left
                else:
                    self.player.rect.left = self.end_portal.right


        # vitória
        if self.keys_collected == len(self.keys):
            if self.player.rect.colliderect(self.end_portal):
                self.state = "win"

        # derrota
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.state = "game_over"

    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.state == "menu":
            self.draw_menu()

        elif self.state == "how_to_play":
            self.draw_how_to_play()

        elif self.state == "playing":
            self.draw_game()

        elif self.state == "win":
            self.draw_win()

        elif self.state == "game_over":
            self.draw_game_over()

        pygame.display.flip()

    #criando menu
    def draw_menu(self):
        title = self.font.render("The Last Key: Castle Escape", True, (255, 255, 255))
        play = self.font.render("ENTER - Jogar", True, (255, 255, 255))
        how = self.font.render("H - Como Jogar", True, (255, 255, 255))

        self.screen.blit(title, (240, 150))
        self.screen.blit(play, (300, 300))
        self.screen.blit(how, (300, 350))

    #criando como jogar
    def draw_how_to_play(self):
        lines = [
            "*Use as setas para mover",
            "*Pegue todas as chaves",
            "*Evite os inimigos",
            "*Atravesse o Portal",
            "Clique em ESC para voltar ao menu" ]

    # percorre cada linha de texto e também pega o índice (i)

        for i, line in enumerate(lines):
            text = self.font.render(line, True, (255, 255, 255))
        # desenha o texto na tela
            self.screen.blit(text, (200, 150 + i * 50))

    def draw_game(self):

        # desenha o mapa de fundo
        self.screen.blit(self.map, (0, 0))

        # desenha o jogador
        self.player.draw(self.screen)

        # desenha todos os inimigos
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # desenha todas as chaves
        for key in self.keys:
            key.draw(self.screen)

        #desenha o portal final
        #pygame.draw.rect(self.screen, (0, 255, 255), self.end_portal, 2)

    def draw_win(self):
        # cria o texto de vitória
        text = self.font.render("VOCÊ VENCEU!", True, (0, 255, 0))

        # cria o texto de reiniciar
        restart = self.font.render("R - Reiniciar", True, (255, 255, 255))

        # desenha os textos na tela
        self.screen.blit(text, (250, 250))
        self.screen.blit(restart, (250, 320))

    def draw_game_over(self):
        # cria o texto de derrota
        text = self.font.render("GAME OVER", True, (255, 0, 0))

        # cria o texto de reiniciar
        restart = self.font.render("R - Reiniciar", True, (255, 255, 255))

        # desenha os textos na tela
        self.screen.blit(text, (250, 250))
        self.screen.blit(restart, (250, 320))

    def run(self):
        # loop principal do jogo (roda continuamente)
        while self.running:
            # limita o jogo a 60 FPS
            self.clock.tick(60)

            # verifica teclado, fechar janela, etc
            for event in pygame.event.get():
                # se fechar a janela, encerra o jogo
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # verifica quando uma tecla é pressionada
                if event.type == pygame.KEYDOWN:

                    # controles do menu inicial
                    if self.state == "menu":
                        if event.key == pygame.K_RETURN:
                            self.state = "playing"  # inicia o jogo
                        if event.key == pygame.K_h:
                            self.state = "how_to_play"  # vai para instruções

                    # tela de instruções
                    elif self.state == "how_to_play":
                        if event.key == pygame.K_ESCAPE:
                            self.state = "menu"  # volta ao menu

                    # telas de vitória ou derrota
                    elif self.state in ["win", "game_over"]:
                        if event.key == pygame.K_r:
                            self.__init__()  # reinicia o jogo

            # só atualiza o jogo se estiver jogando
            if self.state == "playing":
                self.update()

            # desenha a tela atual
            self.draw()

