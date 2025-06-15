import pygame
import os
import json

print("Инициализация модуля menu...")

class Button:
    def __init__(self, x, y, normal_img, hover_img, text, font, action):
        print(f"Создание кнопки с координатами ({x}, {y}) и текстом {text}...")
        self.base_rect = normal_img.get_rect(topleft=(x, y))
        self.normal_img = normal_img
        self.hover_img = hover_img
        self.image = normal_img
        self.text = font.render(text.upper(), True, (68, 36, 52)) if text else None
        self.text_rect = self.text.get_rect(center=self.base_rect.center) if self.text else None
        self.action = action
        self.is_hovered = False
        self.was_pressed = False
        pygame.mixer.init()
        print("Инициализация звука кнопки...")
        self.click_sound = pygame.mixer.Sound("assets/sounds/button_click.wav")
        self.click_sound.set_volume(1.0)
        print("Кнопка создана.")

    def update(self, mouse_pos, mouse_pressed, scale_factor):
        scaled_rect = self.base_rect.copy()
        scaled_rect.x *= scale_factor
        scaled_rect.y *= scale_factor
        scaled_rect.width *= scale_factor
        scaled_rect.height *= scale_factor
        self.is_hovered = scaled_rect.collidepoint(mouse_pos)
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
                self.click_sound.play()
                return True
        return False

    def draw(self, screen, scale_factor):
        scaled_img = pygame.transform.scale(self.image, (int(self.image.get_width() * scale_factor), int(self.image.get_height() * scale_factor)))
        scaled_rect = self.base_rect.copy()
        scaled_rect.x *= scale_factor
        scaled_rect.y *= scale_factor
        scaled_rect.width *= scale_factor
        scaled_rect.height *= scale_factor
        screen.blit(scaled_img, scaled_rect)
        if self.text:
            scaled_text = pygame.transform.scale(self.text, (int(self.text.get_width() * scale_factor), int(self.text.get_height() * scale_factor)))
            scaled_text_rect = scaled_text.get_rect(center=scaled_rect.center)
            screen.blit(scaled_text, scaled_text_rect)

