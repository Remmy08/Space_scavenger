import pygame
import random
import os

class Garbage(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        garbage_files = [f for f in os.listdir("assets/sprites/garbage/") if f.startswith("garbage_")]
        if garbage_files:
            sprite_file = random.choice(garbage_files)
            self.image = pygame.image.load(f"assets/sprites/garbage/{sprite_file}").convert_alpha()
        else:
            self.image = pygame.Surface((64, 64))
            self.image.fill((255, 255, 255))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        # Появление внутри игрового поля
        self.rect.x = random.randint(0, screen_width - 64)
        self.rect.y = random.randint(0, screen_height - 64)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.angle = 0
        self.rotation_speed = random.uniform(-2, 2)

    def update(self, player):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Отражение от краёв экрана
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed_x = -self.speed_x
        if self.rect.right > 1280:
            self.rect.right = 1280
            self.speed_x = -self.speed_x
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed_y = -self.speed_y
        if self.rect.bottom > 720:
            self.rect.bottom = 720
            self.speed_y = -self.speed_y
        # Вращение
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)