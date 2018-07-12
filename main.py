import pygame
import time
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

#Setup tempo (60 frames per second)
clock = pygame.time.Clock()

#Play background music
def play_background_music():
    pygame.mixer.music.load('happy.mp3')
    pygame.mixer.music.play()
    if pygame.mixer.get_busy():
        pygame.time.delay(100)

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
        #Should this do this? or should it be done separately and then draw board is called after? 
        grid = self.create_grid_array()
        screen.fill(WHITE)
        for row in range(box_number):
            for column in range(box_number):
                color = BLUE
                pygame.draw.rect(screen, color, [(margin + box_length) * column + margin, (margin + box_length) * row + margin, box_length, box_length])
        return grid

class Level(object):
    def __init__(self, winner_pos, hole_dict, rock_dict):
        self.winner_pos = winner_pos
        self.hole_dict = hole_dict
        self.rock_dict = rock_dict
    
    def get_winner_list(self):
        #interesting that this uses an external global function. Wonder if there is a better way of managing
        #those external global variables that need to be set with these functions in these classes??
        winner_list = create_winner(self.winner_pos)
        return winner_list

    def get_hole_list(self):
        hole_list = hole_creator(self.hole_dict)
        return hole_list
    
    def get_rock_list(self):
        rock_list = rock_creator(self.rock_dict)
        return rock_list

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

#This class shares some similar variables as Player. Could these extend a parent class or interface? Does Python have interfaces?
class Hole(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Hole, self).__init__()
    
        self.image = pygame.Surface([box_length, box_length])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

        self.rect.x = (box_length + margin) * x + margin
        self.rect.y = (box_length + margin) * y + margin

    def check_hole_collision(self, player_list, player):
        #I like how it does not access the global player and takes it in as parameters
        hole_hit_list = pygame.sprite.spritecollide(self, player_list, True)
        if len(hole_hit_list) > 0:
            pygame.mixer.music.load('acid_burn.mp3')
            pygame.mixer.music.play()
            return True

class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Rock, self).__init__()
    
        self.image = pygame.Surface([box_length, box_length])
        self.image.fill(ROCK)
        self.rect = self.image.get_rect()

        #Similar to how calculations are done for Hole...seems like a good opportunity for a parent class??
        self.rect.x = (box_length + margin) * x + margin
        self.rect.y = (box_length + margin) * y + margin

    def check_rock_collision(self, player_list, player):
        rock_hit_list = pygame.sprite.spritecollide(self, player_list, False)
        if len(rock_hit_list) > 0:
            # pygame.mixer.music.load('Fire_4.mp3')
            # pygame.mixer.music.play()
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

    def check_winner_collision(self, player_list, player):
        winner_hit_list = pygame.sprite.spritecollide(self, player_list, True)
        if len(winner_hit_list) > 0:
            return True   
   
#Setup board      
board = Board()

#Create Player
def create_player():
    player = Player(2, 2)
    player_list = pygame.sprite.Group()
    player_list.add(player)
    return player_list

#Create winning square
def create_winner(winner_pos):
    winner = Winner(winner_pos[0], winner_pos[1])
    winner_list = pygame.sprite.Group()
    winner_list.add(winner)
    return winner_list
#create holes
def hole_creator(hole_dict):
    hole_list = pygame.sprite.Group()
    #cool cool cool. Works how I hoped it would
    for key in hole_dict:
        hole = Hole(hole_dict[key][0], hole_dict[key][1])
        hole_list.add(hole)
    return hole_list

#create rocks
def rock_creator(rock_dict):
    rock_list = pygame.sprite.Group()
    for key in rock_dict:
        rock = Rock(rock_dict[key][0], rock_dict[key][1])
        rock_list.add(rock)
    return rock_list

#make text
def make_text(text, font):
    textSurface = font.render(text, True, WINNER)
    return textSurface, textSurface.get_rect()
#display text
def display_medium_text(text):
    mediumText = pygame.font.Font('freesansbold.ttf', 30)
    TextSurf, TextRect = make_text(text, mediumText)
    TextRect.center = ((width/2), (height/3))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()

#Messages to be passed into tect creation functions
win_message = "You won! Try another level!!"
start_message = 'Save the penguin!'

#display text smaller
def display_instruction_text(text, x):
    mediumText = pygame.font.Font('freesansbold.ttf', 30)
    TextSurf, TextRect = make_text(text, mediumText)
    TextRect.center = ((width/2), (height - x))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()
#Check for pressed key and go to appropriate level
def get_level_input(pressed):
    if pressed[pygame.K_UP]:
        level_choice = 0
        return level_choice
    elif pressed[pygame.K_DOWN]:
        level_choice = 1
        return level_choice

#hard level
hard_winner_pos = [5, 7]

hard_hole_dict = {
    'hole1': [4, 7],
    'hole2': [6, 7]
}

hard_rock_dict = {
    'rock1': [2, 0],
    'rock2': [1, 2],
    'rock3': [2, 2],
    'rock4': [6, 3],
    'rock5': [1, 4],
    'rock6': [3, 5],
    'rock7': [2, 6],
    'rock8': [7, 7]
}
hard_level = Level(hard_winner_pos, hard_hole_dict, hard_rock_dict)

#easy level
easy_winner_pos = [3, 4]

easy_hole_dict = {
    'hole1': [3, 0],
    'hole2': [5, 1]
}

easy_rock_dict = {
    'rock1': [7, 3],
    'rock2': [0, 4],
    'rock3': [1, 2],
}
easy_level = Level(easy_winner_pos, easy_hole_dict, easy_rock_dict)

def title_screen(message):
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Save the penguin!")
    background_image = pygame.image.load('frozen-lake.png').convert()
    start_game = False

    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_UP] or pressed[pygame.K_DOWN]:
                    start_game = True
                else:
                    pressed = pygame.key.get_pressed()
                    

        screen.blit(background_image, [0, 0])
        display_medium_text(message)
        display_instruction_text("For level one, press up", 300)
        display_instruction_text("For level two, press down", 250)

        pygame.display.update()
        clock.tick(60)

    game_loop()

#Create the game loop.
def game_loop():
    pressed = pygame.key.get_pressed()
    level = get_level_input(pressed)
    if level == 0:
        hole_list = easy_level.get_hole_list()
        rock_list = easy_level.get_rock_list()
        winner_list = easy_level.get_winner_list()
        for player in winner_list:
            winner = player
    elif level == 1:
        hole_list = hard_level.get_hole_list()
        rock_list = hard_level.get_rock_list()
        winner_list = hard_level.get_winner_list()
        for player in winner_list:
            winner = player

    player_list = create_player()
    #does this loop through an array but only set person to one of the people in the player_list?
    for person in player_list:
        player = person
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
            pressed = pygame.key.get_pressed()
            player.change_move_speed(pressed)
        
        player.update()
        hole_list.update()
        rock_list.update()
        winner.update()
        
        #Check for collision with the winning square
        won = winner.check_winner_collision(player_list, player)
        if won:
            pygame.mixer.music.load('Won!.wav')
            pygame.mixer.music.play()
            start_game = False
            title_screen(win_message)

        #Check for collision with any of the holes.
        for hole in hole_list:
            deleted = hole.check_hole_collision(player_list, player)
            if deleted:
                player_list = create_player()
                for person in player_list:
                    player = person

        #Check for collision with any of the rocks.
        for rock in rock_list:
            rock.check_rock_collision(player_list, player)

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

title_screen(start_message)
pygame.quit()