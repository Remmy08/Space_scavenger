import pygame
import random
import os

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, level_num, speed):
        super().__init__()
        try:
            self.original_image = pygame.image.load("assets/sprites/asteroids/asteroid_1.png").convert_alpha()
            print("Loaded: assets/sprites/asteroids/asteroid_1.png")
        except FileNotFoundError:
            self.original_image = pygame.Surface((64, 64))
            self.original_image.fill((128, 128, 128))
            print("Failed to load: assets/sprites/asteroids/asteroid_1.png")
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 64)
        self.rect.y = random.randint(0, screen_height - 64)
        self.speed_x = random.choice([-1, 1]) * random.uniform(0.5 * speed, speed)
        self.speed_y = random.choice([-1, 1]) * random.uniform(0.5 * speed, speed)
        self.angle = 0
        self.rotation_speed = random.uniform(-2, 2)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        if (self.rect.right < -100 or self.rect.left > 1920 + 100 or
                self.rect.bottom < -100 or self.rect.top > 1080 + 100):
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)