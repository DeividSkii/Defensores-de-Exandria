from unittest import enterModuleContext

import pygame
import sys

from entities.player import Player
from entities.enemy import Enemy


#Iniciando
pygame.init()

#Janela
WIDTH = 1280
HEIGHT = 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Defensores de Exandria")

clock = pygame.time.Clock()

#Jogador
player = Player(0,0)

#Inimigo
enemy = Enemy(300,0)

#CORES
cores = {
    "preto" : pygame.Color("black"),
    "verde" : pygame.Color("green"),
    "azul" : pygame.Color("blue"),
    "vermelho" : pygame.Color("red"),
}

#Loop
running = True

while running:

    #Tempo entre frames
    delta_time = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Jogador atualizacao
    player.handle_movement(delta_time)
    enemy.seguir_player(player, delta_time)

    #camera cntralizada
    camera = pygame.Vector2(player.position.x - WIDTH / 2, player.position.y - HEIGHT / 2)

    #Desenho
    screen.fill(cores["preto"])

    #Grade do mundo
    grid_size = 100

    start_x = int(camera.x // grid_size) * grid_size
    start_y = int(camera.y // grid_size) * grid_size

    for x in range(start_x, start_x + WIDTH + grid_size, grid_size):
        screen_x = x - camera.x
        pygame.draw.line(
            screen, cores["vermelho"],
            (screen_x, 0),
            (screen_x, HEIGHT)
        )

    for y in range(start_y, start_y + HEIGHT + grid_size, grid_size):
        screen_y = y - camera.y
        pygame.draw.line(
            screen, cores["vermelho"],
            (0, screen_y),
            (WIDTH, screen_y)
        )

    # Jogador sempre no centro da tela
    player.draw(screen, camera)
    enemy.draw(screen, camera)

    pygame.display.flip()

pygame.quit()
sys.exit()