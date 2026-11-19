import pygame

class DamageNumber:

    def __init__(self, value,position):
        self.value = value
        self.position = pygame.Vector2(position)

        self.speed = 40
        self.duration = 0.7
        self.timer = 0

        self.font = pygame.font.SysFont(None, 24)
        self.image = self.font.render(str(value), True, (255,255,255))

    def update(self, delta_time):
        self.timer += delta_time
        self.position.y -= self.speed * delta_time

    def draw(self, screen, camera):
        screen_position = self.position - camera

        screen.blit(self.image, (int(screen_position.x), int(screen_position.y)))

    def is_finished(self):
        return self.timer >= self.duration