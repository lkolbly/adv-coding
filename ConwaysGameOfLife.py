##
## A version of Conway's Game of Life (a cell replication game) in Pygame
## Run with python 3
## Author: Jason Kolbly <jason@rscheme.org>
##


import time
import pygame
import math as m
import os

# Find the current directory
path = os.path.dirname(__file__)

# Decides options based on user text inputs
should_it_preload = input("Do you want to load a premade object? ")
should_it_preload = should_it_preload.lower()

# A bunch of synonyms for "yes"
yes_synonyms = ["y", "yes", "sure", "okay", "fine", "affirmative", "all right", "very well", "of course", "by all means", "certainly", "absolutely", "indeed", "right", "agreed", "roger", "ok", "yeah", "yep", "yup", "okey-dokey", "yea", "aye"]

# Initially set preload_boolean and import_boolean to False
preload_boolean = False
import_boolean = False

# Compare should_it_preload to yes_synonyms
for x in range(len(yes_synonyms)):
    if yes_synonyms[x] in should_it_preload:
        preload_boolean = True
        
# If you aren't preloading, ask if you're importing
if not preload_boolean:
    # Ask if you wan to import
    import_string = input("Do you want to import a file? ")
    
    # Compare the string to yes_synonyms
    for x in range(len(yes_synonyms)):
        if yes_synonyms[x] in import_string:
            import_boolean = True
    
    # If you're not importing, decide on board properties
    if not import_boolean:
        board_width = int(input("What should the board width be? "))
        board_height = int(input("What should the board height be? "))
        tile_size = int(input("How big is each tile? "))

# Defines board and board_live_counts arrays
board = []
board_live_counts = []

# IMPORTANT: ARRAY OF VIABLE OPTIONS TO PRELOAD WITH
preload_options = ["glider", "glider gun", "pentomino"]

# Define preload as empty string
preload = ""

# Save the state as a .txt file with board saved as an array of arrays
def save_state():
    # Ask for name of the save
    save_name = input("What should we save it as? (Don't include an extension, it will automatically be saved with a .txt) ")
    
    # Set the name of the file to include the active directory and the .txt extension
    save_name = os.path.join(path, "Life Data", save_name + ".txt")
    
    # Write to the file
    file = open(save_name,"w+")
    for x in range(board_height):
        file.write(str(board[x]) + "\n")
        
    # Close the file
    file.close()
    
    print ("Game state was saved at: " + save_name)

# Function to wipe to board
def clear_board():
    global board
    global board_live_counts
    global board_width
    global board_height
    
    # Reset board and board_live_counts
    board = []
    board_live_counts = []
    
    # Set board and board_live_counts back to their original state, but full of zeroes
    for x in range(board_height):
        row = []
        for x in range(board_width):
            row.append(0)
        board.append(row)
        board_live_counts.append(row)

# Function to import a file
def import_file():
    global board
    global board_live_counts
    global board_width
    global board_height
    global tile_size
    
    # Ask for filename
    file_name = input("What is the file name? (don't include the extension) ")
    
    # Update filename to include directory and .txt extension
    file_name = os.path.join(path, "Life Data", file_name + ".txt")
    
    # Open file
    file = open(file_name, "r")
    
    # Temporary file to read each line of the file
    lines = file.readlines()
    
    for x in range(len(lines)):
        # Remove the brackets and split into an array
        lines[x].replace("[","")
        lines[x].replace("]","")
        row = lines[x].strip().split(",")
        
        for y in range(len(row)):
            # Remove spaces and brackets, then convert to int
            row[y] = row[y].strip(" ")
            row[y] = row[y].strip("[")
            row[y] = row[y].strip("]")
            
            row[y] = int(row[y])
            
        # Append row to board and board_live_counts
        board.append(row)
        board_live_counts.append(row)
    
    # Close file
    file.close()

    # Set board height and board width, then tile size based on that
    board_height = len(board)
    for x in range(len(board)):
        board_width = len(board[x])
    tile_size = int(700/board_height)
    
    # Start up the game
    initiate()
    
