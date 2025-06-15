import pygame

class UI:
    def __init__(self, scale_factor):
        self.scale_factor = scale_factor
        self.font = pygame.font.Font("assets/fonts/pixel.ttf", int(36 * self.scale_factor))
        self.warning_font = pygame.font.Font("assets/fonts/pixel.ttf", int(48 * self.scale_factor))
        try:
            self.bar_border = pygame.image.load("assets/sprites/ui/bar_border.png").convert_alpha()
            self.bar_border = pygame.transform.scale(self.bar_border, (int(200 * self.scale_factor), int(30 * self.scale_factor)))
            self.pollution_icon = pygame.image.load("assets/sprites/ui/pollution_icon.png").convert_alpha()
            self.health_icon = pygame.image.load("assets/sprites/ui/health_icon.png").convert_alpha()
            self.capacity_icon = pygame.image.load("assets/sprites/ui/capacity_icon.png").convert_alpha()
            print("Loaded: bar_border.png, pollution_icon.png, health_icon.png, capacity_icon.png")
        except FileNotFoundError:
            self.bar_border = pygame.Surface((int(200 * self.scale_factor), int(30 * self.scale_factor)))
            pygame.draw.rect(self.bar_border, (255, 255, 255), (0, 0, int(200 * self.scale_factor), int(30 * self.scale_factor)), 2)
            self.pollution_icon = pygame.Surface((int(30 * self.scale_factor), int(30 * self.scale_factor)))
            self.health_icon = pygame.Surface((int(30 * self.scale_factor), int(30 * self.scale_factor)))
            self.capacity_icon = pygame.Surface((int(30 * self.scale_factor), int(30 * self.scale_factor)))
            self.pollution_icon.fill((255, 255, 255))
            self.health_icon.fill((255, 255, 255))
            self.capacity_icon.fill((255, 255, 255))
            print("Failed to load: bar_border.png, pollution_icon.png, health_icon.png, capacity_icon.png")
        self.warning_timer = 0
        self.show_warning = False

    def draw(self, screen, level, scale_factor):
        bg_color = (34, 32, 52)

        # Шкала загрязнения
        screen.blit(pygame.transform.scale(self.pollution_icon, (int(30 * scale_factor), int(30 * scale_factor))), (int(10 * scale_factor), int(10 * scale_factor)))
        pollution = level.pollution / 100
        if pollution <= 0.5:
            fill_color = (36, 181, 20)
        elif pollution <= 0.8:
            fill_color = (247, 194, 45)
        else:
            fill_color = (250, 54, 54)
        pollution_bar = pygame.Surface((int(200 * scale_factor), int(30 * scale_factor)))
        pollution_bar.fill(bg_color)
        filled_width = int(200 * scale_factor * pollution)
        pygame.draw.rect(pollution_bar, fill_color, (0, 0, filled_width, int(30 * scale_factor)), border_radius=int(10 * scale_factor))
        screen.blit(pollution_bar, (int(45 * scale_factor), int(10 * scale_factor)))
        screen.blit(pygame.transform.scale(self.bar_border, (int(200 * scale_factor), int(30 * scale_factor))), (int(45 * scale_factor), int(10 * scale_factor)))

        # Прочность
        screen.blit(pygame.transform.scale(self.health_icon, (int(30 * scale_factor), int(30 * scale_factor))), (int(10 * scale_factor), int(50 * scale_factor)))
        health = level.player.health / 100
        if health > 0.5:
            fill_color = (36, 181, 20)
        elif health >= 0.2:
            fill_color = (247, 194, 45)
        else:
            fill_color = (250, 54, 54)
        health_bar = pygame.Surface((int(200 * scale_factor), int(30 * scale_factor)))
        health_bar.fill(bg_color)
        filled_width = int(200 * scale_factor * health)
        pygame.draw.rect(health_bar, fill_color, (0, 0, filled_width, int(30 * scale_factor)), border_radius=int(10 * scale_factor))
        screen.blit(health_bar, (int(45 * scale_factor), int(50 * scale_factor)))
        screen.blit(pygame.transform.scale(self.bar_border, (int(200 * scale_factor), int(30 * scale_factor))), (int(45 * scale_factor), int(50 * scale_factor)))

        # Заполненность
        screen.blit(pygame.transform.scale(self.capacity_icon, (int(30 * scale_factor), int(30 * scale_factor))), (int(10 * scale_factor), int(90 * scale_factor)))
        capacity = level.player.capacity / level.player.max_capacity
        fill_color = (36, 181, 20)
        capacity_bar = pygame.Surface((int(200 * scale_factor), int(30 * scale_factor)))
        capacity_bar.fill(bg_color)
        filled_width = int(200 * scale_factor * capacity)
        pygame.draw.rect(capacity_bar, fill_color, (0, 0, filled_width, int(30 * scale_factor)), border_radius=int(10 * scale_factor))
        screen.blit(capacity_bar, (int(45 * scale_factor), int(90 * scale_factor)))
        screen.blit(pygame.transform.scale(self.bar_border, (int(200 * scale_factor), int(30 * scale_factor))), (int(45 * scale_factor), int(90 * scale_factor)))
        capacity_text = self.font.render(f"Мусор: {level.player.capacity}/{level.player.max_capacity}", True, (255, 255, 255))
        screen.blit(capacity_text, (int(255 * scale_factor), int(90 * scale_factor)))

        # Таймер
        time_text = self.font.render(f"Время: {int(level.time_remaining // 1000)}", True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(int(1920 // 2 * scale_factor), int(30 * scale_factor)))
        screen.blit(time_text, time_rect)

        # Надпись "Корабль заполнен"
        if level.player.capacity >= level.player.max_capacity:
            self.warning_timer += 1000 / 60
            if self.warning_timer >= 500:
                self.show_warning = not self.show_warning
                self.warning_timer = 0
            if self.show_warning:
                warning_text = self.warning_font.render("Корабль заполнен", True, (255, 255, 255))
                warning_rect = warning_text.get_rect(center=(int(1920 // 2 * scale_factor), int(1080 // 2 * scale_factor)))
                screen.blit(warning_text, warning_rect)