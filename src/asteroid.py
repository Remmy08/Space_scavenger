import pygame
import random
import os

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/sprites/asteroids/asteroid_1.png").convert_alpha()
        except FileNotFoundError:
            self.image = pygame.Surface((64, 64))
            self.image.fill((128, 128, 128))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            self.rect.x = random.randint(0, screen_width)
            self.rect.y = -64
        elif side == "bottom":
            self.rect.x = random.randint(0, screen_width)
            self.rect.y = screen_height
        elif side == "left":
            self.rect.x = -64
            self.rect.y = random.randint(0, screen_height)
        else:
            self.rect.x = screen_width
            self.rect.y = random.randint(0, screen_height)
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)
        self.angle = 0
        self.rotation_speed = random.uniform(-2, 2)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        if (self.rect.right < -100 or self.rect.left > 1280 + 100 or
                self.rect.bottom < -100 or self.rect.top > 720 + 100):
            self.kill()