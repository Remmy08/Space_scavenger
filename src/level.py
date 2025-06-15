import pygame

class UnloadZone(pygame.sprite.Sprite):
    def __init__(self, x, y, scale_factor):
        super().__init__()
        self.scale_factor = scale_factor
        try:
            self.image = pygame.image.load("assets/sprites/ui/unload_zone.png").convert_alpha()
            print("Loaded: assets/sprites/ui/unload_zone.png")
        except FileNotFoundError:
            self.image = pygame.Surface((200, 100))
            self.image.fill((0, 128, 255))
            print("Failed to load: assets/sprites/ui/unload_zone.png")
        self.base_rect = self.image.get_rect(center=(x, y))
        self.rect = self.base_rect.copy()

    def draw(self, screen, scale_factor):
        scaled_img = pygame.transform.scale(self.image, (int(self.image.get_width() * scale_factor), int(self.image.get_height() * scale_factor)))
        scaled_rect = self.base_rect.copy()
        scaled_rect.x *= scale_factor
        scaled_rect.y *= scale_factor
        scaled_rect.width *= scale_factor
        scaled_rect.height *= scale_factor
        screen.blit(scaled_img, scaled_rect)

    def draw_hitbox(self, screen, scale_factor):
        scaled_rect = self.rect.copy()
        scaled_rect.x *= scale_factor
        scaled_rect.y *= scale_factor
        scaled_rect.width *= scale_factor
        scaled_rect.height *= scale_factor
        pygame.draw.rect(screen, (255, 0, 0), scaled_rect, 2)

class Level:
    def __init__(self, player, garbage_group, asteroid_group, scale_factor, level_num):
        self.player = player
        self.garbage_group = garbage_group
        self.asteroid_group = asteroid_group
        self.scale_factor = scale_factor
        self.unload_zone = UnloadZone(1920 // 2, 1080 - 50, scale_factor)
        self.pollution = 0
        self.score = 0
        self.time_remaining = 60000  # Начальное время 60 секунд (60000 мс)
        self.unload_timer = 0
        self.level_num = level_num
        self.pollution_rate = 0.2  # Базовый прирост 0.2 за мусор за секунду
        self.delta_time = 0  # Для нормализации времени

    def update(self, time_left):
        self.time_remaining = max(0, time_left)  # Обновляем оставшееся время
        self.delta_time += 1000 / 60  # Увеличиваем на длительность кадра (примерно 16.67 мс)
        pollution_increase = 0  # Инициализируем переменную
        if self.delta_time >= 1000:  # Нормализуем на секунду
            pollution_increase = self.pollution_rate * len(self.garbage_group) * (self.level_num * 0.5)  # Увеличиваем с уровнем
            self.pollution += pollution_increase * (self.delta_time / 1000)
            self.delta_time = 0  # Сбрасываем таймер
        self.pollution = min(100, self.pollution)  # Ограничиваем максимум 100
        print(f"Delta time: {self.delta_time}, Pollution increase: {pollution_increase * (self.delta_time / 1000)}, Total pollution: {self.pollution}")
        if self.time_remaining <= 0 or self.pollution >= 100 or self.player.health <= 0:
            print(f"Условие завершения уровня достигнуто! Time: {self.time_remaining}, Pollution: {self.pollution}, Health: {self.player.health}")

        if pygame.sprite.collide_rect(self.player, self.unload_zone):
            self.unload_timer += 1000 / 60
            if self.unload_timer >= 1000 / 3:
                self.unload_timer = 0
                if self.player.capacity > 0:
                    self.player.capacity -= 1
                    self.add_score(1)
                    self.decrease_pollution(0.2 * (1 + self.level_num * 0.1))  # Уменьшаем на 0.2 за мусор

    def add_score(self, points):
        self.score += points

    def decrease_pollution(self, amount):
        self.pollution = max(0, self.pollution - amount)