# Occurs when you choose to load a file
def load_option():
    global preload
    global board_height
    global board_width
    global tile_size
    
    # Ask what you want to preload
    while not any(preload_option in preload for preload_option in preload_options):
        preload = input("What do you want to preload? It can be: " +  str(preload_options) + " ")
        preload = preload.lower()
        
    # If chosen "glider gun"
    if "glider gun" in preload:
        # Set board properties, then start game
        board_width = 50
        board_height = 37
        tile_size = 13
        initiate()
        
        # The following build the shape:
        # Leftmost square
        board[5][1] = 1
        board[5][2] = 1
        board[6][1] = 1
        board[6][2] = 1

        # The middle 'C'
        board[3][14] = 1
        board[3][13] = 1
        board[4][12] = 1
        board[5][11] = 1
        board[6][11] = 1
        board[7][11] = 1
        board[8][12] = 1
        board[9][13] = 1
        board[9][14] = 1

        # The middle dot
        board[6][15] = 1

        # The middle arrow thingy
        board[4][16] = 1
        board[5][17] = 1
        board[6][18] = 1
        board[6][17] = 1
        board[7][17] = 1
        board[8][16] = 1

        # The thing that looks kinda like a frog
        board[5][21] = 1
        board[5][22] = 1
        board[4][21] = 1
        board[4][22] = 1
        board[3][21] = 1
        board[3][22] = 1
        board[2][23] = 1
        board[6][23] = 1
        board[6][25] = 1
        board[7][25] = 1
        board[2][25] = 1
        board[1][25] = 1

        # The right square
        board[3][35] = 1
        board[3][36] = 1
        board[4][35] = 1
        board[4][36] = 1
        
    # If glider is chosen
    elif "glider" in preload:
        # Set board properties then start game
        board_width = 20
        board_height = 20
        tile_size = 20
        initiate()
        
        # Build the shape
        board[0][1] = 1
        board[1][2] = 1
        board[2][2] = 1
        board[2][1] = 1
        board[2][0] = 1
    
    # If pentomino is chosen
    elif "pentomino" in preload:
        # Set board properties then start game
        board_width = 100
        board_height = 100
        tile_size = 7
        initiate()
        
        # Build the shape in the middle of the board
        board[49][49] = 1
        board[49][50] = 1
        board[50][49] = 1
        board[51][49] = 1
        board[50][48] = 1

# This function starts the game itself
def initiate():
    global screen
    global white
    global black
    global paused
    global board_width
    global board_height

    # Initiate pygame, then set the size and open the screen with the "PAUSED" caption
    pygame.init()
    size = [board_width*tile_size,board_height*tile_size]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("PAUSED")

    # Set icon, only uncomment if you have the icon.png in "Life Data" in the file one deeper than this one
    #icon_name = os.path.join(path, "Life Data", "icon.png")
    #icon = pygame.image.load(icon_name)
    #pygame.display.set_icon(icon)

    # Pause the game
    paused = True

    # Set the two colors
    white = (255,255,255)
    black = (0,0,0)

    # If you aren't importing, clear the board
    if not import_boolean:
        clear_board()
    
    # Draw the grid
    for x in range(board_width):
        pygame.draw.line(screen, white, [x*tile_size-tile_size, 0], [x*tile_size-tile_size, board_height*tile_size])
        
    for y in range(board_height):
        pygame.draw.line(screen, white, [0, y*tile_size-tile_size], [board_width*tile_size, y*tile_size-tile_size])


# Initiate, unless there's an undefined variable
try:
    initiate()
except NameError:
    pass

# If you're preloading, do that
if preload_boolean:
    load_option()

# If you're importing, do that
if import_boolean:
    import_file()

# Update the entire pygame display
pygame.display.flip()

# Function to draw the board background
def draw_background():
    global board_width
    global board_height
    
    # Fill the screen black
    screen.fill(black)
    
    # Draw the grid
    for x in range(board_width):
        pygame.draw.line(screen, white, [x*tile_size, 0], [x*tile_size, board_height*tile_size])
    for y in range(board_height):
        pygame.draw.line(screen, white, [0, y*tile_size], [board_width*tile_size, y*tile_size])

