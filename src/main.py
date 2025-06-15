import sys

try:
    import pygame
    from player import Player
    from garbage import Garbage
    from asteroid import Asteroid
    from ui import UI
    from level import Level
    from menu import Menu
    import os
    import json
except Exception as e:
    print(f"Ошибка при импорте модулей: {e}", file=sys.stderr)
    input("Нажмите Enter для выхода...")
    sys.exit(1)

# Инициализация Pygame
try:
    pygame.init()
    BASE_WIDTH, BASE_HEIGHT = 1920, 1080
    screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if menu.state == "game" and event.key == pygame.K_ESCAPE:
                        menu.state = "pause"
                        menu.init_pause_menu()
                    elif menu.state == "pause" and event.key == pygame.K_ESCAPE:
                        menu.state = "game"
                if event.type == pygame.VIDEORESIZE and menu.state != "game":
                    menu.screen_width, menu.screen_height = event.w, event.h
                    menu.scale_factor = min(menu.screen_width / menu.base_width, menu.screen_height / menu.base_height)
                    menu.font = pygame.font.Font("assets/fonts/pixel.ttf", int(36 * menu.scale_factor))
                    menu.background = pygame.transform.scale(menu.background, (menu.screen_width, menu.screen_height))
                    if menu.state == "main":
                        menu.init_main_menu()
                    elif menu.state == "load":
                        menu.init_load_menu()
                    elif menu.state == "account":
                        menu.init_account_menu()
                    elif menu.state == "settings":
                        menu.init_settings()
                    elif menu.state == "pause":
                        menu.init_pause_menu()
                    elif menu.state == "mission_failed":
                        menu.init_mission_failed()
                    elif menu.state == "mission_passed":
                        menu.init_mission_passed()
                if event.type == pygame.USEREVENT + 1 and menu.state == "game" and game_objects:
                    print(f"Попытка спавна мусора. Текущее количество: {len(game_objects['garbage_group'])}, max_garbage: {menu.max_garbage}")
                    if len(game_objects["garbage_group"]) < menu.max_garbage:
                        game_objects["garbage_group"].add(Garbage(BASE_WIDTH, BASE_HEIGHT, menu.scale_factor, menu.current_level))
                if event.type == pygame.USEREVENT + 2 and menu.state == "game" and game_objects:
                    print(f"Попытка спавна астероида. Текущее количество: {len(game_objects['asteroid_group'])}, max: {2 + (menu.current_level - 1)}")
                    if len(game_objects["asteroid_group"]) < 2 + (menu.current_level - 1):
                        game_objects["asteroid_group"].add(Asteroid(BASE_WIDTH, BASE_HEIGHT, menu.scale_factor, menu.current_level, menu.asteroid_speed))

            if menu.state == "game":
                print(f"Состояние игры: game_objects = {game_objects}")
                if not game_objects:
                    print("Инициализация game_objects...")
                    try:
                        player = Player(BASE_WIDTH // 2, BASE_HEIGHT // 2, menu.scale_factor)
                        garbage_group = pygame.sprite.Group()
                        asteroid_group = pygame.sprite.Group()
                        level = Level(player, garbage_group, asteroid_group, menu.scale_factor, menu.current_level)
                        ui = UI(menu.scale_factor)
                        show_hitboxes = False
                        try:
                            background = pygame.image.load("assets/sprites/background.png").convert()
                            print("Loaded: assets/sprites/background.png")
                        except FileNotFoundError:
                            background = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
                            background.fill((0, 0, 0))
                            print("Failed to load: assets/sprites/background.png")
                        for _ in range(5 + (menu.current_level - 1) * 2):
                            garbage_group.add(Garbage(BASE_WIDTH, BASE_HEIGHT, menu.scale_factor, menu.current_level))
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
                    scaled_width = int(BASE_WIDTH * menu.scale_factor)
                    scaled_height = int(BASE_HEIGHT * menu.scale_factor)
                    print("Обновление объектов игры...")
                    print(f"Текущее время: {menu.level_time}, Загрязнение: {game_objects['level'].pollution}, Здоровье: {game_objects['player'].health}")
                    game_objects["player"].update(game_objects["garbage_group"])
                    game_objects["garbage_group"].update(game_objects["player"])
                    game_objects["asteroid_group"].update()
                    game_objects["level"].update(menu.level_time)
                    menu.level_time -= 1000 / FPS

                    asteroid_collisions = pygame.sprite.spritecollide(game_objects["player"], game_objects["asteroid_group"], False)
                    for asteroid in asteroid_collisions:
                        game_objects["player"].health = max(0, game_objects["player"].health - 10 * (1 + (menu.current_level - 1) * 0.2))
                        asteroid.kill()

                    if menu.level_time <= 0 or game_objects["level"].pollution >= 100 * menu.pollution_factor or game_objects["player"].health <= 0:
                        print(f"Условие завершения: time={menu.level_time}, pollution={game_objects['level'].pollution}, health={game_objects['player'].health}")
                        save_data = menu.saves.get(menu.selected_account, {"level": 1, "score": 0})
                        if menu.level_time <= 0 and game_objects["level"].pollution < 100 * menu.pollution_factor and game_objects["player"].health > 0:
                            menu.init_mission_passed()
                            if menu.current_level == save_data["level"]:
                                save_data["level"] += 1
                                menu.save_game(menu.selected_account, save_data["level"], save_data["score"], menu.music_volume, menu.sound_volume)
                        else:
                            menu.init_mission_failed()
                            if menu.current_level == save_data["level"]:
                                menu.save_game(menu.selected_account, save_data["level"], save_data["score"], menu.music_volume, menu.sound_volume)
                        game_objects = None
                        continue  # Пропускаем оставшуюся часть цикла после обнуления
                    elif game_objects["level"].player.capacity >= game_objects["level"].player.max_capacity and pygame.sprite.collide_rect(game_objects["level"].player, game_objects["level"].unload_zone):
                        game_objects["level"].add_score(50 * menu.current_level)

                    scaled_background = pygame.transform.scale(game_objects["background"], (scaled_width, scaled_height))
                    screen.blit(scaled_background, (0, 0))
                    game_objects["level"].unload_zone.draw(screen, menu.scale_factor)
                    game_objects["garbage_group"].draw(screen)
                    game_objects["asteroid_group"].draw(screen)
                    game_objects["player"].draw(screen, menu.scale_factor)
                    if game_objects["show_hitboxes"]:
                        game_objects["player"].draw_hitbox(screen, menu.scale_factor)
                        game_objects["level"].unload_zone.draw_hitbox(screen, menu.scale_factor)
                        for garbage in game_objects["garbage_group"]:
                            garbage.draw_hitbox(screen, menu.scale_factor)
                        for asteroid in game_objects["asteroid_group"]:
                            asteroid.draw_hitbox(screen, menu.scale_factor)
                    game_objects["ui"].draw(screen, game_objects["level"], menu.scale_factor)
                else:
                    print("game_objects не инициализирован, возвращаемся в меню...")
                    menu.state = "main"
                    menu.init_main_menu()
            else:
                menu.update(mouse_pos, mouse_pressed)
                menu.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ошибка в основном цикле: {e}", file=sys.stderr)
        input("Нажмите Enter для выхода...")
        sys.exit(1)