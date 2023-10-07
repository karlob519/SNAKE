# Imports
import pygame
import random
import sys
import time
import sfx

# Display
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
board = pygame.Surface((800, 800))
pygame.display.set_caption('Snake')
score_font = pygame.font.SysFont('Calibri', 50)
score_pos = (40, 100)
ariel = pygame.font.SysFont('Ariel', 50)

# Clock
clock = pygame.time.Clock()
FPS = 8

# Colours
black = (0, 0, 0)
white = (255, 255, 255)
orange = (255, 128, 10)
light_grey = (200, 200, 200)
dark_grey = (50, 50, 50)
light_blue = (20, 150, 250)
dark_blue = (1, 47, 200)
bright_green = (10, 250, 50)
dark_green = (2, 120, 30)
red = (250, 0, 30)
dark_brown = (142, 92, 71)
light_brown = (240, 217, 181)
yellow = (250, 250, 5)
purple = (160, 50, 120)
bg_colour = black

# Setting up the initial state and some constants like the size of the squares and starting 
# positions of the board
screen.fill(bg_colour)
pygame.draw.rect(board, white, (0, 0, 800, 800), 1)
board_pos = (200, 50)
screen.blit(board, board_pos)
pygame.display.update()


block_size = 38
counter = 0
twenty_set = [(i, j) for i in range(20) for j in range(20)]
buttons = []
score = 0
game_paused = False

class Block:
    def __init__(self, start_pos: tuple, colour=white):
        self.key = start_pos
        self.i, self.j = self.key
        self.colour = colour

    def draw(self):
        pygame.draw.rect(board, self.colour, (self.i*40, self.j*40, block_size, block_size))
        return


    def erase(self):
        pygame.draw.rect(board, bg_colour, (self.i*40, self.j*40, block_size, block_size))
        return
    

class Button:
    def __init__(self, x: int, y: int, text: str, colours: tuple, on_click_function=None, one_press=False):
        self.x = x
        self.y = y
        self.text = text
        self.colour = colours[0]
        self.text_colour = colours[1]
        self.on_click_function = on_click_function
        self.one_press = one_press
        
        # Fill colour
        self.a = self.colour[0]
        self.b = self.colour[1]
        self.c = self.colour[2]

        self.fill_colours = {'normal': self.colour, 
                             'hover' : (max(0, self.a-20), max(0, self.b-20), max(0, self.c-20)),
                             'pressed' : (max(0, self.a-40), max(0, self.b-40), max(0, self.c-40))}
        
        # Button surface
        self.button_surface = pygame.Surface((500, 200))
        self.button_rect = pygame.Rect(self.x, self.y, 500, 200)
        self.button_surf = ariel.render(self.text, True, self.text_colour)
        self.already_pressed = False
    
    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        self.button_surface.fill(self.fill_colours['normal'])
        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_colours['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fill_colours['pressed'])
                if self.one_press:
                    self.on_click_function()
                elif not self.already_pressed:
                    self.on_click_function()
                    self.already_pressed = True
            else:
                self.already_pressed = False
        self.button_surface.blit(self.button_surf, 
                [self.button_rect.width/2 - self.button_surf.get_rect().width/2, 
                self.button_rect.height/2 - self.button_surf.get_rect().height/2
            ])
        screen.blit(self.button_surface, self.button_rect)


snake = [Block((10, 2)), Block((10, 1)), Block((10, 0))]
direction = 'down'


def draw_snake():
    global snake
    for block in snake:
        block.draw()
    
    pygame.draw.rect(board, white, (0, 0, 800, 800), 1)
    screen.blit(board, board_pos)

    return


def move_snake():
    global snake, direction, counter

    first_block = snake[0]
    first_x, first_y = first_block.key
    if direction == 'right':
        new_x, new_y = first_x + 1, first_y
    elif direction == 'left':
        new_x, new_y = first_x - 1, first_y
    elif direction == 'down':
        new_x, new_y = first_x, first_y + 1
    else:
        new_x, new_y = first_x, first_y - 1
    
    new_coords = [(new_x, new_y)] + [(block.i, block.j) for block in snake[:-1]]


    for block in snake:
        block.erase()

    for i in range(len(snake)):
        snake[i].i, snake[i].j = new_coords[i]
        snake[i].key = new_coords[i]

    if counter < 8:
        counter += 1
    else:
        counter = 0

    draw_snake()
    return


def crash():
    global snake

    head = snake[0]
    if head.i > 19 or head.j > 19 or head.i < 0 or head.j < 0:
        return True
    else:
        keys = [block.key for block in snake[3:]]
        if head.key in keys:
            return True
        else:
            return False
        

def add_block():
    global snake

    n = len(snake)
    #Last and second to last keys
    key1, key2 = snake[n-1].key, snake[n-2].key
    x1, y1 = key1
    x2, y2 = key2
    new_x, new_y = 2*x1 - x2, 2*y1 - y2
    new_key = (new_x, new_y)
    block = Block(new_key)
    snake.append(block)
    draw_snake()

    return


def food(key: tuple):
    global counter

    food_block = Block(key, colour=red)
    if counter % 2 == 0:
        food_block.draw()
    else:
        food_block.erase()
        
    return


def choose_key():
    global snake, twenty_set

    snake_keys = [block.key for block in snake]
    for key in snake_keys:
        twenty_set.remove(key)

    output_key = random.sample(twenty_set, 1)[0]
    twenty_set = [(i, j) for i in range(20) for j in range(20)]

    return output_key



def show_score():
    global score
    
    score_value = score_font.render(str(score), 1, red)
    surface = pygame.Surface((100, 60))
    surface.fill(bg_colour)
    screen.blit(surface, score_pos)
    screen.blit(score_value, score_pos)
    return    


def quit():
    pygame.QUIT
    sys.exit()


def start():
    global score, counter, buttons, game_paused
    
    screen.fill(bg_colour)
    board.fill(bg_colour)
    pygame.draw.rect(board, white, (0, 0, 800, 800), 1)
    board_pos = (200, 50)
    screen.blit(board, board_pos)
    score, counter = 0, 0
    buttons = []
    game_paused = False
    generate()

    return

def generate():
    global key, snake, direction

    snake = [Block((10, 2)), Block((10, 1)), Block((10, 0))]
    direction = 'down'
    draw_snake()
    food(key)
    score_str = score_font.render('Score :', 1, red)
    screen.blit(score_str, (20, 30))
    show_score()
    return 

# Main game loop
def game_loop():
    global key, direction, buttons, score, game_paused

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_LEFT and direction != 'right':
                    direction = 'left'
                if event.key == pygame.K_RIGHT and direction != 'left':
                    direction = 'right'
                if event.key == pygame.K_DOWN and direction != 'up':
                    direction = 'down'
                if event.key == pygame.K_UP and direction != 'down':
                    direction = 'up'
                if event.key == pygame.K_TAB:
                    add_block()
        if game_paused is False:  
            move_snake()
            head = snake[0]
            if head.key == key:
                key = choose_key()
                food(key)
                sfx.eats()
                add_block()
                score += 10
                show_score()
            else:
                food(key)
        else:
            None


        if crash() is True:
            screen.fill(bg_colour)

            sfx.crash_sound()
            play_again = Button(400, 300, 'Play Again', (bright_green, white), start)
            quits = Button(400, 500, 'Quit', (red, white), quit)
            buttons.append(play_again)
            buttons.append(quits)
            game_paused = True
            for button in buttons:
                button.process()


        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    key = choose_key()
    generate()
    game_loop()
