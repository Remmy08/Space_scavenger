import pygame

class Level:
    def __init__(self, player, garbage_group):
        self.player = player  # Сохраняем объект игрока
        self.garbage_group = garbage_group  # Сохраняем группу мусора
        self.pollution = 0
        self.score = 0
        self.time_remaining = 120 * 1000  # 2 минуты в миллисекундах

    def update(self):
        self.time_remaining -= 1000 / 60  # Уменьшаем время (60 FPS)
        # Загрязнение зависит от количества мусора
        self.pollution += 0.01 * len(self.garbage_group)
        if self.time_remaining <= 0 or self.pollution >= 100:
            print("Игра окончена!")  # Заглушка для проигрыша
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def add_score(self, points):
        self.score += points

    def decrease_pollution(self, amount):
        self.pollution = max(0, self.pollution - amount)