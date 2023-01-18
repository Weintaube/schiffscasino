import random

class Ship:
    blocksize = 30
    selectColor = (180, 230, 30)
    startColor = (100, 100, 230)
    colors = [(200, 0, 0), (250, 120, 0), (150, 255, 50), (50, 255, 255), (50, 50, 255), (255, 55, 150), (150, 255, 200), (120, 0, 255), (20, 50, 100), (255, 255, 0)]

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.width = size * self.blocksize
        self.height = self.blocksize
        self.selected = False
        self.placed = False
        self.fields = []
        self.shot = [] # list for shot blocks
        self.dead = False
        self.color = self.startColor
        #list for blocks that the ship occupies

    def select_ship(self):
        self.selected = True
        self.color = self.selectColor

    def deselect_ship(self):
        self.selected = False
        self.color = self.startColor

    def change_orientation(self): # swap width and height
        print("change orient")
        accu = self.width
        self.width = self.height
        self.height = accu

    def add_field(self, coordinate):
        self.fields.append(coordinate)

    def placing(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.placed = True
        random.shuffle(self.colors)
        self.color = self.colors.pop()
