import pygame
from src.entities.damage_number import DamageNumber


class Axe:
    def __init__(self, player):
        #Atributos
        self.player = player

        self.damage = 10
        self.attack_speed = 2.0
        self.range = 100
        self.size = 60

        self.attack_timer = 0
        self.attack_duration = 0.4
        self.hit_enemies = set()

        self.animation_timer = 0
        self.is_attacking = False
        self.attack_direction = pygame.Vector2(0, -1)

    def update(self, delta_time):
        if self.is_attacking:
            self.animation_timer += delta_time
            if self.animation_timer >= self.attack_duration:
                self.is_attacking = False
        else:
            self.attack_timer += delta_time
            if self.attack_timer >= self.attack_speed:
                self.hit_enemies.clear()
                self.is_attacking = True
                self.attack_direction = self.player.facing_direction.copy()
                self.attack_timer -= self.attack_speed
                self.animation_timer = 0

    def get_position(self):
        return self.player.position + (self.attack_direction * self.range)

    def get_attack_position(self):
        centro = self.player.position

        lateral = self.attack_direction.rotate(90)

        ponta = centro + self.attack_direction * self.range

        ponto_esquerdo = ponta + lateral * self.size
        ponto_direito = ponta - lateral * self.size

        return [centro, ponto_esquerdo, ponto_direito]

    def draw(self, screen, camera):
        if self.is_attacking:
            pontos = self.get_attack_position()

            pontos_tela = [ponto - camera for ponto in pontos]

            pygame.draw.polygon(screen, (255, 0, 0), pontos_tela)

    def point_in_triangle(self, point, triangle):
        a, b, c = triangle

        area = abs((b.x - a.x) * (c.y - a.y) -
                   (c.x - a.x) * (b.y - a.y))

        area1 = abs((a.x - point.x) * (b.y - point.y) -
                    (b.x - point.x) * (a.y - point.y))

        area2 = abs((b.x - point.x) * (c.y - point.y) -
                    (c.x - point.x) * (b.y - point.y))

        area3 = abs((c.x - point.x) * (a.y - point.y) -
                    (a.x - point.x) * (c.y - point.y))

        return area == area1 + area2 + area3

    def check_collision(self, enemies, damage_numbers):
        if not self.is_attacking:
            return

        triangle = self.get_attack_position()

        for enemy in enemies:
            if enemy in self.hit_enemies:
                continue

            if self.point_in_triangle(enemy.position, triangle):
                enemy.take_damage(self.damage)
                damage_numbers.append(
                    DamageNumber(self.damage, enemy.position)
                )
                self.hit_enemies.add(enemy)

