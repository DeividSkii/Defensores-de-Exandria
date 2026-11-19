import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        #Posição no mundo
        self.position = pygame.Vector2(x,y)
        self.facing_direction = pygame.Vector2(0, -1)

        #Atributos
        self.size = 32
        self.speed = 100

        #Aparência
        self.color = (255, 255,0)

        #Imagem
        self.image = pygame.Surface([self.size,self.size])
        self.image.fill(self.color)

        #Retangulo de posicionamento
        self.rect = self.image.get_rect(center=(x,y))

    def handle_movement(self, delta_time):
        keys = pygame.key.get_pressed()

        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_DOWN]:
            direction.y += 1

        if keys[pygame.K_UP]:
            direction.y -= 1

        if keys[pygame.K_LEFT]:
            direction.x -= 1

        if keys[pygame.K_RIGHT]:
            direction.x += 1

        # Evita velocidade maior na diagonal
        if direction.length() > 0:
            direction = direction.normalize()
            self.facing_direction = direction

        self.position += direction * self.speed * delta_time

    def draw(self, screen, camera):
        # Converte posição do mundo para posição da tela
        screen_position = self.position - camera

        self.rect.center = screen_position


        screen.blit(self.image, self.rect)