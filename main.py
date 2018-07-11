import pygame
pygame.init()

#Game colors
BLUE = (159, 232, 252)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROCK = (104, 115, 132)
WINNER = (244, 26, 88)

#Setup our screen size.
box_length = 85
margin = 5
box_number = 8

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
        hole_hit_list = pygame.sprite.spritecollide(self, player_list, True)
        if len(hole_hit_list) > 0:
            return True

class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Rock, self).__init__()
    
        self.image = pygame.Surface([box_length, box_length])
        self.image.fill(ROCK)
        self.rect = self.image.get_rect()

        self.rect.x = (box_length + margin) * x + margin
        self.rect.y = (box_length + margin) * y + margin

    def check_rock_collision(self):
        rock_hit_list = pygame.sprite.spritecollide(self, player_list, False)
        if len(rock_hit_list) > 0:
            if player.move_horizontal != 0:
                player.rect.x -= player.move_horizontal
            if player.move_vertical != 0:
                player.rect.y -= player.move_vertical
            player.move_horizontal = 0
            player.move_vertical = 0
            player.update()  

class Winner(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Winner, self).__init__()
    
        self.image = pygame.Surface([box_length, box_length])
        self.image.fill(WINNER)
        self.rect = self.image.get_rect()

        self.rect.x = (box_length + margin) * x + margin
        self.rect.y = (box_length + margin) * y + margin

    def check_winner_collision(self):
        winner_hit_list = pygame.sprite.spritecollide(self, player_list, True)
        if len(winner_hit_list) > 0:
            return True     
    
#Setup board      
board = Board()

#Create Player
player = Player(2, 2)
player_list = pygame.sprite.Group()
player_list.add(player)

#Create winning square
winner = Winner(5, 7)
winner_list = pygame.sprite.Group()
winner_list.add(winner)

#Create holes
hole1 = Hole(4, 7)
hole2 = Hole(6, 7)
hole_list = pygame.sprite.Group()
hole_list.add(hole1)
hole_list.add(hole2)

#Create rocks
rock1 = Rock(2, 0)
rock2 = Rock(1, 2)
rock3 = Rock(2, 2)
rock4 = Rock(6, 3)
rock5 = Rock(1, 4)
rock6 = Rock(3, 5)
rock7 = Rock(2, 6)
rock8 = Rock(7, 7)
rock_list = pygame.sprite.Group()
rock_list.add(rock1)
rock_list.add(rock2)
rock_list.add(rock3)
rock_list.add(rock4)
rock_list.add(rock5)
rock_list.add(rock6)
rock_list.add(rock7)
rock_list.add(rock8)
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
    rock_list.update()
    winner_list.update()

    won = winner.check_winner_collision()
    if won:
        done = True

    for hole in hole_list:
        deleted = hole.check_hole_collision()
        if deleted:
            player = Player(2, 2)
            player_list.add(player)

    for rock in rock_list:
        rock.check_rock_collision()

    #draw grid to the screen
    board.draw_board()

    #draw sprites to the screen
    player_list.draw(screen)
    winner_list.draw(screen)
    hole_list.draw(screen)
    rock_list.draw(screen)
    #update screen
    pygame.display.update()
    
    #setting clock
    clock.tick(60)

pygame.quit()