
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
        
        #check if occupied via orientation
