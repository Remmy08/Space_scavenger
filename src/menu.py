import pygame
import os
import json

print("Инициализация модуля menu...")

class Button:
    def __init__(self, x, y, normal_img, hover_img, text, font, action):
        print(f"Создание кнопки с координатами ({x}, {y}) и текстом {text}...")
        self.rect = normal_img.get_rect(topleft=(x, y))
        self.normal_img = normal_img
        self.hover_img = hover_img
        self.image = normal_img
        if isinstance(text, str):
            self.text = font.render(text.upper(), True, (68, 36, 52)) if text else None
        else:
            self.text = text
        self.text_rect = self.text.get_rect(center=self.rect.center) if self.text else None
        self.action = action
        self.is_hovered = False
        self.was_pressed = False
        pygame.mixer.init()
        print("Инициализация звука кнопки...")
        try:
            self.click_sound = pygame.mixer.Sound("assets/sounds/button_click.wav")
            self.click_sound.set_volume(1.0)
            print("Звук кнопки загружен.")
        except FileNotFoundError:
            print("Не удалось загрузить: assets/sounds/button_click.wav")
        print("Кнопка создана.")

    def update(self, mouse_pos, mouse_pressed):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        current_pressed = self.is_hovered and mouse_pressed[0]
        if self.is_hovered:
            self.image = self.hover_img
        else:
            self.image = self.normal_img
        if current_pressed and not self.was_pressed:
            self.was_pressed = True
        elif not current_pressed and self.was_pressed:
            self.was_pressed = False
            if self.is_hovered:
                if hasattr(self, 'click_sound'):
                    self.click_sound.play()
                return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.text:
            screen.blit(self.text, self.text_rect)

