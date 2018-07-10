import pygame
pygame.init()

#Game colors
BLUE = (159, 232, 252)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Setup our screen size.
size = (600, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Save the penguins!")

width = 114
height = 114
margin = 5

class Board(object):

    def __init__(self):
        self.grid = []
    
    def create_grid_array(self):
        for row in range(5):
            self.grid.append([])
            for column in range(5):
                self.grid[row].append(0)
        self.grid[1][2] = 1
        self.grid[3][1] = 2
        return self.grid

#Setup tempo (60 frames per second)
clock = pygame.time.Clock()

#Create the game loop.
done = False
while not done:
    board = Board()
    grid = board.create_grid_array()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (width + margin)
            row = pos[1] // (height + margin)
            grid[row][column] = 1

    #draw to the screen
    screen.fill(BLACK)
    for row in range(5):
        for column in range(5):
            color = BLUE
            if grid[row][column] == 1:
                color = WHITE
            elif grid[row][column] == 2:
                color = BLACK
            pygame.draw.rect(screen, color, [(margin + width) * column + margin, (margin + height) * row + margin, width, height])
    pygame.display.update()
    #setting clock
    clock.tick(60)

pygame.quit()