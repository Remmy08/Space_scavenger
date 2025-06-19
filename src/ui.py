import pygame

class UI:
    def __init__(self):
        try:
            self.font = pygame.font.Font("assets/fonts/pixel.ttf", 36)
            self.warning_font = pygame.font.Font("assets/fonts/pixel.ttf", 48)
            print("Loaded: assets/fonts/pixel.ttf")
        except FileNotFoundError:
            self.font = pygame.font.SysFont("arial", 36)
            self.warning_font = pygame.font.SysFont("arial", 48)
            print("Failed to load: assets/fonts/pixel.ttf")
        # Загрузка иконок
        try:
            self.pollution_icon = pygame.image.load("assets/sprites/ui/pollution_icon.png").convert_alpha()
            self.durability_icon = pygame.image.load("assets/sprites/ui/durability_icon.png").convert_alpha()
            self.capacity_icon = pygame.image.load("assets/sprites/ui/capacity_icon.png").convert_alpha()
            print("Loaded: pollution_icon.png, durability_icon.png, capacity_icon.png")
        except FileNotFoundError:
            self.pollution_icon = pygame.Surface((64, 64))
            self.durability_icon = pygame.Surface((64, 64))
            self.capacity_icon = pygame.Surface((64, 64))
            self.pollution_icon.fill((255, 255, 255))
            self.durability_icon.fill((255, 255, 255))
            self.capacity_icon.fill((255, 255, 255))
            print("Failed to load: pollution_icon.png, durability_icon.png, capacity_icon.png")
        # Загрузка универсальных спрайтов шкал
        self.bars = []
        for i in range(11):
            try:
                bar = pygame.image.load(f"assets/sprites/ui/bar_{i}.png").convert_alpha()
                bar = pygame.transform.scale(bar, (320, 64))
                self.bars.append(bar)
                print(f"Loaded: bar_{i}.png")
            except FileNotFoundError:
                bar = pygame.Surface((320, 64))
                bar.fill((100, 100, 100))
                self.bars.append(bar)
                print(f"Failed to load: bar_{i}.png")
        self.warning_timer = 0
        self.show_warning = False

    def draw(self, screen, level):
        # Загрязнение
        screen.blit(self.pollution_icon, (10, 10))
        pollution_index = min(10, int(level.pollution / 10))  # 0-100% -> 0-10
        screen.blit(self.bars[pollution_index], (90, 10))

        # Прочность
        screen.blit(self.durability_icon, (10, 100))
        durability_index = min(10, int(level.player.durability))  # 0-10
        screen.blit(self.bars[durability_index], (90, 100))

        # Вместимость
        screen.blit(self.capacity_icon, (10, 190))
        capacity_index = min(10, int(level.player.capacity / level.player.max_capacity * 10))  # 0-100% -> 0-10
        screen.blit(self.bars[capacity_index], (90, 190))
        # capacity_text = self.font.render(f"{int(level.player.capacity)}/{int(level.player.max_capacity)}", True, (255, 255, 255))
        # screen.blit(capacity_text, (500, 190))

        # Таймер в формате MM:SS
        minutes = int(level.time_remaining // 60000)
        seconds = int((level.time_remaining % 60000) // 1000)
        time_text = self.font.render(f"Время: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(1920 // 2, 30))
        screen.blit(time_text, time_rect)

        # Надпись "Корабль заполнен"
        if level.player.capacity >= level.player.max_capacity:
            self.warning_timer += 1000 / 60
            if self.warning_timer >= 500:
                self.show_warning = not self.show_warning
                self.warning_timer = 0
            if self.show_warning:
                warning_text = self.warning_font.render("Корабль заполнен", True, (255, 255, 255))
                warning_rect = warning_text.get_rect(center=(1920 // 2, 1080 // 2))
                screen.blit(warning_text, warning_rect)