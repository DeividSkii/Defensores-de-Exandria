import pygame

class Enemy(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()

        #Posição no mundo
        self.position = pygame.Vector2(x,y)

        #Atributos
        self.size = 32
        self.speed = 70
        self.max_health = 10
        self.health = self.max_health
        self.hit_flash_timer = 0
        self.hit_flash_duration = 0.1

        #Aparencia
        self.color = pygame.color.THECOLORS["red"]

        #Imagem
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)

        #Hitbox
        self.rect = self.image.get_rect(center=(x,y))

    def follow_target(self, player, delta_time):

        #Atualizar flash
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= delta_time


        #Calcula direção até player
        direction = player.position - self.position

        if direction.length() > 0:
            direction = direction.normalize()

        #Movimenta o inimigo
        self.position += direction * self.speed * delta_time

    def take_damage(self, damage):
        self.health -= damage
        self.hit_flash_timer = self.hit_flash_duration

        if self.health <= 0:
            self.kill()

    def draw(self, screen, camera):

        #Define cor do inimigo
        if self.hit_flash_timer > 0:
            self.image.fill((255,255,255))
        else:
            self.image.fill(self.color)

        # Converte posição do mundo para tela
        screen_position = self.position - camera

        self.rect.center = screen_position

        screen.blit(self.image, self.rect)