class Menu:
    def __init__(self, screen_width, screen_height):
        print(f"Инициализация Menu с размерами {screen_width}x{screen_height}...")
        self.screen_width, self.screen_height = screen_width, screen_height
        print("Загрузка шрифта...")
        try:
            self.font = pygame.font.Font("assets/fonts/pixel.ttf", 36)
            print("Шрифт загружен.")
        except FileNotFoundError:
            print("Не удалось загрузить: assets/fonts/pixel.ttf")
            self.font = pygame.font.SysFont("arial", 36)
        try:
            print("Попытка загрузки фона...")
            self.background = pygame.image.load("assets/sprites/menu_background.png").convert()
            print("Фон загружен.")
        except FileNotFoundError:
            print("Ошибка загрузки фона, создание дефолтного фона...")
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((0, 0, 0))
            print("Дефолтный фон создан.")
        try:
            print("Попытка загрузки кнопок...")
            self.button_normal = pygame.image.load("assets/sprites/ui/button_normal.png").convert_alpha()
            self.button_hover = pygame.image.load("assets/sprites/ui/button_hover.png").convert_alpha()
            print("Кнопки загружены.")
        except FileNotFoundError:
            print("Ошибка загрузки кнопок, создание дефолтных...")
            self.button_normal = pygame.Surface((300, 60))
            self.button_hover = pygame.Surface((300, 60))
            self.button_normal.fill((100, 100, 100))
            self.button_hover.fill((150, 150, 150))
            print("Дефолтные кнопки созданы.")
        try:
            print("Попытка загрузки панели настроек...")
            self.settings_panel = pygame.image.load("assets/sprites/ui/settings_panel.png").convert_alpha()
            self.settings_panel = pygame.transform.scale(self.settings_panel, (900, 600))
            print("Панель настроек загружена.")
        except FileNotFoundError:
            print("Ошибка загрузки панели настроек, создание дефолтной...")
            self.settings_panel = pygame.Surface((900, 600))
            self.settings_panel.fill((50, 50, 50))
            print("Дефолтная панель создана.")
        try:
            print("Попытка загрузки музыки...")
            pygame.mixer.music.load("assets/sounds/menu_music.mp3")
            pygame.mixer.music.set_volume(100.0 / 100.0)
            pygame.mixer.music.play(-1)
            print("Музыка загружена и запущена.")
        except FileNotFoundError:
            print("Ошибка загрузки музыки...")
            print("Не удалось загрузить: assets/sounds/menu_music.mp3")
        try:
            print("Попытка загрузки спрайтов громкости...")
            self.volume_decrease = pygame.image.load("assets/sprites/ui/volume_decrease.png").convert_alpha()
            self.volume_decrease_hover = pygame.image.load("assets/sprites/ui/volume_decrease_hover.png").convert_alpha()
            self.volume_display = pygame.image.load("assets/sprites/ui/volume_display.png").convert_alpha()
            self.volume_increase = pygame.image.load("assets/sprites/ui/volume_increase.png").convert_alpha()
            self.volume_increase_hover = pygame.image.load("assets/sprites/ui/volume_increase_hover.png").convert_alpha()
            print("Спрайты громкости загружены.")
        except FileNotFoundError:
            print("Ошибка загрузки спрайтов громкости, создание дефолтных...")
            self.volume_decrease = pygame.Surface((60, 60))
            self.volume_decrease_hover = pygame.Surface((60, 60))
            self.volume_display = pygame.Surface((165, 60))
            self.volume_increase = pygame.Surface((60, 60))
            self.volume_increase_hover = pygame.Surface((60, 60))
            self.volume_decrease.fill((100, 100, 100))
            self.volume_decrease_hover.fill((150, 150, 150))
            self.volume_display.fill((150, 150, 150))
            self.volume_increase.fill((100, 100, 100))
            self.volume_increase_hover.fill((150, 150, 150))
            print("Дефолтные спрайты громкости созданы.")
        self.state = "main"
        self.buttons = []
        self.fullscreen = False
        self.music_volume = 100.0
        self.sound_volume = 100.0
        self.selected_account = None
        self.save_dir = "saves"
        self.settings_file = "settings.json"
        self.input_text = ""  # Текст для ввода имени аккаунта
        self.max_input_length = 15  # Максимальная длина имени
        print("Создание директории сохранений...")
        os.makedirs(self.save_dir, exist_ok=True)
        print("Директория сохранений создана или существует.")
        print("Загрузка настроек...")
        self.load_settings()
        print("Настройки загружены.")
        print("Загрузка сохранений...")
        self.load_saves()
        print("Сохранения загружены.")
        print("Инициализация главного меню...")
        self.init_main_menu()
        print("Menu инициализирован.")

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                self.music_volume = settings.get("music_volume", 100.0)
                self.sound_volume = settings.get("sound_volume", 100.0)
                self.fullscreen = settings.get("fullscreen", False)
                pygame.mixer.music.set_volume(self.music_volume / 100.0)
                print(f"Настройки загружены: music_volume={self.music_volume}, sound_volume={self.sound_volume}, fullscreen={self.fullscreen}")
        else:
            self.save_settings()

    def save_settings(self):
        settings = {
            "music_volume": self.music_volume,
            "sound_volume": self.sound_volume,
            "fullscreen": self.fullscreen
        }
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)
        print("Настройки сохранены.")

    def load_saves(self):
        self.saves = {}
        index = 0
        while True:
            save_file = os.path.join(self.save_dir, f"save_{index}.json")
            if os.path.exists(save_file):
                with open(save_file, 'r') as f:
                    save_data = json.load(f)
                    account_name = save_data.get("name", f"Аккаунт {index + 1}")
                    self.saves[account_name] = save_data
                print(f"Загружено сохранение: {save_file} для аккаунта {account_name}")
                index += 1
            else:
                break

    def save_game(self, account_name, balance, best_time, music_volume, sound_volume):
        save_data = {
            "name": account_name,
            "balance": balance,
            "best_time": best_time
        }
        index = 0
        existing_index = None
        while True:
            save_file = os.path.join(self.save_dir, f"save_{index}.json")
            if os.path.exists(save_file):
                with open(save_file, 'r') as f:
                    data = json.load(f)
                    if data.get("name") == account_name:
                        existing_index = index
                        break
                index += 1
            else:
                if existing_index is None:
                    existing_index = index
                break
        save_file = os.path.join(self.save_dir, f"save_{existing_index}.json")
        with open(save_file, 'w') as f:
            json.dump(save_data, f)
        self.saves[account_name] = save_data
        print(f"Сохранение записано: {save_file} для аккаунта {account_name}")

    def init_main_menu(self):
        self.state = "main"
        self.buttons = [
            Button(self.screen_width // 2 - 150, self.screen_height // 2 - 150, self.button_normal, self.button_hover, "НОВАЯ ИГРА", self.font, lambda: self.init_new_account()),
            Button(self.screen_width // 2 - 150, self.screen_height // 2 - 50, self.button_normal, self.button_hover, "ЗАГРУЗИТЬ", self.font, lambda: self.open_load_menu()),
            Button(self.screen_width // 2 - 150, self.screen_height // 2 + 50, self.button_normal, self.button_hover, "НАСТРОЙКИ", self.font, lambda: self.open_settings()),
            Button(self.screen_width // 2 - 150, self.screen_height // 2 + 150, self.button_normal, self.button_hover, "ВЫХОД", self.font, lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)))
        ]
        print("Главное меню инициализировано.")

    def init_new_account(self):
        self.state = "new_account"
        self.input_text = ""
        panel_center_x = self.screen_width // 2 - 450
        panel_center_y = self.screen_height // 2 - 300
        self.buttons = [
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 250, self.button_normal, self.button_hover, "СОЗДАТЬ", self.font, lambda: self.create_new_game() if self.input_text.strip() else None),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 350, self.button_normal, self.button_hover, "НАЗАД", self.font, lambda: self.init_main_menu())
        ]
        self.input_text_surface = self.font.render(self.input_text.upper(), True, (255, 255, 255))
        self.input_text_rect = self.input_text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        print("Меню создания нового аккаунта инициализировано.")

    def create_new_game(self):
        account_name = self.input_text.strip()
        if account_name and account_name not in self.saves:
            self.selected_account = account_name
            save_data = {"name": account_name, "balance": 0, "best_time": 0}
            self.save_game(account_name, 0, 0, self.music_volume, self.sound_volume)
            self.init_account_menu()
            print(f"Создан новый аккаунт: {account_name}")
        else:
            print(f"Ошибка создания аккаунта: имя '{account_name}' уже существует или пустое")

    def init_load_menu(self):
        self.state = "load"
        panel_center_x = self.screen_width // 2 - 450
        panel_center_y = self.screen_height // 2 - 300
        self.buttons = []
        y_offset = 50
        for account_name in self.saves:
            self.buttons.append(
                Button(panel_center_x + (900 - 300) // 2, panel_center_y + y_offset, self.button_normal, self.button_hover,
                       account_name, self.font, lambda name=account_name: setattr(self, 'selected_account', name))
            )
            y_offset += 100
        self.buttons.extend([
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + y_offset, self.button_normal, self.button_hover,
                   "ВЫБРАТЬ", self.font, lambda: self.open_account_menu() if self.selected_account else None),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + y_offset + 100, self.button_normal, self.button_hover,
                   "УДАЛИТЬ", self.font, lambda: self.delete_account() if self.selected_account else None),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + y_offset + 200, self.button_normal, self.button_hover,
                   "НАЗАД", self.font, lambda: self.init_main_menu())
        ])
        print("Меню загрузки инициализировано.")

    def init_account_menu(self):
        self.state = "account"
        panel_center_x = self.screen_width // 2 - 450
        panel_center_y = self.screen_height // 2 - 300
        self.buttons = [
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 50, self.button_normal, self.button_hover, "ИГРАТЬ", self.font, lambda: self.start_game()),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 150, self.button_normal, self.button_hover, "УЛУЧШЕНИЯ", self.font, lambda: self.open_upgrades()),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 250, self.button_normal, self.button_hover, "ДОСТИЖЕНИЯ", self.font, lambda: self.open_achievements()),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 350, self.button_normal, self.button_hover, "НАЗАД", self.font, lambda: self.init_load_menu())
        ]
        save_data = self.saves.get(self.selected_account, {"balance": 0, "best_time": 0})
        self.balance_text = self.font.render(f"Баланс: {save_data['balance']}", True, (255, 255, 255))
        self.balance_text_rect = self.balance_text.get_rect(center=(self.screen_width // 2, panel_center_y - 100))
        minutes = int(save_data['best_time'] // 60000)
        seconds = int((save_data['best_time'] % 60000) // 1000)
        self.best_time_text = self.font.render(f"Лучшее время: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        self.best_time_text_rect = self.best_time_text.get_rect(center=(self.screen_width // 2, panel_center_y - 50))
        print("Меню аккаунта инициализировано.")

    def init_settings(self):
        self.state = "settings"
        panel_center_x = self.screen_width // 2 - 450
        panel_center_y = self.screen_height // 2 - 300
        total_width = 60 + 5 + 165 + 5 + 60
        start_x_music = panel_center_x + (900 - total_width) // 2
        start_x_sound = panel_center_x + (900 - total_width) // 2
        self.buttons = [
            Button(start_x_music, panel_center_y + 50, self.volume_decrease, self.volume_decrease_hover, "", self.font, lambda: self.adjust_music_volume(-10)),
            Button(start_x_music + 65, panel_center_y + 50, self.volume_display, self.volume_display, f"МУЗЫКА: {int(self.music_volume)}", self.font, lambda: None),
            Button(start_x_music + 235, panel_center_y + 50, self.volume_increase, self.volume_increase_hover, "", self.font, lambda: self.adjust_music_volume(10)),
            Button(start_x_sound, panel_center_y + 150, self.volume_decrease, self.volume_decrease_hover, "", self.font, lambda: self.adjust_sound_volume(-10)),
            Button(start_x_sound + 65, panel_center_y + 150, self.volume_display, self.volume_display, f"ЗВУКИ: {int(self.sound_volume)}", self.font, lambda: None),
            Button(start_x_sound + 235, panel_center_y + 150, self.volume_increase, self.volume_increase_hover, "", self.font, lambda: self.adjust_sound_volume(10)),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 350, self.button_normal, self.button_hover, "ПРИМЕНИТЬ", self.font, lambda: self.apply_settings()),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 450, self.button_normal, self.button_hover, "НАЗАД", self.font, lambda: self.init_main_menu())
        ]
        print("Меню настроек инициализировано.")

    def init_pause_menu(self):
        self.state = "pause"
        panel_center_x = self.screen_width // 2 - 450
        panel_center_y = self.screen_height // 2 - 300
        self.buttons = [
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 150, self.button_normal, self.button_hover, "ПРОДОЛЖИТЬ", self.font, lambda: setattr(self, 'state', 'game')),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 250, self.button_normal, self.button_hover, "ЗАНОВО", self.font, lambda: self.restart_level()),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 350, self.button_normal, self.button_hover, "НАСТРОЙКИ", self.font, lambda: self.open_settings()),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 450, self.button_normal, self.button_hover, "ГЛАВНОЕ МЕНЮ", self.font, lambda: self.exit_to_main_menu())
        ]
        print("Меню паузы инициализировано.")

    def init_mission_failed(self):
        self.state = "mission_failed"
        panel_center_x = self.screen_width // 2 - 450
        panel_center_y = self.screen_height // 2 - 300
        try:
            fail_sound = pygame.mixer.Sound("assets/sounds/mission_failed.wav")
            fail_sound.set_volume(self.sound_volume / 100.0)
            fail_sound.play()
            print("Звук 'Миссия провалена' воспроизведён.")
        except FileNotFoundError:
            print("Не удалось загрузить: assets/sounds/mission_failed.wav")
            if hasattr(self, 'click_sound'):
                self.click_sound.play()
        self.buttons = [
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 300, self.button_normal, self.button_hover, "ЗАНОВО", self.font, lambda: self.restart_level()),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 400, self.button_normal, self.button_hover, "ГЛАВНОЕ МЕНЮ", self.font, lambda: self.init_main_menu())
        ]
        print("Меню 'Миссия провалена' инициализировано.")

    def apply_settings(self):
        self.save_settings()
        print("Настройки применены.")

    def start_game(self):
        pygame.mixer.music.stop()
        self.state = "game"
        self.current_level = 1
        self.level_time = 0
        self.pollution_factor = 0.2
        self.garbage_spawn_timer = 2000
        self.asteroid_spawn_timer = 5000
        self.max_garbage = 5
        self.asteroid_speed = 1.0
        print("Игра начата.")

    def restart_level(self):
        self.start_game()
        print("Уровень перезапущен.")

    def exit_to_main_menu(self):
        self.state = "main"
        self.init_main_menu()
        print("Выход в главное меню.")

    def open_settings(self):
        self.state = "settings"
        self.init_settings()
        print("Открыто меню настроек.")

    def open_load_menu(self):
        self.state = "load"
        self.init_load_menu()
        print("Открыто меню загрузки.")

    def open_account_menu(self):
        if self.selected_account:
            self.state = "account"
            self.init_account_menu()
            print(f"Открыто меню аккаунта: {self.selected_account}")

    def open_upgrades(self):
        self.state = "upgrades"
        self.buttons = [Button(self.screen_width // 2 - 150, self.screen_height // 2, self.button_normal, self.button_hover, "НАЗАД", self.font, lambda: self.init_account_menu())]
        print("Открыто меню улучшений.")

    def open_achievements(self):
        self.state = "achievements"
        self.buttons = [Button(self.screen_width // 2 - 150, self.screen_height // 2, self.button_normal, self.button_hover, "НАЗАД", self.font, lambda: self.init_account_menu())]
        print("Открыто меню достижений.")

    def delete_account(self):
        if self.selected_account and self.selected_account in self.saves:
            index = 0
            while True:
                save_file = os.path.join(self.save_dir, f"save_{index}.json")
                if os.path.exists(save_file):
                    with open(save_file, 'r') as f:
                        data = json.load(f)
                        if data.get("name") == self.selected_account:
                            os.remove(save_file)
                            print(f"Удалён файл сохранения: {save_file}")
                            break
                    index += 1
                else:
                    break
            del self.saves[self.selected_account]
            self.selected_account = None
            self.init_load_menu()
            print(f"Аккаунт {self.selected_account} удалён.")

    def adjust_music_volume(self, step):
        self.music_volume = max(0.0, min(100.0, self.music_volume + step))
        pygame.mixer.music.set_volume(self.music_volume / 100.0)
        self.buttons[1].text = self.font.render(f"МУЗЫКА: {int(self.music_volume)}".upper(), True, (68, 36, 52))
        self.buttons[1].text_rect = self.buttons[1].text.get_rect(center=self.buttons[1].rect.center)
        self.save_settings()
        print(f"Громкость музыки изменена: {self.music_volume}")

    def adjust_sound_volume(self, step):
        self.sound_volume = max(0.0, min(100.0, self.sound_volume + step))
        for button in self.buttons:
            if hasattr(button, 'click_sound'):
                button.click_sound.set_volume(self.sound_volume / 100.0)
        self.buttons[4].text = self.font.render(f"ЗВУКИ: {int(self.sound_volume)}".upper(), True, (68, 36, 52))
        self.buttons[4].text_rect = self.buttons[4].text.get_rect(center=self.buttons[4].rect.center)
        self.save_settings()
        print(f"Громкость звука изменена: {self.sound_volume}")

    def update(self, mouse_pos, mouse_pressed):
        print(f"Обновление меню, текущее состояние: {self.state}")
        for button in self.buttons:
            if button.update(mouse_pos, mouse_pressed):
                button.action()
        if self.state == "new_account":
            for event in pygame.event.get():  # Убрано дублирование обработки событий
                if event.type == pygame.KEYDOWN:
                    print(f"Обработка клавиши: {event.key}")
                    if event.key == pygame.K_RETURN and self.input_text.strip():
                        self.create_new_game()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif len(self.input_text) < self.max_input_length:
                        char = event.unicode
                        if char.isalnum() or char.isspace():
                            self.input_text += char
                            print(f"Добавлен символ: {char}, текущий текст: {self.input_text}")
            self.input_text_surface = self.font.render(self.input_text.upper(), True, (255, 255, 255))
            self.input_text_rect = self.input_text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        return self.state

    def draw(self, screen):
        print(f"Рендеринг меню, состояние: {self.state}")
        screen.blit(self.background, (0, 0))
        if self.state in ["settings", "load", "account", "new_account", "upgrades", "achievements", "pause", "mission_failed"]:
            panel_rect = self.settings_panel.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            screen.blit(self.settings_panel, panel_rect)
            if self.state == "mission_failed":
                text = self.font.render("Миссия провалена!", True, (255, 0, 0))
                text_rect = text.get_rect(center=(self.screen_width // 2, panel_rect.centery - 100))
                screen.blit(text, text_rect)
            elif self.state == "account":
                screen.blit(self.balance_text, self.balance_text_rect)
                screen.blit(self.best_time_text, self.best_time_text_rect)
            elif self.state == "new_account":
                prompt_text = self.font.render("Введи имя аккаунта:", True, (255, 255, 255))
                prompt_text_rect = prompt_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
                screen.blit(prompt_text, prompt_text_rect)
                screen.blit(self.input_text_surface, self.input_text_rect)
        for button in self.buttons:
            button.draw(screen)