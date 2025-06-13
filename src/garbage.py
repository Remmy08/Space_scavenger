import pygame
import random
import os

class Garbage(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        # Случайный выбор спрайта мусора
        garbage_files = [f for f in os.listdir("assets/sprites/garbage/") if f.startswith("garbage_")]
        if garbage_files:
            sprite_file = random.choice(garbage_files)
            self.image = pygame.image.load(f"assets/sprites/garbage/{sprite_file}").convert_alpha()
        else:
            self.image = pygame.Surface((64, 64))
            self.image.fill((255, 255, 255))  # Заглушка: белый квадрат
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width)
        self.rect.y = random.randint(0, screen_height)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Ограничение движения за пределы экрана
        if self.rect.left < 0 or self.rect.right > 1280:
            self.speed_x = -self.speed_x
        if self.rect.top < 0 or self.rect.bottom > 720:
            self.speed_y = -self.speed_y