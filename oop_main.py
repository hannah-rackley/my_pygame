import pygame
pygame.init()

#Game colors
BLUE = (159, 232, 252)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROCK = (104, 115, 132)
WINNER = (244, 26, 88)

box_length = 85
margin = 5
box_number = 8

width = box_number * (box_length + margin)
height = box_number * (box_length + margin)

size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Save the penguins!")

class Top_level(object):
    def __init__(self):
        level_number = 3

    top_level_hole_dict = {
        'hole1': [4, 7],
        'hole2': [6, 7]
    }

    top_level_rock_dict = {
        'rock1': [2, 0],
        'rock2': [1, 2],
        'rock3': [2, 2],
        'rock4': [6, 3],
        'rock5': [1, 4],
        'rock6': [3, 5],
        'rock7': [2, 6],
        'rock8': [7, 7]
    }

    top_level_player = [2, 2]

    top_level_winner = [5, 7]

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
        screen.fill(WHITE)
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
            pygame.mixer.music.load('acid_burn.mp3')
            pygame.mixer.music.play()
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
            pygame.mixer.music.load('Fire_4.mp3')
            pygame.mixer.music.play()
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

class Create(object):
    def __init__(self, level):
        self.level = level
        player = self.level.top_level_player
        winner = self.level.top_level_winner
        hole_dict = self.level.top_level_hole_dict
        rock_dict = self.level.top_level_rock_dict
        
    #Create Player
    def create_player(player):
        player = Player(player[0], player[1])
        player_list = pygame.sprite.Group()
        player_list.add(player)
        return player_list

    #Create winning square
    def create_winner(winner):
        winner = Winner(winner[0], winner[1])
        winner_list = pygame.sprite.Group()
        winner_list.add(winner)
        return winner_list

    #Create holes given dictionary of holes and positions
    def hole_creator(hole_dict):
        hole_list = pygame.sprite.Group()
        for key in hole_dict:
            hole = Hole(hole_dict[key][0], hole_dict[key][1])
            hole_list.add(hole)
        return hole_list

    #Create rocks given dictionary of rocks and positions
    def rock_creator(rock_dict):
        rock_list = pygame.sprite.Group()
        for key in rock_dict:
            rock = Rock(rock_dict[key][0], rock_dict[key][1])
            rock_list.add(rock)
        return rock_list

#Setup tempo (60 frames per second)
clock = pygame.time.Clock()

def title_screen():
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Save the penguins!")
    background_image = pygame.image.load('frozen-lake.png').convert()

    start_game = False

    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_game = True
                done = True
        
        screen.blit(background_image, [0, 0])
        
        pygame.display.update()
        clock.tick(60)
    pygame.quit()

#Create the game loop.
def game_loop():
    level = Top_level()
    create = Create(level)
    player = create.create_player()
    winner_list = create.create_winner()

    done = False
    while not done:
        # title_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            pressed = pygame.key.get_pressed()
            player.change_move_speed(pressed)
        
        player_list.update()
        hole_list.update()
        rock_list.update()
        winner_list.update()
        
        #Check for collision with the winning square
        won = winner.check_winner_collision()
        if won:
            pygame.mixer.music.load('Won!.wav')
            pygame.mixer.music.play()

        #Check for collision with any of the holes.
        for hole in hole_list:
            deleted = hole.check_hole_collision()
            if deleted:
                player = Player(2, 2)
                player_list.add(player)

        #Check for collision with any of the rocks.
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
game_loop()
pygame.quit()