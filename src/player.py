import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/sprites/ship.png").convert_alpha()
        except FileNotFoundError:
            self.image = pygame.Surface((256, 256))
            self.image.fill((0, 255, 0))  # Заглушка: зелёный квадрат
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.health = 100
        self.capacity = 0
        self.max_capacity = 50

    def update(self):
        keys = pygame.key.get_pressed()  # Исправлено: keyPressed -> get_pressed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < 720:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < 1280:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)