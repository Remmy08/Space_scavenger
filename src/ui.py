import pygame

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen, level):
        # Шкала загрязнения
        pollution_bar = pygame.Surface((200, 20))
        pollution_bar.fill((255, 0, 0))  # Красная шкала
        filled_width = 200 * (level.pollution / 100)
        pygame.draw.rect(pollution_bar, (0, 255, 0), (0, 0, filled_width, 20))
        screen.blit(pollution_bar, (10, 10))

        # Таймер
        time_text = self.font.render(f"Время: {int(level.time_remaining // 1000)}", True, (255, 255, 255))
        screen.blit(time_text, (10, 40))

        # Прочность
        health_bar = pygame.Surface((200, 20))
        health_bar.fill((255, 0, 0))
        filled_width = 200 * (level.player.health / 100)
        pygame.draw.rect(health_bar, (0, 255, 0), (0, 0, filled_width, 20))
        screen.blit(health_bar, (10, 70))

        # Заполненность
        capacity_bar = pygame.Surface((200, 20))
        capacity_bar.fill((255, 0, 0))
        filled_width = 200 * (level.player.capacity / level.player.max_capacity)
        pygame.draw.rect(capacity_bar, (0, 255, 0), (0, 0, filled_width, 20))
        screen.blit(capacity_bar, (10, 100))
        capacity_text = self.font.render(f"Мусор: {level.player.capacity}/{level.player.max_capacity}", True, (255, 255, 255))
        screen.blit(capacity_text, (220, 100))