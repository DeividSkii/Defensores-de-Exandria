import pygame

class Enemy(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()

        #Posição no mundo
        self.position = pygame.Vector2(x,y)

        #Atributos
        self.size = 35
        self.speed = 70

        #Aparencia
        self.color = pygame.color.THECOLORS["red"]

        #Imagem
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)

        #Hitbox
        self.rect = self.image.get_rect(center=(x,y))

    def seguir_player(self, player, delta_time):

        #Calcula direção até player
        direction = player.position - self.position

        if direction.length() > 0:
            direction = direction.normalize()

        #Movimenta o inimigo
        self.position += direction * self.speed * delta_time

    def draw(self, screen, camera):

        # Converte posição do mundo para tela
        screen_position = self.position - camera

        self.rect.center = screen_position

        screen.blit(self.image, self.rect)
