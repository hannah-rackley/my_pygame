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
        return self.grid

    # def create_hole(self):
    #     self.grid[x][y] = 1
    #     return self.grid
    
    # def create_rock(self):
    #     self.grid[x][y] = 2
    #     return self.grid

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()

        #Set image
        self.image = pygame.image.load('penguin1.png').convert_alpha()

        #Make top left corner the passed-in location
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #Set speed
        self.move_horizontal = 0
        self.move_vertical = 0

    def update(self):
        if self.rect.right + self.move_horizontal >= 600:
            self.move_horizontal = 0
        elif self.rect.left + self.move_horizontal <= 0:
            self.move_horizontal = 0
        if self.rect.bottom + self.move_vertical >= 600:
            self.move_vertical = 0
        elif self.rect.top + self.move_vertical <= 0:
            self.move_vertical = 0
        
        self.rect.x += self.move_horizontal
        self.rect.y += self.move_vertical

    def change_move_speed(self, pressed):
        if self.move_horizontal == 0 and self.move_vertical == 0:
            if pressed[pygame.K_RIGHT]:
                self.move_horizontal = 3
            elif pressed[pygame.K_LEFT]:
                self.move_horizontal = -3
            elif pressed[pygame.K_UP]:
                self.move_vertical = -3
            elif pressed[pygame.K_DOWN]:
                self.move_vertical = 3
    
#Setup board      
board = Board()
grid = board.create_grid_array()

#Create player
player = Player(2, 2)
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player)

#Setup tempo (60 frames per second)
clock = pygame.time.Clock()

#Create the game loop.
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        pressed = pygame.key.get_pressed()
        player.change_move_speed(pressed)
        
        player.update()

    #draw grid to the screen
    screen.fill(BLACK)
    for row in range(5):
        for column in range(5):
            color = BLUE
            if grid[row][column] == 1:
                color = WHITE
            elif grid[row][column] == 2:
                color = BLACK
            pygame.draw.rect(screen, color, [(margin + width) * column + margin, (margin + height) * row + margin, width, height])

    #draw sprites to the screen
    all_sprites_list.draw(screen)

    #Get pressed keys
    player.update()

    #update screen
    pygame.display.update()
    
    #setting clock
    clock.tick(60)

pygame.quit()