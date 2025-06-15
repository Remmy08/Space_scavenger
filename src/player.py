import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale_factor):
        super().__init__()
        self.scale_factor = scale_factor
        try:
            self.original_image = pygame.image.load("assets/sprites/ship.png").convert_alpha()
            print("Loaded: assets/sprites/ship.png")
        except FileNotFoundError:
            self.original_image = pygame.Surface((256, 256))
            self.original_image.fill((0, 255, 0))
            print("Failed to load: assets/sprites/ship.png")
        self.image = self.original_image
        self.base_rect = self.image.get_rect(center=(x, y))
        self.rect = self.base_rect.copy()  # Для collide_rect
        self.speed = 5 * scale_factor
        self.health = 100
        self.capacity = 0
        self.max_capacity = 15
        self.suction_radius = 100 * scale_factor
        self.angle = 0

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

        # Ограничение движения с учётом масштабирования
        self.base_rect.x = max(0, min(self.base_rect.x + dx, 1920 - self.base_rect.width))
        self.base_rect.y = max(0, min(self.base_rect.y + dy, 1080 - self.base_rect.height))
        self.rect = self.base_rect.copy()

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
            self.base_rect = self.image.get_rect(center=self.base_rect.center)
            self.rect = self.base_rect.copy()

        # Притягивание мусора
        if self.capacity < self.max_capacity:
            for garbage in garbage_group:
                dx = self.base_rect.centerx - garbage.base_rect.centerx
                dy = self.base_rect.centery - garbage.base_rect.centery
                distance = math.hypot(dx, dy)
                if distance < self.suction_radius and distance > 0:
                    garbage.base_rect.x += (dx / distance) * 5 * self.scale_factor
                    garbage.base_rect.y += (dy / distance) * 5 * self.scale_factor
                    if distance < 40 * self.scale_factor:
                        garbage.kill()
                        self.capacity = min(self.max_capacity, self.capacity + 1)

    def draw(self, screen, scale_factor):
        scaled_img = pygame.transform.scale(self.image, (int(self.image.get_width() * scale_factor), int(self.image.get_height() * scale_factor)))
        scaled_rect = self.base_rect.copy()
        scaled_rect.x *= scale_factor
        scaled_rect.y *= scale_factor
        scaled_rect.width *= scale_factor
        scaled_rect.height *= scale_factor
        screen.blit(scaled_img, scaled_rect)

    def draw_hitbox(self, screen, scale_factor):
        scaled_rect = self.rect.copy()
        scaled_rect.x *= scale_factor
        scaled_rect.y *= scale_factor
        scaled_rect.width *= scale_factor
        scaled_rect.height *= scale_factor
        pygame.draw.rect(screen, (255, 0, 0), scaled_rect, 2)
        pygame.draw.circle(screen, (0, 0, 255), (int(scaled_rect.centerx), int(scaled_rect.centery)), int(self.suction_radius / scale_factor), 2)