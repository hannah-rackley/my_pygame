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

        #Set height and width
        self.image = pygame.image.load('penguin1.png').convert_alpha()

        #Make top left corner the passed-in location
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #Set speed
        self.change_x = 0
        self.change_y = 0

    def change_speed(self, x, y):
        self.change_x += x
        self.change_y += y
    
    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
#Setup board      
board = Board()
grid = board.create_grid_array()

#Create player
player = Player(5, 5)
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
        #Set speed based on key pressed.
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.change_speed(-3, 0)
            elif event.key == pygame.K_RIGHT:
                player.change_speed(3, 0)
            elif event.key == pygame.K_UP:
                player.change_speed(0, -3)
            elif event.key == pygame.K_DOWN:
                player.change_speed(0, 3)
        #Reset speed when key is released
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.change_speed(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.change_speed(-3, 0)
            elif event.key == pygame.K_UP:
                player.change_speed(0, 3)
            elif event.key == pygame.K_DOWN:
                player.change_speed(0, -3)

        
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     pos = pygame.mouse.get_pos()
        #     column = pos[0] // (width + margin)
        #     row = pos[1] // (height + margin)
        #     grid[row][column] = 1

    all_sprites_list.update()
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

    #update screen
    pygame.display.update()
    
    #setting clock
    clock.tick(60)

pygame.quit()