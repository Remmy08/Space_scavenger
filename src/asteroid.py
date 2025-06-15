import pygame
import random
import os

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, scale_factor, level_num):
        super().__init__()
        self.scale_factor = scale_factor
        try:
            self.original_image = pygame.image.load("assets/sprites/asteroids/asteroid_1.png").convert_alpha()
            print("Loaded: assets/sprites/asteroids/asteroid_1.png")
        except FileNotFoundError:
            self.original_image = pygame.Surface((64, 64))
            self.original_image.fill((128, 128, 128))
            print("Failed to load: assets/sprites/asteroids/asteroid_1.png")
        self.image = self.original_image
        self.base_rect = self.image.get_rect()
        self.rect = self.base_rect.copy()
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            self.base_rect.x = random.randint(0, screen_width)
            self.base_rect.y = -64
        elif side == "bottom":
            self.base_rect.x = random.randint(0, screen_width)
            self.base_rect.y = screen_height
        elif side == "left":
            self.base_rect.x = -64
            self.base_rect.y = random.randint(0, screen_height)
        else:
            self.base_rect.x = screen_width
            self.base_rect.y = random.randint(0, screen_height)
        self.speed_x = random.uniform(-3, 3) * (1 + level_num * 0.3) * scale_factor  # Увеличиваем скорость
        self.speed_y = random.uniform(-3, 3) * (1 + level_num * 0.3) * scale_factor
        self.angle = 0
        self.rotation_speed = random.uniform(-2, 2)

    def update(self):
        self.base_rect.x += self.speed_x
        self.base_rect.y += self.speed_y
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.base_rect = self.image.get_rect(center=self.base_rect.center)
        self.rect = self.base_rect.copy()
        if (self.base_rect.right < -100 or self.base_rect.left > 1920 + 100 or
                self.base_rect.bottom < -100 or self.base_rect.top > 1080 + 100):
            self.kill()

    def draw(self, screen):
        scaled_img = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale_factor), int(self.image.get_height() * self.scale_factor)))
        scaled_rect = self.base_rect.copy()
        scaled_rect.x *= self.scale_factor
        scaled_rect.y *= self.scale_factor
        scaled_rect.width *= self.scale_factor
        scaled_rect.height *= scale_factor
        screen.blit(scaled_img, scaled_rect)

    def draw_hitbox(self, screen, scale_factor):
        scaled_rect = self.rect.copy()
        scaled_rect.x *= scale_factor
        scaled_rect.y *= scale_factor
        scaled_rect.width *= scale_factor
        scaled_rect.height *= scale_factor
        pygame.draw.rect(screen, (255, 0, 0), scaled_rect, 2)