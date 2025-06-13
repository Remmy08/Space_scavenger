import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.original_image = pygame.image.load("assets/sprites/ship.png").convert_alpha()
        except FileNotFoundError:
            self.original_image = pygame.Surface((256, 256))
            self.original_image.fill((0, 255, 0))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.health = 100
        self.capacity = 0
        self.max_capacity = 15
        self.suction_radius = 100

    def update(self, garbage_group):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed

        # Ограничение движения
        self.rect.x = max(0, min(self.rect.x + dx, 1280 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y + dy, 720 - self.rect.height))

        # Поворот корабля
        if dx != 0 or dy != 0:
            if keys[pygame.K_w] and not keys[pygame.K_s]:
                if keys[pygame.K_d] and not keys[pygame.K_a]:
                    self.angle = 315  # Вправо-вверх
                elif keys[pygame.K_a] and not keys[pygame.K_d]:
                    self.angle = 45  # Влево-вверх
                else:
                    self.angle = 0  # Вверх
            elif keys[pygame.K_s] and not keys[pygame.K_w]:
                if keys[pygame.K_d] and not keys[pygame.K_a]:
                    self.angle = 225  # Вправо-вниз
                elif keys[pygame.K_a] and not keys[pygame.K_d]:
                    self.angle = 135  # Влево-вниз
                else:
                    self.angle = 180  # Вниз
            elif keys[pygame.K_d] and not keys[pygame.K_a]:
                self.angle = 270  # Вправо
            elif keys[pygame.K_a] and not keys[pygame.K_d]:
                self.angle = 90  # Влево
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

        # Притягивание мусора
        if self.capacity < self.max_capacity:
            for garbage in garbage_group:
                dx = self.rect.centerx - garbage.rect.centerx
                dy = self.rect.centery - garbage.rect.centery
                distance = math.hypot(dx, dy)
                if distance < self.suction_radius and distance > 0:
                    garbage.rect.x += (dx / distance) * 5
                    garbage.rect.y += (dy / distance) * 5
                    if distance < 40:
                        garbage.kill()
                        self.capacity = min(self.max_capacity, self.capacity + 1)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        pygame.draw.circle(screen, (0, 0, 255), self.rect.center, self.suction_radius, 2)