import pygame

class UnloadZone(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/sprites/ui/unload_zone.png").convert_alpha()
        except FileNotFoundError:
            self.image = pygame.Surface((200, 100))
            self.image.fill((0, 128, 255))  # Голубая заглушка
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

class Level:
    def __init__(self, player, garbage_group, asteroid_group):
        self.player = player
        self.garbage_group = garbage_group
        self.asteroid_group = asteroid_group
        self.unload_zone = UnloadZone(1280 // 2, 720 - 50)  # Зона внизу по центру
        self.pollution = 0
        self.score = 0
        self.time_remaining = 120 * 1000
        self.unload_timer = 0

    def update(self):
        self.time_remaining -= 1000 / 60
        self.pollution += 0.005 * len(self.garbage_group)
        if self.time_remaining <= 0 or self.pollution >= 100 or self.player.health <= 0:
            print("Игра окончена!")
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Разгрузка мусора
        if pygame.sprite.collide_rect(self.player, self.unload_zone):
            self.unload_timer += 1000 / 60
            if self.unload_timer >= 1000 / 3:  # 3 единицы в секунду
                self.unload_timer = 0
                if self.player.capacity > 0:
                    self.player.capacity -= 1
                    self.add_score(1)
                    self.decrease_pollution(0.1)

    def add_score(self, points):
        self.score += points

    def decrease_pollution(self, amount):
        self.pollution = max(0, self.pollution - amount)