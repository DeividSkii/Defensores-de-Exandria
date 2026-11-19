import random

import pygame
from src.settings import WIDTH, HEIGHT, FPS
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.world.camera import Camera
from src.entities.weapons.axe import Axe
from src.entities.damage_number import DamageNumber


class Game:
    def __init__(self):

        self.spawn_timer = 0
        self.spawn_interval = 2

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True

        self.damage_numbers = []

        # Jogador
        self.player = Player(0, 0)
        self.axe = Axe(self.player)

        #Inimigos
        self.enemies = pygame.sprite.Group()

        # CORES
        self.cores = {
            "preto": pygame.Color("black"),
            "verde": pygame.Color("green"),
            "azul": pygame.Color("blue"),
            "vermelho": pygame.Color("red"),
        }

        self.clock = pygame.time.Clock()

        self.camera = Camera(WIDTH, HEIGHT)

        self.direcoes = {
            "norte": pygame.Vector2(0,-(HEIGHT / 2 + 100)),
            "sul": pygame.Vector2(0,HEIGHT / 2 + 100),
            "leste": pygame.Vector2(WIDTH / 2 + 300, 0),
            "oeste": pygame.Vector2(-(WIDTH / 2 + 300), 0),
        }

    def run(self):
        while self.running:
            #Tempo entre frames
            delta_time = self.clock.tick(FPS) / 1000

            self.handle_events()
            self.update(delta_time)
            self.draw()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


    def update(self, delta_time):
    # Jogador atualizacao
        self.player.handle_movement(delta_time)

        for enemy in self.enemies:
            enemy.follow_target(self.player, delta_time)


        self.camera.update(self.player)

        self.spawn_timer += delta_time

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer -= self.spawn_interval
            if len(self.enemies) < 50:
                self.spawn_enemy()

        self.axe.update(delta_time)
        self.axe.check_collision(self.enemies, self.damage_numbers)

        for damage_number in self.damage_numbers:
            damage_number.update(delta_time)

        self.damage_numbers = [
            number for number in self.damage_numbers
            if not number.is_finished()
        ]




    def draw(self):


        # Desenho
        self.screen.fill(self.cores["preto"])

        # Grade do mundo
        grid_size = 100

        start_x = int(self.camera.offset.x // grid_size) * grid_size
        start_y = int(self.camera.offset.y // grid_size) * grid_size

        for x in range(start_x, start_x + WIDTH + grid_size, grid_size):
            screen_x = x - self.camera.offset.x
            pygame.draw.line(
                self.screen, self.cores["vermelho"],
                (screen_x, 0),
                (screen_x, HEIGHT)
            )

        for y in range(start_y, start_y + HEIGHT + grid_size, grid_size):
            screen_y = y - self.camera.offset.y
            pygame.draw.line(
                self.screen, self.cores["vermelho"],
                (0, screen_y),
                (WIDTH, screen_y)
            )

        # Jogador sempre no centro da tela
        self.player.draw(self.screen, self.camera.offset)
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera.offset)

        self.axe.draw(self.screen, self.camera.offset)

        for damage_number in self.damage_numbers:
            damage_number.draw(self.screen, self.camera.offset)

        pygame.display.flip()

    def spawn_enemy(self):


        lado = random.choice(list(self.direcoes.keys()))
        if lado == "norte" or lado == "sul":
            posicao_x = random.randint(-WIDTH // 2, WIDTH // 2)
            posicao_y = 0
        elif lado == "leste" or lado == "oeste":
            posicao_y = random.randint(-HEIGHT // 2, HEIGHT// 2)
            posicao_x = 0
        deslocamento = self.direcoes[lado]
        posicao_aleatoria = pygame.Vector2(posicao_x, posicao_y)

        posicao_inimigo = self.player.position + deslocamento + posicao_aleatoria
        self.enemies.add(Enemy(posicao_inimigo[0], posicao_inimigo[1]))