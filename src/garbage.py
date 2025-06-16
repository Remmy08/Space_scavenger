import pygame
import random
import os

class Garbage(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, level_num):
        super().__init__()
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
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 64)
        self.rect.y = random.randint(0, screen_height - 64)
        self.speed_x = random.uniform(-2, 2) * (1 + level_num * 0.2)
        self.speed_y = random.uniform(-2, 2) * (1 + level_num * 0.2)
        self.angle = 0
        self.rotation_speed = random.uniform(-2, 2)

    def update(self, player):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed_x = -self.speed_x
        if self.rect.right > 1920:
            self.rect.right = 1920
            self.speed_x = -self.speed_x
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed_y = -self.speed_y
        if self.rect.bottom > 1080:
            self.rect.bottom = 1080
            self.speed_y = -self.speed_y
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)