class Menu:
    def __init__(self, screen_width, screen_height):
        print(f"Инициализация Menu с размерами {screen_width}x{screen_height}...")
        self.base_width, self.base_height = 1920, 1080
        self.screen_width, self.screen_height = screen_width, screen_height
        self.scale_factor = min(screen_width / self.base_width, screen_height / self.base_height)
        print("Загрузка шрифта...")
        self.font = pygame.font.Font("assets/fonts/pixel.ttf", int(24 * self.scale_factor))
        try:
            print("Попытка загрузки фона...")
            self.background = pygame.image.load("assets/sprites/menu_background.png").convert()
            print("Фон загружен.")
        except FileNotFoundError:
            print("Ошибка загрузки фона, создание дефолтного фона...")
            self.background = pygame.Surface((self.base_width, self.base_height))
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
            print("Failed to load: assets/sounds/menu_music.mp3")
        try:
            print("Попытка загрузки спрайтов громкости...")
            volume_decrease = pygame.image.load("assets/sprites/ui/volume_decrease.png").convert_alpha()
            volume_decrease_hover = pygame.image.load("assets/sprites/ui/volume_decrease_hover.png").convert_alpha()
            volume_display = pygame.image.load("assets/sprites/ui/volume_display.png").convert_alpha()
            volume_increase = pygame.image.load("assets/sprites/ui/volume_increase.png").convert_alpha()
            volume_increase_hover = pygame.image.load("assets/sprites/ui/volume_increase_hover.png").convert_alpha()
            print("Спрайты громкости загружены.")
        except FileNotFoundError:
            print("Ошибка загрузки спрайтов громкости, создание дефолтных...")
            volume_decrease = pygame.Surface((60, 60))
            volume_decrease_hover = pygame.Surface((60, 60))
            volume_display = pygame.Surface((165, 60))
            volume_increase = pygame.Surface((60, 60))
            volume_increase_hover = pygame.Surface((60, 60))
            volume_decrease.fill((100, 100, 100))
            volume_decrease_hover.fill((150, 150, 150))
            volume_display.fill((150, 150, 150))
            volume_increase.fill((100, 100, 100))
            volume_increase_hover.fill((150, 150, 150))
            print("Дефолтные спрайты громкости созданы.")
        self.state = "main"
        self.buttons = []
        self.fullscreen = False
        self.music_volume = 100.0
        self.sound_volume = 100.0
        self.selected_account = None
        self.save_dir = "saves"
        self.settings_file = "settings.json"
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

    def load_saves(self):
        self.saves = {}
        for i in range(3):
            save_file = os.path.join(self.save_dir, f"save_{i}.json")
            if os.path.exists(save_file):
                with open(save_file, 'r') as f:
                    self.saves[f"Аккаунт {i+1}"] = json.load(f)
                print(f"Загружено сохранение: {save_file}")

    def save_game(self, account_name, level, score, music_volume, sound_volume):
        save_data = {
            "level": level,
            "score": score
        }
        for i in range(3):
            if f"Аккаунт {i+1}" not in self.saves or f"Аккаунт {i+1}" == account_name:
                save_file = os.path.join(self.save_dir, f"save_{i}.json")
                with open(save_file, 'w') as f:
                    json.dump(save_data, f)
                self.saves[account_name] = save_data
                break

    def init_main_menu(self):
        self.state = "main"
        self.buttons = [
            Button(self.base_width // 2 - 150, self.base_height // 2 - 150, self.button_normal, self.button_hover, "НОВАЯ ИГРА", self.font, lambda: self.start_game()),
            Button(self.base_width // 2 - 150, self.base_height // 2 - 50, self.button_normal, self.button_hover, "ЗАГРУЗИТЬ", self.font, lambda: self.open_load_menu()),
            Button(self.base_width // 2 - 150, self.base_height // 2 + 50, self.button_normal, self.button_hover, "НАСТРОЙКИ", self.font, lambda: self.open_settings()),
            Button(self.base_width // 2 - 150, self.base_height // 2 + 150, self.button_normal, self.button_hover, "ВЫХОД", self.font, lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)))
        ]
        print("Главное меню инициализировано.")

    def init_load_menu(self):
        self.state = "load"
        panel_center_x = self.base_width // 2 - 450
        panel_center_y = self.base_height // 2 - 300
        self.buttons = [
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 50, self.button_normal, self.button_hover, "АККАУНТ 1" if "Аккаунт 1" in self.saves else "", self.font, lambda: setattr(self, 'selected_account', "Аккаунт 1")),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 150, self.button_normal, self.button_hover, "АККАУНТ 2" if "Аккаунт 2" in self.saves else "", self.font, lambda: setattr(self, 'selected_account', "Аккаунт 2")),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 250, self.button_normal, self.button_hover, "АККАУНТ 3" if "Аккаунт 3" in self.saves else "", self.font, lambda: setattr(self, 'selected_account', "Аккаунт 3")),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 400, self.button_normal, self.button_hover, "ВЫБРАТЬ", self.font, lambda: self.open_account_menu() if self.selected_account else None),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 500, self.button_normal, self.button_hover, "УДАЛИТЬ", self.font, lambda: self.delete_account() if self.selected_account else None)
        ]
        print("Меню загрузки инициализировано.")

    def init_account_menu(self):
        self.state = "account"
        panel_center_x = self.base_width // 2 - 450
        panel_center_y = self.base_height // 2 - 300
        save_data = self.saves.get(self.selected_account, {"level": 1, "score": 0})
        self.buttons = []
        start_x = panel_center_x + 50
        start_y = panel_center_y + 50
        for i in range(12):  # Увеличено до 12 уровней
            row = i // 4
            col = i % 4
            x = start_x + (64 + 10) * col
            y = start_y + (64 + 10) * row
            is_locked = i + 1 > save_data["level"]
            sprite = "assets/sprites/levels/current_level.png" if i + 1 == save_data["level"] else \
                     "assets/sprites/levels/locked_level.png" if is_locked else "assets/sprites/levels/completed_level.png"
            try:
                level_img = pygame.image.load(sprite).convert_alpha()
            except FileNotFoundError:
                level_img = pygame.Surface((64, 64))
                level_img.fill((100, 100, 100))
            self.buttons.append(Button(x, y, level_img, level_img, "", self.font, lambda x=i+1: self.start_game(x) if not is_locked else None))
        self.buttons.append(Button(panel_center_x + 750, panel_center_y + 550, self.button_normal, self.button_hover, "НАЗАД", self.font, lambda: self.init_main_menu()))
        self.buttons.append(Button(panel_center_x + 450, panel_center_y + 550, self.button_normal, self.button_hover, "УЛУЧШЕНИЯ", self.font, lambda: self.open_upgrades()))
        self.buttons.append(Button(panel_center_x + 600, panel_center_y + 550, self.button_normal, self.button_hover, "ДОСТИЖЕНИЯ", self.font, lambda: self.open_achievements()))
        print("Меню аккаунта инициализировано.")

    def init_settings(self):
        self.state = "settings"
        panel_center_x = self.base_width // 2 - 450
        panel_center_y = self.base_height // 2 - 300
        total_width = 60 + 5 + 165 + 5 + 60
        start_x_music = panel_center_x + (900 - total_width) // 2
        start_x_sound = panel_center_x + (900 - total_width) // 2
        self.buttons = [
            Button(start_x_music, panel_center_y + 50, volume_decrease, volume_decrease_hover, "", self.font, lambda: self.adjust_music_volume(-10)),
            Button(start_x_music + 65, panel_center_y + 50, volume_display, volume_display, f"МУЗЫКА: {int(self.music_volume)}", self.font, lambda: None),
            Button(start_x_music + 235, panel_center_y + 50, volume_increase, volume_increase_hover, "", self.font, lambda: self.adjust_music_volume(10)),
            Button(start_x_sound, panel_center_y + 150, volume_decrease, volume_decrease_hover, "", self.font, lambda: self.adjust_sound_volume(-10)),
            Button(start_x_sound + 65, panel_center_y + 150, volume_display, volume_display, f"ЗВУКИ: {int(self.sound_volume)}", self.font, lambda: None),
            Button(start_x_sound + 235, panel_center_y + 150, volume_increase, volume_increase_hover, "", self.font, lambda: self.adjust_sound_volume(10)),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 250, self.button_normal, self.button_hover, f"ПОЛНОЭКРАННЫЙ: {'ВКЛ' if self.fullscreen else 'ВЫКЛ'}", self.font, lambda: self.toggle_fullscreen()),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 350, self.button_normal, self.button_hover, "ПРИМЕНИТЬ", self.font, lambda: self.apply_settings()),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 450, self.button_normal, self.button_hover, "НАЗАД", self.font, lambda: self.init_main_menu())
        ]
        print("Меню настроек инициализировано.")

    def init_pause_menu(self):
        self.state = "pause"
        panel_center_x = self.base_width // 2 - 450
        panel_center_y = self.base_height // 2 - 300
        self.buttons = [
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 150, self.button_normal, self.button_hover, "ПРОДОЛЖИТЬ", self.font, lambda: setattr(self, 'state', 'game')),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 250, self.button_normal, self.button_hover, "ЗАНОВО", self.font, lambda: self.start_game(self.current_level)),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 350, self.button_normal, self.button_hover, "НАСТРОЙКИ", self.font, lambda: self.open_settings()),
            Button(panel_center_x + (900 - 300) // 2, panel_center_y + 450, self.button_normal, self.button_hover, "ГЛАВНОЕ МЕНЮ", self.font, lambda: self.init_main_menu())
        ]
        print("Меню паузы инициализировано.")

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.buttons[6].text = self.font.render(f"ПОЛНОЭКРАННЫЙ: {'ВКЛ' if self.fullscreen else 'ВЫКЛ'}".upper(), True, (68, 36, 52))
        self.buttons[6].text_rect = self.buttons[6].text.get_rect(center=self.buttons[6].base_rect.center)
        self.save_settings()

    def apply_settings(self):
        flags = pygame.FULLSCREEN if self.fullscreen else 0
        if not self.fullscreen:
            screen = pygame.display.set_mode((self.base_width, self.base_height), flags | pygame.RESIZABLE)
        else:
            screen = pygame.display.set_mode((0, 0), flags | pygame.FULLSCREEN)
        self.screen_width, self.screen_height = screen.get_size()
        self.scale_factor = min(self.screen_width / self.base_width, self.screen_height / self.base_height)
        self.font = pygame.font.Font("assets/fonts/pixel.ttf", int(24 * self.scale_factor))
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        self.init_settings()
        self.save_settings()

    def start_game(self, level=1):
        pygame.mixer.music.stop()
        self.state = "game"
        self.current_level = level

    def open_settings(self):
        self.state = "settings"
        self.init_settings()

    def open_load_menu(self):
        self.state = "load"
        self.init_load_menu()

    def open_account_menu(self):
        if self.selected_account:
            self.state = "account"
            self.init_account_menu()

    def open_upgrades(self):
        self.state = "upgrades"
        self.buttons = [Button(self.base_width // 2 - 150, self.base_height // 2, self.button_normal, self.button_hover, "НАЗАД", self.font, lambda: self.init_account_menu())]

    def open_achievements(self):
        self.state = "achievements"
        self.buttons = [Button(self.base_width // 2 - 150, self.base_height // 2, self.button_normal, self.button_hover, "НАЗАД", self.font, lambda: self.init_account_menu())]

    def delete_account(self):
        if self.selected_account and self.selected_account in self.saves:
            save_file = os.path.join(self.save_dir, f"save_{int(self.selected_account[-1]) - 1}.json")
            if os.path.exists(save_file):
                os.remove(save_file)
            del self.saves[self.selected_account]
            self.selected_account = None
            self.init_load_menu()

    def adjust_music_volume(self, step):
        self.music_volume = max(0.0, min(100.0, self.music_volume + step))
        pygame.mixer.music.set_volume(self.music_volume / 100.0)
        self.buttons[1].text = self.font.render(f"МУЗЫКА: {int(self.music_volume)}".upper(), True, (68, 36, 52))
        self.buttons[1].text_rect = self.buttons[1].text.get_rect(center=self.buttons[1].base_rect.center)
        self.save_settings()

    def adjust_sound_volume(self, step):
        self.sound_volume = max(0.0, min(100.0, self.sound_volume + step))
        for button in self.buttons:
            if hasattr(button, 'click_sound'):
                button.click_sound.set_volume(self.sound_volume / 100.0)
        self.buttons[4].text = self.font.render(f"ЗВУКИ: {int(self.sound_volume)}".upper(), True, (68, 36, 52))
        self.buttons[4].text_rect = self.buttons[4].text.get_rect(center=self.buttons[4].base_rect.center)
        self.save_settings()

    def update(self, mouse_pos, mouse_pressed):
        scaled_mouse_pos = (mouse_pos[0] / self.scale_factor, mouse_pos[1] / self.scale_factor)
        for button in self.buttons:
            if button.update(scaled_mouse_pos, mouse_pressed, self.scale_factor):
                button.action()
        return self.state

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        if self.state in ["settings", "load", "account", "upgrades", "achievements", "pause"]:
            scaled_panel = pygame.transform.scale(self.settings_panel, (int(900 * self.scale_factor), int(600 * self.scale_factor)))
            panel_rect = scaled_panel.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            screen.blit(scaled_panel, panel_rect)
        for button in self.buttons:
            button.draw(screen, self.scale_factor)