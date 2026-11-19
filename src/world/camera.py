import pygame

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.offset = pygame.Vector2(0,0)

    def update(self, target):
        self.offset.x = target.position.x - self.width / 2
        self.offset.y = target.position.y - self.height / 2