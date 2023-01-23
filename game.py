import pygame
from enum import Enum
from Ship import Ship
from client import Client
from gridField import gridField

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 200, 255)
PURPLE = (160, 110, 170)
c = (180, 230, 30)
screen = pygame.display.set_mode((700, 600))
GameStages = Enum("GameStages", ["BUY", "PLACE", "PLAY"])
Grids = Enum("Grids", ["MAINGRID", "ENEMYGRID"]) # for click identification
gridSize = 10
blocksize = 30
my_font = pygame.font.SysFont('Arial', 15)
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']  # for drawing
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  # for drawing
shipNumbers = [5, 4, 4, 3, 3, 3, 2, 2, 2, 2]  # which sizes ships should have
enemyships = []
shipstoplace = []  # list of ship objects
shipsPlaced = []
mainGridx = 370  # start x of my grid
mainGridy = 250  # start y of my grid
enemyGridx = 25
enemyGridy = 250

stage = GameStages.PLACE  # TODO change
shipIndex = 0  # current selected ship to place
running = True
#client = Client()  # initialises the connection


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


def generate_grid(size, gridx, gridy):
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            cell = gridField(i, j, i * blocksize + gridx, j * blocksize + gridy)
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
        pygame.draw.rect(screen, currentship.color, (pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1] - 10, currentship.width, currentship.height))
    elif stage == GameStages.PLAY:
        pass
        # if shooting, shoot icon or so


def process_click():
    x, y = pygame.mouse.get_pos()
    if x in range(mainGridx, mainGridx + 10 * blocksize):  # if click in the main grid
        if y in range(mainGridy, mainGridy + 10 * blocksize):
            xclick = int((x - mainGridx) / blocksize)
            yclick = int((y - mainGridy) / blocksize)
            if xclick + currentship.width / blocksize > gridSize or yclick + currentship.height / blocksize > gridSize:  # if ship cant be placed as it overextends the space
                return None
            else:
                return Grids.MAINGRID, xclick, yclick  # return tuple for grid cell index and main grid

    elif x in range(enemyGridx, enemyGridx + 10 * blocksize):  # if click in the enemy grid
        if y in range(enemyGridy, enemyGridy + 10 * blocksize):
            xclick = int((x - enemyGridx) / blocksize)
            yclick = int((y - enemyGridy) / blocksize) #TODO distinguish if cell already hit?
            return Grids.MAINGRID, xclick, yclick  # return tuple for grid cell index and enemy grid


def place_ships():
    global shipIndex, currentship, stage
    if process_click() is None:
        return
    grid, i, j, = process_click()  # i and j coordinates of the cell in which the click was in
    if grid == Grids.MAINGRID:
        canPlace = True  # check if ship can be placed or is too wide or high for grid
        for x in range(i, int(i + currentship.width / blocksize)):
            for y in range(j, int(j + currentship.height / blocksize)):
                if mainGrid[x][y].ship is not None:  # field already occupied
                    canPlace = False

        if canPlace:  # place ship onto fields that are free
            firstcell = mainGrid[i][j]
            shipstoplace[shipIndex].placing(firstcell.xcoord, firstcell.ycoord, currentship.width,
                                            currentship.height)  # for drawing
            for x in range(i, int(i + currentship.width / blocksize)):
                for y in range(j, int(j + currentship.height / blocksize)):
                    cell = mainGrid[x][y]  # cell to place ship in
                    cell.place_ship(shipstoplace[shipIndex])  # add ship to cell
                    shipstoplace[shipIndex].add_field(cell)  # add the cell to the ship todo problem with reference?

            shipsPlaced.append(shipstoplace[shipIndex])
            del (shipstoplace[shipIndex])
            shipIndex = 0
            if not all_placed():
                currentship = Ship(0, 0, shipstoplace[shipIndex].size)
            else:
                stage = GameStages.PLAY


def all_placed():
    allPlaced = True
    for ship in shipstoplace:
        if not ship.placed:
            allPlaced = False
    return allPlaced


def attack():
    if process_click() is None:
        return
    grid, i, j = process_click()
    if grid == Grids.ENEMYGRID:
        cell = enemyGrid[i][j]
        cell.attack_cell() #TODO check for other player!!!

generate_ships()  # make list of ships objects
currentship = Ship(0, 0, shipstoplace[shipIndex].size)
mainGrid = generate_grid(gridSize, mainGridx, mainGridy)
enemyGrid = generate_grid(gridSize, enemyGridx, enemyGridy)
client = Client()  # TODO handle exception


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if stage == GameStages.PLACE:  # only process up and down when game stage is place
                shipstoplace[shipIndex].deselect_ship()
                if event.key == pygame.K_UP:
                    shipIndex = max(0, shipIndex - 1)  # select one ship upwards
                    currentship = Ship(0, 0, shipstoplace[shipIndex].size)

                elif event.key == pygame.K_DOWN:
                    shipIndex = min(shipIndex + 1, len(shipstoplace) - 1)  # select one ship downwards
                    currentship = Ship(0, 0, shipstoplace[shipIndex].size)

                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # swap orientation
                    currentship.change_orientation()


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if stage == GameStages.PLACE:
                place_ships()
            elif stage == GameStages.PLAY:
                attack()

    screen.fill(PURPLE)

    if stage == GameStages.BUY:
        pass

    elif stage == GameStages.PLACE: # todo
        draw_ships()
        shipstoplace[shipIndex].select_ship()
        draw_grid(mainGridx, mainGridy, blocksize, gridSize)

    elif stage == GameStages.PLAY:
        draw_ships()
        draw_grid(mainGridx, mainGridy, blocksize, gridSize)
        draw_grid(enemyGridx, enemyGridy, blocksize, gridSize)

    mouse_icon()


    pygame.display.update()
