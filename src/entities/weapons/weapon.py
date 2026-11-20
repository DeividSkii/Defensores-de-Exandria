class Weapon:
    def __init__(self, player):
        self.player = player

    def update(self, delta_time):
        pass

    def draw(self, screen, camera):
        pass

    def check_collision(self, enemies):
        return []