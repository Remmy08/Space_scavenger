import pygame
from player import Player
from garbage import Garbage
from asteroid import Asteroid
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
    level = Level(player, garbage_group, asteroid_group)
    ui = UI()
    show_hitboxes = False

    # Загрузка фона
    try:
        background = pygame.image.load("assets/sprites/background.png").convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except FileNotFoundError:
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill((0, 0, 0))  # Чёрный фон

    # Начальная генерация мусора
    for _ in range(10):
        garbage_group.add(Garbage(SCREEN_WIDTH, SCREEN_HEIGHT))

    # Таймеры для генерации
    garbage_spawn_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(garbage_spawn_timer, 500)  # 2 мусора каждые 0.5 секунды
    asteroid_spawn_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(asteroid_spawn_timer, 5000)  # Астероид каждые 5 секунд

    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_F1:
                    show_hitboxes = not show_hitboxes
            if event.type == garbage_spawn_timer and len(garbage_group) < 10:
                garbage_group.add(Garbage(SCREEN_WIDTH, SCREEN_HEIGHT))
                if len(garbage_group) < 10:
                    garbage_group.add(Garbage(SCREEN_WIDTH, SCREEN_HEIGHT))
            if event.type == asteroid_spawn_timer and len(asteroid_group) < 5:
                asteroid_group.add(Asteroid(SCREEN_WIDTH, SCREEN_HEIGHT))

        # Обновление
        player.update(garbage_group)
        garbage_group.update(player)
        asteroid_group.update()
        level.update()

        # Проверка столкновений с астероидами
        asteroid_collisions = pygame.sprite.spritecollide(player, asteroid_group, False)
        for asteroid in asteroid_collisions:
            player.health = max(0, player.health - 10)
            asteroid.kill()

        # Отрисовка
        screen.blit(background, (0, 0))
        level.unload_zone.draw(screen)
        garbage_group.draw(screen)
        asteroid_group.draw(screen)
        player.draw(screen)
        if show_hitboxes:
            player.draw_hitbox(screen)
            level.unload_zone.draw_hitbox(screen)
            for garbage in garbage_group:
                pygame.draw.rect(screen, (255, 0, 0), garbage.rect, 2)
            for asteroid in asteroid_group:
                pygame.draw.rect(screen, (255, 0, 0), asteroid.rect, 2)
        ui.draw(screen, level)
        pygame.display.flip()

        # Контроль FPS
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()