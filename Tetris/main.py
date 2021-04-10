import pygame
import random
 
# creating the class for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main
 
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
 
pygame.font.init()
 
# GLOBALS VARS
s_width = 800      # SCREEN WIDTH
s_height = 700     # SCREEN HEIGHT
play_width = 300   # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30
 
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
 
 
# SHAPE FORMATS
 
S = [['.....',
      '......',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
# index 0 - 6 represent shape
shapes = [S, Z, I, O, J, L, T]
shape_colors =  [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
 
# Piece Class
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
 

def create_grid(locked_positions={}):
    # Locked Position means a piece is no longer moving & it has hit the bottom
    # It is a dict with 'key' as the piece's position and value as the color of the piece
    grid = [[(0, 0, 0) for y in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


# For convering the shape by storing their positions in a list format
def convert_shape_format(shape):
    positions = []
    format_shape = shape.shape[shape.rotation % len(shape.shape)]

    # Here, line is the sub-list of shape and i acts as the index (Ex. [[.....], [..0..], [.00..]])
    for i, line in enumerate(format_shape):     
        row = list(line)
        for j, column in enumerate(row):    # Traversing the sub list and searching for '.' or '0'
            if column == '0':               # If '0' found, add that position in the list
                # Since the shape can move left or right and downwards, so we will add the j and i value to it
                positions.append((shape.x + j, shape.y + i)) 

    for i, pos in enumerate(positions):
        # Move our shape little to left and up ('up', because we want it to start little above the screen)
        positions[i] = (pos[0] - 2, pos[1] - 4)   
        # So, the piece will start to fall from negative coordinate of y
        # Positions is a list of tuples(each tuple with x & y coordinate)
    
    return positions


# To check whether the piece is in a valid position or not (i.e, it should not go out of screen or move over any other piece)
def valid_space(shape, grid):
    # Position will be valid, only if there is no piece (i.e, it will not be a coloured position)
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]   
    # Deleting the sub-list from the list
    accepted_pos = [j for sub in accepted_pos for j in sub]          

    formatted = convert_shape_format(shape)    # We will receive a list of positions 

    for pos in formatted:
        if pos not in accepted_pos:
            # Checking if the y value is in the valid position (i.e, while falling it is in valid position or not)
            if pos[1] > -1:   
                return False
    return True


# Check if the piece is lost or not (i.e. out of screen)
def check_lost(positions):
    for pos in positions:
        x, y = pos
        # If a piece is out of the screen, it is lost
        if y < 1:          
            return True
    return False

 
# GIVES US A RANDOM SHAPE FROM THE SHAPES LIST (or 'Object' of Piece class)
def get_shape():                         
    return Piece(5, 0, random.choice(shapes))            

 
#  For Displaying the starting and ending text
def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont("Comic Sans MS", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))


# FUNCTION FOR DRAWING THE GRID OF THE PLAY AREA
def draw_grid(surface, grid):           
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        # Draws the horizontal grid lines
        pygame.draw.line(surface, (18, 128, 128), (sx, sy + i*block_size), (sx+play_width, sy + i*block_size)) 
        
        for j in range(len(grid[i])):
            # Draws the vertical grid lines
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy), (sx + j*block_size, sy+play_height))  



# Clears the full row (if it gets filled)
def clear_rows(grid, locked):
    inc = 0
    # Traverse the grid from downwards to upwards
    for i in range(len(grid)-1, -1, -1):      
        row = grid[i]
        # If there is no black area (i.e. empty space) in the row
        if (0, 0, 0) not in row:         
            inc += 1
            index = i
            for j in range(len(row)):
                try:
                    # Delete the whole row (i.e. remove the locked postions of that row)
                    del locked[(j, i)]   
                except:
                    continue
    
    # Now shifting the above rows down
    if inc > 0:
        # We have to get the locked positions from down to up in sorted order
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:  
            x, y = key
            if y < index:          
                newkey = (x, y + inc)
                # Changing the y coordinate of the up locked position and shifting its coordinate and color down
                locked[newkey] = locked.pop(key)  
    
    return inc      # Used to increment score



# Draws next shape on right side of the play window
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("Comic Sans MS", 30)
    label1 = font.render('Next Shape', 1, (255, 255, 255))
    
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    
    format_shape = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format_shape):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + sy - i*block_size - 150, block_size, block_size), 0)
    
    surface.blit(label1, (sx, sy))


