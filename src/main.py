import pygame
from player import Player
from garbage import Garbage
from asteroid import Asteroid
from ui import UI
from level import Level
from menu import Menu
import os
import json
import sys

# Инициализация Pygame
pygame.init()
BASE_WIDTH, BASE_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Космический Мусорщик")
clock = pygame.time.Clock()
FPS = 60

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
                menu.font = pygame.font.Font("assets/fonts/pixel.ttf", int(24 * menu.scale_factor))
                menu.background = pygame.transform.scale(menu.background, (menu.screen_width, menu.screen_height))
                menu.init_main_menu()
            if event.type == pygame.USEREVENT + 1 and menu.state == "game" and game_objects:
                if len(game_objects["garbage_group"]) < 5 + menu.current_level * 2:
                    game_objects["garbage_group"].add(Garbage(BASE_WIDTH, BASE_HEIGHT, menu.scale_factor, menu.current_level))
            if event.type == pygame.USEREVENT + 2 and menu.state == "game" and game_objects:
                if len(game_objects["asteroid_group"]) < 2 + menu.current_level:
                    game_objects["asteroid_group"].add(Asteroid(BASE_WIDTH, BASE_HEIGHT, menu.scale_factor, menu.current_level))

        if menu.state == "game":
            if not game_objects:
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
                for _ in range(5 + menu.current_level):
                    garbage_group.add(Garbage(BASE_WIDTH, BASE_HEIGHT, menu.scale_factor, menu.current_level))
                garbage_spawn_timer = pygame.USEREVENT + 1
                pygame.time.set_timer(garbage_spawn_timer, max(1000, 2000 - menu.current_level * 200))
                asteroid_spawn_timer = pygame.USEREVENT + 2
                pygame.time.set_timer(asteroid_spawn_timer, max(3000, 5000 - menu.current_level * 500))
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

            scaled_width = int(BASE_WIDTH * menu.scale_factor)
            scaled_height = int(BASE_HEIGHT * menu.scale_factor)
            game_objects["player"].update(game_objects["garbage_group"])
            game_objects["garbage_group"].update(game_objects["player"])
            game_objects["asteroid_group"].update()
            game_objects["level"].update()

            asteroid_collisions = pygame.sprite.spritecollide(game_objects["player"], game_objects["asteroid_group"], False)
            for asteroid in asteroid_collisions:
                game_objects["player"].health = max(0, game_objects["player"].health - 10 * (1 + (menu.current_level - 1) * 0.2))
                asteroid.kill()

            if game_objects["level"].time_remaining <= 0 or game_objects["level"].pollution >= 100 or game_objects["player"].health <= 0:
                if game_objects["level"].player.capacity >= game_objects["level"].player.max_capacity:
                    game_objects["level"].add_score(100 * menu.current_level)
                menu.save_game(menu.selected_account, min(12, menu.current_level + 1), game_objects["level"].score, menu.music_volume, menu.sound_volume)
                menu.state = "main"
                game_objects = None
                menu.init_main_menu()
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
            menu.update(mouse_pos, mouse_pressed)
            menu.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()