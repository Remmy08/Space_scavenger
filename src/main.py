import pygame
from player import Player
from garbage import Garbage
from ui import UI
from level import Level

# Инициализация Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Космический Мусорщик")
clock = pygame.time.Clock()
FPS = 60

def main():
    # Создание объектов
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    garbage_group = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    level = Level(player, garbage_group)  # Передаём player и garbage_group в Level
    ui = UI()

    # Генерация мусора
    for _ in range(10):  # Начальное количество мусора
        garbage = Garbage(SCREEN_WIDTH, SCREEN_HEIGHT)
        garbage_group.add(garbage)

    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Обновление
        player.update()
        garbage_group.update()
        level.update()

        # Проверка столкновений
        collected_garbage = pygame.sprite.spritecollide(player, garbage_group, True)
        for garbage in collected_garbage:
            level.add_score(1)  # +1 очко за мусор
            level.decrease_pollution(0.1)  # Уменьшаем загрязнение
            # Добавляем новый мусор
            garbage_group.add(Garbage(SCREEN_WIDTH, SCREEN_HEIGHT))

        # Отрисовка
        screen.fill((0, 0, 0))  # Чёрный фон (космос)
        garbage_group.draw(screen)
        player.draw(screen)
        ui.draw(screen, level)
        pygame.display.flip()

        # Контроль FPS
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()