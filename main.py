import pygame
from enum import Enum
from Ship import Ship
from gridField import gridField

pygame.init()

GameStages = Enum("GameStages", ["BUY", "PLACE", "PLAY"])
stage = GameStages.PLACE #TODO change

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (200, 100, 230)
PURPLE = (100, 100, 230)
c = (180, 230, 30)

screen = pygame.display.set_mode((700, 600))
running = True

gridSize = 10
blocksize = 30
my_font = pygame.font.SysFont('Arial', 15)
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']  # for drawing
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  # for drawing
shipNumbers = [5, 4, 4, 3, 3, 3, 2, 2, 2, 2]  # which sizes ships should have
shipstoplace = []  # list of ship objects
shipsPlaced = []

shipIndex = 0  # current selected ship to place
mainGridx = 350  # start x of my grid
mainGridy = 250  # start y of my grid
#mainGrid = []  # two dimensional list of grid fields


def generate_ships():
    offset = 0
    startx = 20
    starty = 20
    for size in shipNumbers:
        s = Ship(startx, starty + offset, size)
        shipstoplace.append(s)
        offset += 2 * blocksize

def draw_ships():
    for ship in shipstoplace:
        pygame.draw.rect(screen, ship.color, (ship.x, ship.y, ship.width, ship.height))
    for ship in shipsPlaced:
        pygame.draw.rect(screen, ship.color, (ship.x, ship.y, ship.width, ship.height))

def generate_grid(size):
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            cell = gridField(i, j, i*blocksize+mainGridx, j*blocksize+mainGridy)
            row.append(cell)
        grid.append(row)
    return grid


def draw_grid(startx, starty, blocksize, size):
    offset = 0
    for i in range(0, size + 1):  # horizontal
        pygame.draw.line(screen, WHITE, (startx, starty + offset), ((startx + size * blocksize), starty + offset), 2)
        offset += blocksize

    offset = 0
    for j in range(0, size + 1):  # vertical
        pygame.draw.line(screen, WHITE, (startx + offset, starty), (startx + offset, (starty + size * blocksize)), 2)
        offset += blocksize

    # Buchstaben und Zahlen
    offset = 0
    for letter in letters:
        text_surface = my_font.render(letter, False, BLACK)
        screen.blit(text_surface, (startx + blocksize / 2 + offset, starty - blocksize / 2))
        offset += blocksize

    offset = 0
    for number in numbers:
        text_surface = my_font.render(number, False, BLACK)
        screen.blit(text_surface, (startx - blocksize / 2, starty + blocksize / 2 + offset))
        offset += blocksize

def mouse_icon():
    if stage == GameStages.PLACE:
        currentShip = Ship(0, 0, shipstoplace[
            shipIndex].size)


def process_click(mousePos):
    global shipIndex
    if mousePos[0] in range(mainGridx, mainGridx + 10 * blocksize):
        if mousePos[1] in range(mainGridy, mainGridy + 10 * blocksize):  # if click in the main grid
            xclick = int((mousePos[0] - mainGridx) / blocksize)
            yclick = int((mousePos[1] - mainGridy) / blocksize)
            if xclick + currentShip.width / blocksize > gridSize or yclick + currentShip.height / blocksize > gridSize:  # if ship cant be placed as it overextends the space
                return


            canPlace = True
            for x in range(xclick, int(xclick + currentShip.width / blocksize)):
                for y in range(yclick, int(yclick + currentShip.height / blocksize)):
                    if mainGrid[x][y].ship is not None:  # field already occupied
                        canPlace = False

            if canPlace:  # place ship onto fields that are free
                print("can place ship on "+ str(xclick)+" "+ str(yclick))
                firstcell = mainGrid[xclick][yclick]
                shipstoplace[shipIndex].placing(firstcell.xcoord, firstcell.ycoord, currentShip.width, currentShip.height)
                for x in range(xclick, int(xclick + currentShip.width / blocksize)):
                    for y in range(yclick, int(yclick + currentShip.height / blocksize)):
                        cell = mainGrid[x][y] # cell to place ship in
                        cell.place_ship(shipstoplace[shipIndex])  # add ship to field
                        shipstoplace[shipIndex].add_field(cell)  # add the field to the ship todo problem with reference?

                shipsPlaced.append(shipstoplace[shipIndex])
                del(shipstoplace[shipIndex]) #todo delete hard copy?
                print(shipstoplace)
                shipIndex = 0
                are_all_placed()

def are_all_placed():
    allPlaced = True
    for ship in shipstoplace:
        if not ship.placed:
            allPlaced = False
    if allPlaced:
        next_screen()
        print("NEXT SCREEN")
    print(allPlaced)
    return allPlaced
   
def next_screen():
    print("ALL SHIPS ARE PLACED")

generate_ships()  # make list of ships objects

currentShip = Ship(0, 0, shipstoplace[shipIndex].size)  # default first ship next to mouse

mainGrid = generate_grid(gridSize)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                are_all_placed()
                shipstoplace[shipIndex].deselect_ship()
                shipIndex = max(0, shipIndex - 1)  # select one ship upwards
                currentShip = Ship(0, 0, shipstoplace[
                    shipIndex].size)  # change current ship copy, only change when current ship changes

            elif event.key == pygame.K_DOWN:
                are_all_placed()
                shipstoplace[shipIndex].deselect_ship()
                shipIndex = min(shipIndex + 1, len(shipstoplace) - 1)  # select one ship downwards
                currentShip = Ship(0, 0, shipstoplace[
                    shipIndex].size)  # change current ship copy, only change when current ship changes

            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # vertical orientation
                currentShip.change_orientation()

        elif event.type == pygame.MOUSEBUTTONDOWN:
             #generates next screen
            process_click(pygame.mouse.get_pos())
            if not are_all_placed():
                currentShip = Ship(0, 0, shipstoplace[shipIndex].size) # todo fix when all are placed

    screen.fill(PINK)
    draw_ships()
    draw_grid(mainGridx, mainGridy, blocksize, gridSize)

    shipstoplace[shipIndex].select_ship() #todo

    pygame.draw.rect(screen, currentShip.color, (
        pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1] - 10, currentShip.width, currentShip.height))

    pygame.display.update()
