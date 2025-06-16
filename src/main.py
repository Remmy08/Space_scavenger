
import sys
import pygame
from player import Player
from garbage import Garbage
from asteroid import Asteroid
from ui import UI
from level import Level
from menu import Menu
import os
import json

# Инициализация Pygame
try:
    pygame.init()
    BASE_WIDTH, BASE_HEIGHT = 1920, 1080
    screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT))
    pygame.display.set_caption("Космический Мусорщик")
    clock = pygame.time.Clock()
    FPS = 60
except Exception as e:
    print(f"Ошибка инициализации Pygame: {e}", file=sys.stderr)
    input("Нажмите Enter для выхода...")
    sys.exit(1)

def main():
    menu = Menu(BASE_WIDTH, BASE_HEIGHT)
    game_objects = None
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                print("Получено событие QUIT, завершение программы...")
                running = False
            if event.type == pygame.KEYDOWN:
                if menu.state == "game" and event.key == pygame.K_p:
                    print("Нажата клавиша P, переход в паузу...")
                    menu.state = "pause"
                    menu.init_pause_menu()
                elif menu.state == "pause" and event.key == pygame.K_p:
                    print("Нажата клавиша P, возврат в игру...")
                    menu.state = "game"
            if event.type == pygame.USEREVENT + 1 and menu.state == "game" and game_objects:
                print(f"Попытка спавна мусора. Текущее количество: {len(game_objects['garbage_group'])}, max_garbage: {menu.max_garbage}")
                if len(game_objects["garbage_group"]) < menu.max_garbage:
                    game_objects["garbage_group"].add(Garbage(BASE_WIDTH, BASE_HEIGHT, menu.current_level))
            if event.type == pygame.USEREVENT + 2 and menu.state == "game" and game_objects:
                print(f"Попытка спавна астероида. Текущее количество: {len(game_objects['asteroid_group'])}, max: {2 + (menu.current_level - 1)}")
                if len(game_objects["asteroid_group"]) < 2 + (menu.current_level - 1):
                    game_objects["asteroid_group"].add(Asteroid(BASE_WIDTH, BASE_HEIGHT, menu.current_level, menu.asteroid_speed))

        if menu.state == "game":
            print(f"Состояние игры: game_objects = {game_objects}")
            if not game_objects:
                print("Инициализация game_objects...")
                try:
                    player = Player(BASE_WIDTH // 2, BASE_HEIGHT // 2)
                    garbage_group = pygame.sprite.Group()
                    asteroid_group = pygame.sprite.Group()
                    level = Level(player, garbage_group, asteroid_group, menu.current_level)
                    ui = UI()
                    show_hitboxes = False
                    try:
                        background = pygame.image.load("assets/sprites/background.png").convert()
                        print("Загружено: assets/sprites/background.png")
                    except FileNotFoundError:
                        background = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
                        background.fill((0, 0, 0))
                        print("Не удалось загрузить: assets/sprites/background.png")
                    for _ in range(5 + (menu.current_level - 1) * 2):
                        garbage_group.add(Garbage(BASE_WIDTH, BASE_HEIGHT, menu.current_level))
                    garbage_spawn_timer = pygame.USEREVENT + 1
                    pygame.time.set_timer(garbage_spawn_timer, int(menu.garbage_spawn_timer))
                    asteroid_spawn_timer = pygame.USEREVENT + 2
                    pygame.time.set_timer(asteroid_spawn_timer, int(menu.asteroid_spawn_timer))
                    game_objects = {
                        "player": player,
                        "garbage_group": garbage_group,
                        "asteroid_group": asteroid_group,
                        "level": level,
                        "ui": ui,
                        "show_hitboxes": show_hitboxes,
                        "background": background,
                        "garbage_spawn_timer": garbage_spawn_timer,
                        "asteroid_spawn_timer": asteroid_spawn_timer
                    }
                    print("game_objects инициализирован: ", game_objects)
                except Exception as e:
                    print(f"Ошибка инициализации game_objects: {e}")
                    game_objects = None

            if game_objects:
                print(f"Обновление объектов игры... Время: {menu.level_time}, Загрязнение: {game_objects['level'].pollution}, Здоровье: {game_objects['player'].health}")
                game_objects["player"].update(game_objects["garbage_group"])
                game_objects["garbage_group"].update(game_objects["player"])
                game_objects["asteroid_group"].update()
                game_objects["level"].update(menu.level_time, menu)
                menu.level_time += 1000 / FPS  # Увеличиваем время для бесконечного режима

                asteroid_collisions = pygame.sprite.spritecollide(game_objects["player"], game_objects["asteroid_group"], False)
                for asteroid in asteroid_collisions:
                    game_objects["player"].health = max(0, game_objects["player"].health - 10 * (1 + (menu.current_level - 1) * 0.2))
                    asteroid.kill()

                if game_objects["level"].pollution >= 100 or game_objects["player"].health <= 0:
                    print(f"Условие завершения: pollution={game_objects['level'].pollution}, health={game_objects['player'].health}")
                    save_data = menu.saves.get(menu.selected_account, {"balance": 0, "best_time": 0})
                    save_data["balance"] += game_objects["level"].balance
                    if menu.level_time > save_data["best_time"]:
                        save_data["best_time"] = menu.level_time
                    menu.save_game(menu.selected_account, save_data["balance"], save_data["best_time"], menu.music_volume, menu.sound_volume)
                    print(f"Баланс сохранён при проигрыше: {save_data['balance']}, время: {save_data['best_time']}")
                    menu.init_mission_failed()
                    game_objects = None
                    continue
                elif game_objects["level"].player.capacity >= game_objects["level"].player.max_capacity and pygame.sprite.collide_rect(game_objects["level"].player, game_objects["level"].unload_zone):
                    game_objects["level"].add_balance(1)

                screen.blit(game_objects["background"], (0, 0))
                game_objects["level"].unload_zone.draw(screen)
                game_objects["garbage_group"].draw(screen)
                game_objects["asteroid_group"].draw(screen)
                game_objects["player"].draw(screen)
                if game_objects["show_hitboxes"]:
                    game_objects["player"].draw_hitbox(screen)
                    game_objects["level"].unload_zone.draw_hitbox(screen)
                    for garbage in game_objects["garbage_group"]:
                        garbage.draw_hitbox(screen)
                    for asteroid in game_objects["asteroid_group"]:
                        asteroid.draw_hitbox(screen)
                game_objects["ui"].draw(screen, game_objects["level"])
        else:
            print(f"Обновление меню, состояние: {menu.state}")
            new_state = menu.update(mouse_pos, mouse_pressed, events)
            if new_state is None:
                print("menu.update вернул None, пропускаем рендеринг...")
                continue
            menu.draw(screen)
            if menu.state == "main" and game_objects:  # Сохраняем баланс при выходе в главное меню
                save_data = menu.saves.get(menu.selected_account, {"balance": 0, "best_time": 0})
                save_data["balance"] += game_objects["level"].balance
                if menu.level_time > save_data["best_time"]:
                    save_data["best_time"] = menu.level_time
                menu.save_game(menu.selected_account, save_data["balance"], save_data["best_time"], menu.music_volume, menu.sound_volume)
                print(f"Баланс сохранён при выходе в главное меню: {save_data['balance']}, время: {save_data['best_time']}")
                game_objects = None

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ошибка в основном цикле: {e}", file=sys.stderr)
        input("Нажмите Enter для выхода...")
        pygame.quit()
        sys.exit(1)
