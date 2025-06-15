import pygame
import random
import os

class Garbage(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, scale_factor, level_num):
        super().__init__()
        self.scale_factor = scale_factor
        garbage_files = [f for f in os.listdir("assets/sprites/garbage/") if f.startswith("garbage_")]
        if garbage_files:
            sprite_file = random.choice(garbage_files)
            self.original_image = pygame.image.load(f"assets/sprites/garbage/{sprite_file}").convert_alpha()
            print(f"Loaded: assets/sprites/garbage/{sprite_file}")
        else:
            self.original_image = pygame.Surface((64, 64))
            self.original_image.fill((255, 255, 255))
            print("Failed to load: garbage sprites")
        self.image = self.original_image
        self.base_rect = self.image.get_rect()
        self.rect = self.base_rect.copy()
        self.base_rect.x = random.randint(0, screen_width - 64)
        self.base_rect.y = random.randint(0, screen_height - 64)
        self.speed_x = random.uniform(-2, 2) * (1 + level_num * 0.2) * scale_factor  # Увеличиваем скорость
        self.speed_y = random.uniform(-2, 2) * (1 + level_num * 0.2) * scale_factor
        self.angle = 0
        self.rotation_speed = random.uniform(-2, 2)

    def update(self, player):
        self.base_rect.x += self.speed_x
        self.base_rect.y += self.speed_y
        if self.base_rect.left < 0:
            self.base_rect.left = 0
            self.speed_x = -self.speed_x
        if self.base_rect.right > 1920:
            self.base_rect.right = 1920
            self.speed_x = -self.speed_x
        if self.base_rect.top < 0:
            self.base_rect.top = 0
            self.speed_y = -self.speed_y
        if self.base_rect.bottom > 1080:
            self.base_rect.bottom = 1080
            self.speed_y = -self.speed_y
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.base_rect = self.image.get_rect(center=self.base_rect.center)
        self.rect = self.base_rect.copy()

    def draw(self, screen):
        scaled_img = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale_factor), int(self.image.get_height() * self.scale_factor)))
        scaled_rect = self.base_rect.copy()
        scaled_rect.x *= self.scale_factor
        scaled_rect.y *= self.scale_factor
        scaled_rect.width *= self.scale_factor
        scaled_rect.height *= self.scale_factor
        screen.blit(scaled_img, scaled_rect)

    def draw_hitbox(self, screen, scale_factor):
        scaled_rect = self.rect.copy()
        scaled_rect.x *= scale_factor
        scaled_rect.y *= scale_factor
        scaled_rect.width *= scale_factor
        scaled_rect.height *= scale_factor
        pygame.draw.rect(screen, (255, 0, 0), scaled_rect, 2)