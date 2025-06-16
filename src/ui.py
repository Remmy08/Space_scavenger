import pygame

class UI:
    def __init__(self):
        self.font = pygame.font.Font("assets/fonts/pixel.ttf", 36)
        self.warning_font = pygame.font.Font("assets/fonts/pixel.ttf", 48)
        try:
            self.bar_border = pygame.image.load("assets/sprites/ui/bar_border.png").convert_alpha()
            self.bar_border = pygame.transform.scale(self.bar_border, (200, 30))
            self.pollution_icon = pygame.image.load("assets/sprites/ui/pollution_icon.png").convert_alpha()
            self.health_icon = pygame.image.load("assets/sprites/ui/health_icon.png").convert_alpha()
            self.capacity_icon = pygame.image.load("assets/sprites/ui/capacity_icon.png").convert_alpha()
            print("Loaded: bar_border.png, pollution_icon.png, health_icon.png, capacity_icon.png")
        except FileNotFoundError:
            self.bar_border = pygame.Surface((200, 30))
            pygame.draw.rect(self.bar_border, (255, 255, 255), (0, 0, 200, 30), 2)
            self.pollution_icon = pygame.Surface((30, 30))
            self.health_icon = pygame.Surface((30, 30))
            self.capacity_icon = pygame.Surface((30, 30))
            self.pollution_icon.fill((255, 255, 255))
            self.health_icon.fill((255, 255, 255))
            self.capacity_icon.fill((255, 255, 255))
            print("Failed to load: bar_border.png, pollution_icon.png, health_icon.png, capacity_icon.png")
        self.warning_timer = 0
        self.show_warning = False

    def draw(self, screen, level):
        bg_color = (34, 32, 52)

        # Шкала загрязнения
        screen.blit(self.pollution_icon, (10, 10))
        pollution = level.pollution / 100
        if pollution <= 0.5:
            fill_color = (36, 181, 20)
        elif pollution <= 0.8:
            fill_color = (247, 194, 45)
        else:
            fill_color = (250, 54, 54)
        pollution_bar = pygame.Surface((200, 30))
        pollution_bar.fill(bg_color)
        filled_width = int(200 * pollution)
        pygame.draw.rect(pollution_bar, fill_color, (0, 0, filled_width, 30), border_radius=10)
        screen.blit(pollution_bar, (45, 10))
        screen.blit(self.bar_border, (45, 10))

        # Прочность
        screen.blit(self.health_icon, (10, 50))
        health = level.player.health / 100
        if health > 0.5:
            fill_color = (36, 181, 20)
        elif health >= 0.2:
            fill_color = (247, 194, 45)
        else:
            fill_color = (250, 54, 54)
        health_bar = pygame.Surface((200, 30))
        health_bar.fill(bg_color)
        filled_width = int(200 * health)
        pygame.draw.rect(health_bar, fill_color, (0, 0, filled_width, 30), border_radius=10)
        screen.blit(health_bar, (45, 50))
        screen.blit(self.bar_border, (45, 50))

        # Заполненность
        screen.blit(self.capacity_icon, (10, 90))
        capacity = level.player.capacity / level.player.max_capacity
        fill_color = (36, 181, 20)
        capacity_bar = pygame.Surface((200, 30))
        capacity_bar.fill(bg_color)
        filled_width = int(200 * capacity)
        pygame.draw.rect(capacity_bar, fill_color, (0, 0, filled_width, 30), border_radius=10)
        screen.blit(capacity_bar, (45, 90))
        screen.blit(self.bar_border, (45, 90))
        capacity_text = self.font.render(f"Мусор: {level.player.capacity}/{level.player.max_capacity}", True, (255, 255, 255))
        screen.blit(capacity_text, (255, 90))

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