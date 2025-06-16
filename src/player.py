import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, upgrades):
        super().__init__()
        try:
            self.original_image = pygame.image.load("assets/sprites/ship.png").convert_alpha()
            print("Loaded: assets/sprites/ship.png")
        except FileNotFoundError:
            self.original_image = pygame.Surface((256, 256))
            self.original_image.fill((0, 255, 0))
            print("Failed to load: assets/sprites/ship.png")
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = upgrades.get("speed", 5.0)
        self.durability = upgrades.get("durability", 3)
        self.max_durability = self.durability  # Для UI
        self.unloading_speed = upgrades.get("unloading_speed", 3)  # Мусор/сек
        self.collection_radius = upgrades.get("collection_radius", 100)
        self.max_capacity = upgrades.get("capacity", 10)
        self.capacity = 0
        self.angle = 0
        self.unloading_timer = 0

    def update(self, level, garbage_group, unload_zone):
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

        self.rect.x = max(0, min(self.rect.x + dx, 1920 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y + dy, 1080 - self.rect.height))

        if dx != 0 or dy != 0:
            if keys[pygame.K_w] and not keys[pygame.K_s]:
                if keys[pygame.K_d] and not keys[pygame.K_a]:
                    self.angle = 315
                elif keys[pygame.K_a] and not keys[pygame.K_d]:
                    self.angle = 45
                else:
                    self.angle = 0
            elif keys[pygame.K_s] and not keys[pygame.K_w]:
                if keys[pygame.K_d] and not keys[pygame.K_a]:
                    self.angle = 225
                elif keys[pygame.K_a] and not keys[pygame.K_d]:
                    self.angle = 135
                else:
                    self.angle = 180
            elif keys[pygame.K_d] and not keys[pygame.K_a]:
                self.angle = 270
            elif keys[pygame.K_a] and not keys[pygame.K_d]:
                self.angle = 90
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

        if self.capacity < self.max_capacity:
            for garbage in garbage_group:
                dx = self.rect.centerx - garbage.rect.centerx
                dy = self.rect.centery - garbage.rect.centery
                distance = math.hypot(dx, dy)
                if distance < self.collection_radius and distance > 0:
                    garbage.rect.x += (dx / distance) * 5
                    garbage.rect.y += (dy / distance) * 5
                    if distance < 40:
                        garbage.kill()
                        self.capacity = min(self.max_capacity, self.capacity + 1)
                        print(f"Собран мусор: capacity={self.capacity}/{self.max_capacity}")

        if self.capacity > 0 and pygame.sprite.collide_rect(self, unload_zone):
            self.unloading_timer += 1000 / 60  # Дельта времени в мс (при 60 FPS)
            unload_amount = (self.unloading_speed * self.unloading_timer) // 1000
            if unload_amount >= 1:
                self.capacity = max(0, self.capacity - int(unload_amount))
                level.add_balance(int(unload_amount))  # Добавляем выгруженный мусор в баланс
                self.unloading_timer -= (int(unload_amount) * 1000) / self.unloading_speed
                print(f"Выгрузка: unload_amount={unload_amount}, capacity={self.capacity}, balance={level.balance}")
        else:
            self.unloading_timer = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        pygame.draw.circle(screen, (0, 0, 255), (int(self.rect.centerx), int(self.rect.centery)), int(self.collection_radius), 2)