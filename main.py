import pygame
pygame.init()

#Game colors
BLUE = (159, 232, 252)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROCK = (104, 115, 132)

#Setup our screen size.
box_length = 85
margin = 2
box_number = 6

width = box_number * (box_length + margin)
height = box_number * (box_length + margin)

size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Save the penguins!")

class Board(object):

    def __init__(self):
        self.grid = []
    
    def create_grid_array(self):
        for row in range(box_number):
            self.grid.append([])
            for column in range(box_number):
                self.grid[row].append(0)
        return self.grid

    def draw_board(self):
        grid = self.create_grid_array()
        screen.fill(BLACK)
        for row in range(box_number):
            for column in range(box_number):
                color = BLUE
                pygame.draw.rect(screen, color, [(margin + box_length) * column + margin, (margin + box_length) * row + margin, box_length, box_length])
        return grid

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

    def change_move_speed(self, pressed):
        if self.move_horizontal == 0 and self.move_vertical == 0:
            if pressed[pygame.K_RIGHT]:
                self.move_horizontal = 10
            elif pressed[pygame.K_LEFT]:
                self.move_horizontal = -10
            elif pressed[pygame.K_UP]:
                self.move_vertical = -10
            elif pressed[pygame.K_DOWN]:
                self.move_vertical = 10

    def update(self):
        if self.rect.right + self.move_horizontal >= width:
            self.move_horizontal = 0
        elif self.rect.left + self.move_horizontal <= 0:
            self.move_horizontal = 0
        if self.rect.bottom + self.move_vertical >= height:
            self.move_vertical = 0
        elif self.rect.top + self.move_vertical <= 0:
            self.move_vertical = 0
        
        self.rect.x += self.move_horizontal
        self.rect.y += self.move_vertical

class Hole(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Hole, self).__init__()
    
        self.image = pygame.Surface([box_length, box_length])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

        self.rect.x = (box_length + margin) * x + margin
        self.rect.y = (box_length + margin) * y + margin

    def check_hole_collision(self):
       pygame.sprite.spritecollide(self, all_sprites_list, True)

# class Rock(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super(Rock, self).__init__()
    
#         self.image = pygame.Surface([box_length, box_length])
#         self.image.fill(BLACK)
#         self.rect = self.image.get_rect()

#         self.rect.x = (box_length + margin) * x + margin
#         self.rect.y = (box_length + margin) * y + margin

#     def check_hole_collision(self):
#        pygame.sprite.spritecollide(self, all_sprites_list, True)
            
    
#Setup board      
board = Board()

#Create Player
player = Player(2, 2)
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player)

#Create hole
hole = Hole(0, 2)
hole_list = pygame.sprite.Group()
hole_list.add(hole)

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
    hole_list.update()

    hole.check_hole_collision()
    #draw grid to the screen
    board.draw_board()

    #draw sprites to the screen
    all_sprites_list.draw(screen)
    hole_list.draw(screen)
    #update screen
    pygame.display.update()
    
    #setting clock
    clock.tick(60)

pygame.quit()