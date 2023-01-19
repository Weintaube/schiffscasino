
class gridField:

    def __init__(self, x, y, xcoord, ycoord):
        self.ship = None
        self.hit = False
        self.x = x
        self.y = y
        self.xcoord = xcoord
        self.ycoord = ycoord

    def place_ship(self, ship):
        self.ship = ship

    def attack_cell(self):
        #check if ship is already hit there, else give ship hit
        return False
