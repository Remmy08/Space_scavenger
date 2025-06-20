import pygame

class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary  
        self.capacity = capacity  
        self.objects = []  
        self.divided = False  
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    def subdivide(self):
        x, y, w, h = self.boundary
        half_w, half_h = w / 2, h / 2

        ne = pygame.Rect(x + half_w, y, half_w, half_h)
        nw = pygame.Rect(x, y, half_w, half_h)
        se = pygame.Rect(x + half_w, y + half_h, half_w, half_h)
        sw = pygame.Rect(x, y + half_h, half_w, half_h)

        self.northeast = QuadTree(ne, self.capacity)
        self.northwest = QuadTree(nw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)
        self.divided = True

        for obj in self.objects:
            self.insert(obj)
        self.objects = [] 

    def insert(self, obj):

        if not self.boundary.colliderect(obj.rect):
            return False

        if len(self.objects) < self.capacity and not self.divided:
            self.objects.append(obj)
            return True

        if not self.divided:
            self.subdivide()

        return (self.northeast.insert(obj) or
                self.northwest.insert(obj) or
                self.southeast.insert(obj) or
                self.southwest.insert(obj))

    def retrieve(self, rect):
        found = []
        if not self.boundary.colliderect(rect):
            return found

        found.extend(self.objects)

        if self.divided:
            found.extend(self.northeast.retrieve(rect))
            found.extend(self.northwest.retrieve(rect))
            found.extend(self.southeast.retrieve(rect))
            found.extend(self.southwest.retrieve(rect))

        return list(set(found))

    def clear(self):
        self.objects = []
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None