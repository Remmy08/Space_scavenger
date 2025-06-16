import pygame

class UnloadZone(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/sprites/ui/unload_zone.png").convert_alpha()
            print("Загружено: assets/sprites/ui/unload_zone.png")
        except FileNotFoundError:
            self.image = pygame.Surface((200, 100))
            self.image.fill((0, 128, 255))
            print("Не удалось загрузить: assets/sprites/ui/unload_zone.png")
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

class Level:
    def __init__(self, player, garbage_group, asteroid_group, level_num):
        self.player = player
        self.garbage_group = garbage_group
        self.asteroid_group = asteroid_group
        self.unload_zone = UnloadZone(1920 // 2, 1080 - 50)
        self.pollution = 0
        self.balance = 0
        self.time_remaining = 0  # Начинаем с 0 для бесконечного режима
        self.level_num = level_num
        self.pollution_rate = 0.2  # Базовый прирост загрязнения
        self.delta_time = 0
        self.progression_timer = 0  # Таймер для усложнения каждые 30 секунд

    def update(self, time_left, menu):
        self.time_remaining = time_left  # Обновляем время
        self.delta_time += 1000 / 60
        self.progression_timer += 1000 / 60
        pollution_increase = 0
        if self.delta_time >= 1000:
            pollution_increase = self.pollution_rate * len(self.garbage_group) * (self.level_num * 0.5)
            self.pollution += pollution_increase * (self.delta_time / 1000)
            self.delta_time = 0
        self.pollution = min(100, self.pollution)
        print(f"Delta time: {self.delta_time}, Увеличение загрязнения: {pollution_increase * (self.delta_time / 1000)}, Общее загрязнение: {self.pollution}")

        # Усложнение каждые 30 секунд
        if self.progression_timer >= 30000:
            self.progression_timer = 0
            self.pollution_rate += 0.05
            menu.max_garbage += 3
            menu.asteroid_speed += 0.2
            menu.garbage_spawn_timer = max(1000, menu.garbage_spawn_timer - 1000)
            menu.asteroid_spawn_timer = max(3000, menu.asteroid_spawn_timer - 1000)
            pygame.time.set_timer(pygame.USEREVENT + 1, int(menu.garbage_spawn_timer))
            pygame.time.set_timer(pygame.USEREVENT + 2, int(menu.asteroid_spawn_timer))
            print(f"Усложнение: pollution_rate={self.pollution_rate}, max_garbage={menu.max_garbage}, "
                  f"garbage_spawn_timer={menu.garbage_spawn_timer}, asteroid_spawn_timer={menu.asteroid_spawn_timer}, "
                  f"asteroid_speed={menu.asteroid_speed}")

        if self.pollution >= 100 or self.player.durability <= 0:
            print(f"Условие завершения уровня достигнуто! Загрязнение: {self.pollution}, Прочность: {self.player.durability}")

    def add_balance(self, amount):
        self.balance += amount
        self.decrease_pollution(0.2 * (1 + self.level_num * 0.1))
        print(f"Баланс увеличен на {amount}, текущий баланс: {self.balance}")

    def decrease_pollution(self, amount):
        self.pollution = max(0, self.pollution - amount)