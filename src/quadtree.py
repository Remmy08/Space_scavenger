import pygame

class QuadTree:
    def __init__(self, boundary, capacity):
        """
        Инициализация QuadTree.
        boundary: pygame.Rect, определяющий границы узла
        capacity: максимальное количество объектов в узле перед разделением
        """
        self.boundary = boundary  # pygame.Rect(x, y, width, height)
        self.capacity = capacity  # Максимум объектов в узле
        self.objects = []  # Список объектов (спрайты с rect)
        self.divided = False  # Флаг, разделён ли узел
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    def subdivide(self):
        """
        Разделяет узел на четыре подузла.
        """
        x, y, w, h = self.boundary
        half_w, half_h = w / 2, h / 2

        # Создаём четыре подузла
        ne = pygame.Rect(x + half_w, y, half_w, half_h)
        nw = pygame.Rect(x, y, half_w, half_h)
        se = pygame.Rect(x + half_w, y + half_h, half_w, half_h)
        sw = pygame.Rect(x, y + half_h, half_w, half_h)

        self.northeast = QuadTree(ne, self.capacity)
        self.northwest = QuadTree(nw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)
        self.divided = True

        # Перераспределяем существующие объекты по подузлам
        for obj in self.objects:
            self.insert(obj)
        self.objects = []  # Очищаем список, так как объекты теперь в подузлах

    def insert(self, obj):
        """
        Вставляет объект в QuadTree.
        obj: спрайт с атрибутом rect
        """
        # Проверяем, пересекается ли объект с границами узла
        if not self.boundary.colliderect(obj.rect):
            return False

        # Если узел не разделён и есть место, добавляем объект
        if len(self.objects) < self.capacity and not self.divided:
            self.objects.append(obj)
            return True

        # Если узел полон и не разделён, разделяем его
        if not self.divided:
            self.subdivide()

        # Пробуем вставить объект в подузлы
        return (self.northeast.insert(obj) or
                self.northwest.insert(obj) or
                self.southeast.insert(obj) or
                self.southwest.insert(obj))

    def retrieve(self, rect):
        """
        Возвращает список объектов, которые могут пересекаться с заданным rect.
        """
        found = []
        # Проверяем, пересекается ли заданный rect с границами узла
        if not self.boundary.colliderect(rect):
            return found

        # Добавляем объекты текущего узла
        found.extend(self.objects)

        # Если узел разделён, рекурсивно ищем в подузлах
        if self.divided:
            found.extend(self.northeast.retrieve(rect))
            found.extend(self.northwest.retrieve(rect))
            found.extend(self.southeast.retrieve(rect))
            found.extend(self.southwest.retrieve(rect))

        # Удаляем дубликаты (на случай, если объект попал в несколько узлов)
        return list(set(found))

    def clear(self):
        """
        Очищает QuadTree, удаляя все объекты и подузлы.
        """
        self.objects = []
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None