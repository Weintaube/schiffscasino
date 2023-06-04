import sys

import pygame
from enum import Enum
from Ship import Ship
from gridField import gridField
from threading import Thread
from socket import socket

pygame.init()

GameStages = Enum("GameStages", ["LOBBY", "PLACE", "PLAY"])

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (200, 100, 230)
PURPLE = (100, 100, 230)
c = (180, 230, 30)

screen = pygame.display.set_mode((700, 600))

gridSize = 10
blocksize = 30
my_font = pygame.font.SysFont('Arial', 15)
my_lobby_font = pygame.font.SysFont('freesansbold.ttf', 35)
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']  # for drawing
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  # for drawing
shipNumbers = [5, 4, 4, 3, 3, 3, 2, 2, 2, 2]  # which sizes ships should have

mainGridx = 350  # start x of my grid
mainGridy = 250  # start y of my grid
enemyGridx = 20  # start x of       enemy grid
enemyGridy = 20  # start y of enemy grid

host = '127.0.0.1'  # server name
port = 5001  # port name


# mainGrid = []  # two dimensional list of grid fields

class Game:

    def __init__(self):  # instance variables
        self.stop = False
        self.running = True
        self.client_socket = socket()  # instantiate
        self.client_socket.connect((host, port))  # connect to the server
        print("Waiting for connection")
        self.stage = GameStages.LOBBY  # TODO change
        self.shipstoplace = []  # list of ship objects
        self.shipsPlaced = []
        self.shipIndex = 0  # current selected ship to place
        self.generate_ships()  # make list of ships objects
        self.currentShip = Ship(0, 0, self.shipstoplace[self.shipIndex].size)  # default first ship next to mouse
        self.mainGrid = self.generate_grid(gridSize)

    def receive(self):
        username = input("Username: ")
        self.client_socket.send(username.encode())  # first, send username to server

        while True:
            try:
                if self.stop:  # exiting thread
                    sys.exit()

                message = self.client_socket.recv(1024).decode()  # receive msg from server
                if message == "START":
                    print("The game can start.")
                    self.stage = GameStages.PLACE
                else:
                    print(message)
            except:
                self.client_socket.close()
                break

    def write(self):
        while True:  # take input from console
            message = input()
            self.client_socket.send(message.encode())  # send to server
            if message == "STOP":
                self.stop = True
                sys.exit()

    def generate_ships(self):
        offset = 0
        startx = 20
        starty = 20
        for size in shipNumbers:
            s = Ship(startx, starty + offset, size)
            self.shipstoplace.append(s)
            offset += 2 * blocksize

    def draw_ships(self):
        for ship in self.shipstoplace:
            pygame.draw.rect(screen, ship.color, (ship.x, ship.y, ship.width, ship.height))
        for ship in self.shipsPlaced:
            pygame.draw.rect(screen, ship.color, (ship.x, ship.y, ship.width, ship.height))

    def generate_grid(self, size):
        grid = []
        for i in range(size):
            row = []
            for j in range(size):
                cell = gridField(i, j, i * blocksize + mainGridx, j * blocksize + mainGridy)
                row.append(cell)
            grid.append(row)
        return grid

    def draw_grid(self, startx, starty, blocksize, size):
        offset = 0
        for i in range(0, size + 1):  # horizontal
            pygame.draw.line(screen, WHITE, (startx, starty + offset), ((startx + size * blocksize), starty + offset),
                             2)
            offset += blocksize

        offset = 0
        for j in range(0, size + 1):  # vertical
            pygame.draw.line(screen, WHITE, (startx + offset, starty), (startx + offset, (starty + size * blocksize)),
                             2)
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

    """
    def mouse_icon():
        if stage == GameStages.PLACE:
            currentShip = Ship(0, 0, shipstoplace[
                shipIndex].size)
        elif stage == GameStages.PLAY:
            print("new mouse icon")
    """

    def process_click(self, mousePos):
        global shipIndex
        if self.stage == GameStages.PLACE:
            if mousePos[0] in range(mainGridx, mainGridx + 10 * blocksize):
                if mousePos[1] in range(mainGridy, mainGridy + 10 * blocksize):  # if click in the main grid
                    xclick = int((mousePos[0] - mainGridx) / blocksize)
                    yclick = int((mousePos[1] - mainGridy) / blocksize)
                    if xclick + self.currentShip.width / blocksize > gridSize or yclick + self.currentShip.height / blocksize > gridSize:  # if ship cant be placed as it overextends the space
                        return

                    canPlace = True
                    for x in range(xclick, int(xclick + self.currentShip.width / blocksize)):
                        for y in range(yclick, int(yclick + self.currentShip.height / blocksize)):
                            if self.mainGrid[x][y].ship is not None:  # field already occupied
                                canPlace = False

                    if canPlace:  # place ship onto fields that are free
                        print("can place ship on " + str(xclick) + " " + str(yclick))
                        firstcell = self.mainGrid[xclick][yclick]
                        self.shipstoplace[self.shipIndex].placing(firstcell.xcoord, firstcell.ycoord, self.currentShip.width,
                                                             self.currentShip.height)
                        for x in range(xclick, int(xclick + self.currentShip.width / blocksize)):
                            for y in range(yclick, int(yclick + self.currentShip.height / blocksize)):
                                cell = self.mainGrid[x][y]  # cell to place ship in
                                cell.place_ship(self.shipstoplace[self.shipIndex])  # add ship to field
                                self.shipstoplace[self.shipIndex].add_field(
                                    cell)  # add the field to the ship todo problem with reference?

                        self.shipsPlaced.append(self.shipstoplace[self.shipIndex])
                        del (self.shipstoplace[self.shipIndex])  # todo delete hard copy?
                        print(self.shipstoplace)
                        self.shipIndex = 0
                        # are_all_placed()
            elif self.stage == GameStages.PLAY:
                print("process the click in play phase")

    # checks if all ships are placed, it returns boolean, if all placed the next screen shows
    def are_all_placed(self):
        allPlaced = True
        for ship in self.shipstoplace:
            if not ship.placed:
                allPlaced = False
        if allPlaced:
            print("ALL SHIPS ARE PLACED")
        return allPlaced

    def main_game(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        # are_all_placed()
                        self.shipstoplace[self.shipIndex].deselect_ship()
                        self.shipIndex = max(0, self.shipIndex - 1)  # select one ship upwards
                        self.currentShip = Ship(0, 0, self.shipstoplace[
                            self.shipIndex].size)  # change current ship copy, only change when current ship changes

                    elif event.key == pygame.K_DOWN:
                        # are_all_placed()
                        self.shipstoplace[self.shipIndex].deselect_ship()
                        self.shipIndex = min(self.shipIndex + 1,
                                             len(self.shipstoplace) - 1)  # select one ship downwards
                        self.currentShip = Ship(0, 0, self.shipstoplace[
                            self.shipIndex].size)  # change current ship copy, only change when current ship changes

                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # vertical orientation
                        self.currentShip.change_orientation()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.process_click(pygame.mouse.get_pos())  # placing ship in place phase
                    if not self.are_all_placed():
                        self.currentShip = Ship(0, 0,
                                                self.shipstoplace[self.shipIndex].size)  # todo fix when all are placed
                    else:  # generates next screen when all ships are placed
                        self.stage = GameStages.PLAY

            screen.fill(PINK)
            self.draw_ships()
            self.draw_grid(mainGridx, mainGridy, blocksize, gridSize)

            if self.stage == GameStages.LOBBY:
                screen.fill(PURPLE)
                text_surface = my_lobby_font.render("In Lobby. Waiting for the other player to join...", False, BLACK)
                screen.blit(text_surface, (50, 100))
            elif self.stage == GameStages.PLACE:

                self.shipstoplace[self.shipIndex].select_ship()
                pygame.draw.rect(screen, self.currentShip.color, (
                    pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1] - 10, self.currentShip.width,
                    self.currentShip.height))

            elif self.stage == GameStages.PLAY:
                self.draw_grid(enemyGridx, enemyGridy, blocksize, gridSize)

            pygame.display.update()


game = Game()
recv_thread = Thread(target=game.receive) #thread for receiving msgs
recv_thread.start()

write_thread = Thread(target=game.write) #thread for writing msgs
write_thread.start()

game.main_game()