# Function to update the high score in the text file
def update_score(nscore):
    score = max_score()

    with open("scores.txt", 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


# Function to get the max score from the text file
def max_score():
    with open("scores.txt", 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


# SETS UP THE WHOLE WINDOW
def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))        # Gives our screen Black Background color

    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), 20))   # Draws the text onto the window

    # Display score
    font = pygame.font.SysFont("Comic Sans MS", 28)
    label2 = font.render('Score: ' + str(score), 1, (255, 255, 255))
    
    sx = top_left_x - 200
    sy = top_left_y + play_height/2 - 40

    surface.blit(label2, (sx, sy))

    # Display max score
    font = pygame.font.SysFont("Comic Sans MS", 28)
    label2 = font.render('High Score: ' + str(last_score), 1, (255, 255, 255))
    
    sx = top_left_x - 230
    sy = top_left_y + play_height/2 - 150

    surface.blit(label2, (sx, sy))

    # Drawing of grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)  
    
    # Play area border
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)  

    draw_grid(surface, grid)
 

# Main Block
def main(win):
    last_score = max_score()

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True

    current_piece = get_shape()      # Receives a Piece class object
    next_piece = get_shape()         # Receives a Piece class object

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0  
    score = 0

    while run:
        # Updating the grid, because the locked positions will change after each piece goes down
        grid = create_grid(locked_positions)   
        # Actual time of the previous tick (in milliseconds)
        fall_time += clock.get_rawtime()       
        level_time += clock.get_rawtime()
        # Computes the time each iteration took (then in next iteration, add it to the fall_time)
        clock.tick()                          
        # This will make the game to run at same speed in every machine

        if level_time/1000 > 5:     # Increase speed in every 5 sec
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        # With every change of frame (or new iteration) the piece will move down
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            # Check for valid position
            if not(valid_space(current_piece, grid) and current_piece.y > 0):
                current_piece.y -= 1
                change_piece = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            
            if event.type == pygame.KEYDOWN:       # CHECKS ALL THE KEY PRESS EVENTS (i.e WHAT ALL KEYS ARE PRESSED)
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1              # MOVES LEFT, WHEN LEFT KEY IS PRESSED
                    
                    # CHECKS IF THE LEFT SIDE IS VALID POSITION OR NOT (i.e. NO BLOCKS ARE THERE ON LEFT)
                    if not(valid_space(current_piece, grid)):   
                        current_piece.x += 1             # IF IT IS NOT VALID POSITION, THEN THE BLOCK WILL NOT MOVE LEFT

                elif event.key == pygame.K_RIGHT:   
                    current_piece.x += 1              # MOVES RIGHT, WHEN RIGHT KEY IS PRESSED

                    # CHECKS IF THE RIGHT SIDE IS VALID POSITION OR NOT (i.e. NO BLOCKS ARE THERE ON RIGHT)
                    if not(valid_space(current_piece, grid)):   
                        current_piece.x -= 1             # IF IT IS NOT VALID POSITION, THEN THE BLOCK WILL NOT MOVE RIGHT

                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1        # ROTATE THE CURRENT SHAPE, WHEN UP KEY IS PRESSED 

                    if not(valid_space(current_piece, grid)):   # CHECKS IF AFTER ROTATION THE SPACE IS VALID OR NOT
                        current_piece.rotation -= 1      # IF IT IS NOT VALID POSITION, THEN THE BLOCK WILL NOT CHANGE THE SHAPE

                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1            # MOVES DOWN, WHEN DOWN KEY IS PRESSED

                    # CHECKS IF THE DOWN SIDE IS VALID POSITION OR NOT (i.e. NO BLOCKS ARE THERE BELOW)
                    if not(valid_space(current_piece, grid)):   
                        current_piece.y -= 1          # IF IT IS NOT VALID POSITION, THEN THE BLOCK WILL NOT MOVE DOWN
        
        
        shape_pos = convert_shape_format(current_piece)

        # Show color on the screen (corresponding the piece) 
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # If change piece is True, we have to update the locked positions (because the piece might have hit the bottom)
        if change_piece:        
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece      # Updating the current piece with next piece
            next_piece = get_shape()
            change_piece = False

            # Calling clear rows function, only when a piece hits the bottom
            score += clear_rows(grid, locked_positions) * 10   

        
        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # If the locked positions start to move out of the screen (i.e. while getting stacked over one another)
        if check_lost(locked_positions):
            win.fill((0,0,0))
            draw_text_middle("YOU LOST!", 80, (255, 255, 255), win)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False
            update_score(score) 


def main_menu(win):
    run = True

    while(run):
        win.fill((0, 0, 0))
        draw_text_middle("Press any key to Play", 60, (255, 255, 255), win)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


# Initialises a screen/window for display
win = pygame.display.set_mode((s_width, s_height))   
# Sets the display window caption    
pygame.display.set_caption('Tetris')                 

main_menu(win)                               # Start Game