# This function is called every turn that the game is unpaused
def turn():
    global board_width
    global board_height
    
    # Set board_live_counts to 0
    for x in range(len(board)):
        board_live_counts[x] = [0] * (len(board_live_counts[x]))
    
    # Run for all elements of list, and all elements of sublists
    for x in range(len(board)):
        for y in range(len(board[x])):
            
            # Increase board_live_counts if the tile to the left is alive
            if x > 0:
                if board[x-1][y] == 1:
                    board_live_counts[x][y] += 1
                    
            # Increase board_live_counts if the tile to the right is alive
            if x < len(board)-1:
                if board[x+1][y] == 1:
                    board_live_counts[x][y] += 1
                    
            # Increase board_live_counts if the tile above is alive
            if y > 0:
                if board[x][y-1] == 1:
                    board_live_counts[x][y] += 1
                    
            # Increase board_live_counts if the tile below is alive
            if y < len(board[x])-1:
                if board[x][y+1] == 1:
                    board_live_counts[x][y] += 1
                    
            # Increase board_live_counts if the tile to the bottom right is alive
            if y < len(board[x])-1 and x < len(board)-1:
                if board[x+1][y+1] == 1:
                    board_live_counts[x][y] += 1
                    
            # Increase board_live_counts if the tile to the top right is alive
            if y > 0 and x < len(board)-1:
                if board[x+1][y-1] == 1:
                    board_live_counts[x][y] += 1
                    
            # Increase board_live_counts if the tile to the bottom left is alive
            if y < len(board[x])-1 and x > 0:
                if board[x-1][y+1] == 1:
                    board_live_counts[x][y] += 1
                    
            # Increase board_live_counts if the tile to the top left is alive
            if y > 0 and x > 0:
                if board[x-1][y-1] == 1:
                    board_live_counts[x][y] += 1
    
    # Run for all elements of list and sublists
    for x in range(len(board)):
        for y in range(len(board[x])):
            # Run if tile is alive
            if board[x][y] == 1:
                # If board_live_counts is 2 or 3, the tile will survive
                if board_live_counts[x][y] < 2:
                    board[x][y] = 0
                elif board_live_counts[x][y] <= 3:
                    board[x][y] = 1
                else:
                    board[x][y] = 0
                    
            # Run if the tile is dead
            else:
                # If there are exactly 3 alive neighbors, it comes alive
                if board_live_counts[x][y] == 3:
                    board[x][y] = 1
                    
    # Delay for a tenth of a second
    time.sleep(0.1)

# The main loop
while True:
    for event in pygame.event.get():
        # If the red X is clicked, quit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        # Run if you press a key
        if event.type == pygame.KEYDOWN:
            # Run if you press space
            if event.key == pygame.K_SPACE:
                # It it's already paused, unpause it
                if paused == True:
                    paused = False
                    pygame.display.set_caption("This is Conway's game of life!")
                # If it's unpaused, pause it
                else:
                    pygame.display.set_caption("PAUSED")
                    paused = True
            # Run if you press s, then run save_state function
            if event.key == pygame.K_s:
                save_state()
        
        # Run if you clicked the mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Set mouse_position to the mouse coordinates
            mouse_position = pygame.mouse.get_pos()
            
            # If the mouse is on the map, run
            if mouse_position[0] > 0 and mouse_position[1] > 0 and mouse_position[0] < tile_size*board_width and mouse_position[1] < tile_size*board_height:
                # Get the position of the tile that was clicked
                pressed_location = [int(m.floor(mouse_position[0]/tile_size)),int(m.floor(mouse_position[1]/tile_size))]
                
                # If the pressed location is alive, make it dead
                if board[pressed_location[1]][pressed_location[0]] != 1:
                        board[pressed_location[1]][pressed_location[0]] = 1
                # If the pressed location is dead, make it alive
                else:
                        board[pressed_location[1]][pressed_location[0]] = 0
    
    # If it is unpaused, run the turn function
    if paused == False:
        turn()
    
    # Draw the background
    draw_background()
    
    # Draw the tiles for all list elements and sublists
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == 1:
                pygame.draw.rect(screen, white, [y*tile_size,x*tile_size,tile_size,tile_size])
                
    # Update the display
    pygame.display.update()
