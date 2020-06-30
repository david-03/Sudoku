import pygame
import random

# Initialize pygame
pygame.init()

# Constant variables (size of everything)
BIG_BAR = 20
SMALL_BAR = 5
TEXT_SPACING = 400
V_SPACING = 50
ICON_SPACING = 25
PANEL_SPACING = 20
CIRCLE = 45
CIRCLE_RADIUS = 20
CIRCLE_SPACING = 64
ICON_SIZE_1 = (64, 64)
ICON_SIZE_2 = (72, 72)
CLOSE = (50, 30)
SLIDER_LEN = 200
SLIDER_RAD = 10
# Colors
BACKGROUND_ALPHA = 200
BLACK = (0, 0, 0)
GRAY = (32, 32, 32)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PALE_RED = (255, 175, 175)
PALE_GREEN = (175, 255, 175)
PALE_BLUE = (175, 175, 255)
BLUE1 = (0, 110, 255)
YELLOW = (255, 255, 0)
PURPLE = (150, 0, 255)
GOLD = (-1, -1, -1)
COLOR_MULTIPLIER = 5
# Color name of each confetti
CONFETTI_COLORS = ["blue", "dark_green", "green", "orange", "pink", "red", "yellow", "teal"]
CONFETTI_LENGTH = 150
CONFETTI_MULTIPLIER = 10
Y_SPEED = 8
confetti_pos = []
confetti_speed = []
# Fonts
FONT_72 = pygame.font.Font("data\\Bauhaus 93 Regular.ttf", 72)
FONT_75 = pygame.font.Font("data\\Bauhaus 93 Regular.ttf", 75)
TEXT_FONT_48 = pygame.font.Font("data\\agency-fb.ttf", 48)
TEXT_FONT_64 = pygame.font.Font("data\\agency-fb.ttf", 64)
TEXT_FONT_72 = pygame.font.Font("data\\agency-fb.ttf", 72)
TEXT_FONT_84 = pygame.font.Font("data\\agency-fb.ttf", 84)
# Keep track of how many times solve function has been called
MAX_ITERATIONS = 500_000
iterations = 0
# Easy way to stop recursive function
showing = False
# Keep track of congratulations colors
color_0 = 0
color_1 = 0
color_2 = 0

# User's monitor dimensions
MON_W = pygame.display.Info().current_w
MON_H = pygame.display.Info().current_h

# Load background image
BACKGROUND = pygame.image.load("data\\background.jpg")
# Get width
bg_w = BACKGROUND.get_width()
bg_h = BACKGROUND.get_height()
# Adjust image based on user's monitor's aspect ratio
if bg_w / bg_h <= MON_W / MON_H:
    BACKGROUND = pygame.transform.scale(BACKGROUND, (MON_W, MON_W * bg_h // bg_w))
else:
    BACKGROUND = pygame.transform.scale(BACKGROUND, (MON_H * bg_w // bg_h, MON_H))

# Dimensions of each square based on monitor aspect ratio
if MON_W > MON_H - 2 * V_SPACING + TEXT_SPACING:
    SQUARE = (MON_H - 2 * V_SPACING) // 9
else:
    SQUARE = (MON_W - TEXT_SPACING - 2 * V_SPACING) // 9

# Top left position of grid
X = (MON_W - TEXT_SPACING - 9 * SQUARE) // 2
Y = (MON_H - 9 * SQUARE) // 2

# Make regular cursor invisible
pygame.mouse.set_visible(False)

# Load cursor
cursor = pygame.transform.scale(pygame.image.load("data\\cursor.png"), (32, 32))
# Load bar image
bar = pygame.image.load("data\\bar.png")
# Load blue square
blue_square = pygame.transform.scale(pygame.image.load("data\\frame.png"), (int(5 / 4 * SQUARE), int(5 / 4 * SQUARE)))
# Load red square
red_square = pygame.transform.scale(pygame.image.load("data\\frame_red.png"), (int(5 / 4 * SQUARE), int(5 / 4 * SQUARE)))
# Load gold circle
gold_circle = pygame.transform.scale(pygame.image.load("data\\gold.png"), (2 * CIRCLE_RADIUS, 2 * CIRCLE_RADIUS))
# Load gold paint image
gold_paint = pygame.transform.scale(pygame.image.load("data\\gold_paint.png"), (100, 50))
white_paint = pygame.transform.scale(pygame.image.load("data\\white_paint.png"), (120, 60))
# Load clock
clock_img = pygame.transform.scale(pygame.image.load("data\\clock.png"), ICON_SIZE_1)

# Create dynamic variables to load all the number png (I know, I know, fancy as fuck)
for n in range(1, 10):
    # Create variable name (num1, num2, ..., num9)
    var_name = "num_{0}".format(n)
    # File location (data\\1.png)
    loc = "data\\{0}.png".format(n)
    # Assign global variable to a pygame image object
    # globals() is a function that returns a dictionary containing all the global variables of the program as keys and
    # the values of each key is the value assigned to the variable. By doing it this way, I can create variable names as
    # general strings and assign their value dynamically.
    globals()[var_name] = pygame.transform.scale(pygame.image.load(loc), (SQUARE // 2, SQUARE // 2))

# Create dynamic variables to load all the confetti images
for n in CONFETTI_COLORS:
    # Create variable name
    var_name = "{0}_confetti".format(n)
    # File location (data\\1.png)
    loc = "data\\{0}.png".format(var_name)
    # Assign global variable to a pygame image object
    globals()[var_name] = pygame.image.load(loc)

# Store every line in file into "data" list
with open("data\\sudoku.txt", "r") as file:
    data = file.readlines()


def random_confetti():
    global confetti_pos, confetti_speed
    # Reset all the confettis' position and speed
    confetti_pos = []
    confetti_speed = []
    # How many confettis of each color to generate
    for j in range(CONFETTI_MULTIPLIER):
        # Do for each color of confetti
        for i, color in enumerate(CONFETTI_COLORS):
            # Create new variable name based on confetti number
            variable_name = "{0}_confetti".format(color)
            new_var_name = "{0}_confetti_{1}".format(color, i + j * len(CONFETTI_COLORS))
            globals()[new_var_name] = pygame.transform.scale(globals()[variable_name], (CONFETTI_LENGTH-i * 10,
                                                                                        (CONFETTI_LENGTH - i * 10) // 2))
            # Create random start position
            x = random.randint(MON_W // 2 - 5 * SQUARE, MON_W // 2 + 4 * SQUARE)
            y = - random.randint(CONFETTI_LENGTH // 2, CONFETTI_LENGTH + 9 * SQUARE)
            # Append its position to list
            confetti_pos.append([x, y])
            # Random horizontal speed
            x_speed = random.randint(-20, 20) / 10
            confetti_speed.append(x_speed)
            # Random rotation
            globals()[new_var_name] = pygame.transform.rotate(globals()[new_var_name], random.randint(-45, 45))


def confetti(win):
    # Do for each confetti
    for j in range(CONFETTI_MULTIPLIER):
        for i, color in enumerate(CONFETTI_COLORS):
            # Update index
            i += j * len(CONFETTI_COLORS)
            # Do not do anything once confetti is lower than screen bottom
            if confetti_pos[i][1] <= MON_H:
                # Get confetti from global variables dictionary
                variable_name = "{0}_confetti_{1}".format(color, i)
                # Draw confetti at its position
                win.blit(globals()[variable_name], (round(confetti_pos[i][0]), round(confetti_pos[i][1])))
                # Change its position based on its speed
                confetti_pos[i][0] += confetti_speed[i]
                confetti_pos[i][1] += Y_SPEED


def empty_board():
    # Creates an empty board and appends 9 empty rows into it
    board1 = []
    for _ in range(9):
        board1.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    return board1


def load_board(name):
    # Starting line depends on board or user board
    if name == "board":
        start = 1
    else:
        start = 11
    # Create temporary empty board
    board1 = []
    for line in range(9):
        row = []
        # Take each number by itself
        for num in data[start + line].split(" "):
            if num != '\n':
                row.append(int(num))
        board1.append(row)
    return board1


def save_board(ind, board1):
    # Iterate through the 9 rows
    for i in range(9):
        temp_str = ""
        # For each number inside the row
        for num in board1[i]:
            # Add to temporary string
            temp_str += "{0} ".format(str(num))
        # At the end of the string, add \n
        temp_str += "\n"
        data[i + ind] = temp_str


def save_line(ind, item):
    data[ind] = str(item) + "\n"


def load_color(ind):
    color = []
    for rgb in data[ind].split(" "):
        if rgb != '\n':
            color.append(int(rgb))
    return color


def save_color(ind, color):
    temp_str = ""
    # For each number inside the row
    for num in color:
        # Add to temporary string
        temp_str += "{0} ".format(str(num))
    save_line(ind, temp_str)


def save_game(board1, user1, add_time, difficulty, board_color, user_color):
    # Save the two boards
    save_board(1, board1)
    save_board(11, user1)
    # Save time
    save_line(21, add_time)
    # Save difficulty
    save_line(23, difficulty)
    # Save board color
    save_color(35, board_color)
    # Save user color
    save_color(37, user_color)
    # Write data to file
    with open("data\\sudoku.txt", "w") as file1:
        for item in data:
            file1.write(item)


def time_format(time):
    if len(str(time)) == 1:
        time = "0{0}".format(time)
    else:
        time = str(time)
    return time


def get_time(initial_ticks, added_seconds):
    # Number of milliseconds after pygame.init() was called
    current_ticks = pygame.time.get_ticks()
    # Total number of seconds
    seconds = (current_ticks - initial_ticks) // 1000 + added_seconds
    # Total number of minutes
    minutes = seconds // 60
    # Total number of hours
    hours = minutes // 60
    # Number of minutes minus all the hours
    minutes -= 60 * hours
    # Number of seconds minus all the hours and minutes
    seconds -= 60 * minutes + 3600 * hours
    return [hours, minutes, seconds]


def close_button(win, color):
    # Create rectangle
    close_rect = pygame.rect.Rect((MON_W - CLOSE[0], 0), (CLOSE[0], CLOSE[1]))
    # Draw rectangle based on color
    pygame.draw.rect(win, color, close_rect)
    # Draw white X
    pygame.draw.line(win, WHITE, (MON_W - 30, 10), (MON_W - 20, 20))
    pygame.draw.line(win, WHITE, (MON_W - 30, 20), (MON_W - 20, 10))


def draw_grid(win):
    # Horizontal bars
    h_big_bar = pygame.transform.scale(bar, (9 * SQUARE, BIG_BAR))
    h_small_bar = pygame.transform.scale(bar, (9 * SQUARE, SMALL_BAR))
    # Vertical bars
    v_big_bar = pygame.transform.rotate(h_big_bar, 90)
    v_small_bar = pygame.transform.rotate(h_small_bar, 90)
    # Upper left corner of grid
    left_x = X
    upper_y = Y
    # Transparent background cover
    cover = pygame.Surface((9 * SQUARE, 9 * SQUARE))
    cover.set_alpha(BACKGROUND_ALPHA)
    cover.fill(BLACK)
    win.blit(cover, (left_x, upper_y))

    # Draw all horizontal bars
    for i in range(10):
        # Draw a thick bar every three bars
        if i % 3 == 0:
            win.blit(h_big_bar, (left_x, upper_y + i * SQUARE - BIG_BAR // 2))
        else:
            win.blit(h_small_bar, (left_x, upper_y + i * SQUARE - SMALL_BAR // 2))
    # Draw all vertical bars
    for j in range(10):
        # Draw a thick bar every three bars
        if j % 3 == 0:
            win.blit(v_big_bar, (left_x + j * SQUARE - BIG_BAR // 2, upper_y))
        else:
            win.blit(v_small_bar, (left_x + j * SQUARE - SMALL_BAR // 2, upper_y))


def get_pos(col, row):
    # Calculate pixel position of any column and row combination
    x = X + col * SQUARE
    y = Y + row * SQUARE
    return int(x), int(y)


def get_mouse(mouse_x, mouse_y):
    # Check if mouse is in grid
    if X <= mouse_x <= X + 9 * SQUARE and Y <= mouse_y <= Y + 9 * SQUARE:
        # Calculate column, row of mouse
        col = (mouse_x - X) // SQUARE
        row = (mouse_y - Y) // SQUARE
        return col, row
    return None


def move_selected(board1, selected, x_or_y, move):
    # Loop until program finds an empty spot in board
    while True:
        # If it goes out of the board
        if selected[x_or_y] == 0 and move < 0:
            selected[x_or_y] = 8
        elif selected[x_or_y] == 8 and move > 0:
            selected[x_or_y] = 0
        else:
            selected[x_or_y] += move
        # If spot is empty, stop the loop
        if board1[selected[1]][selected[0]] == 0:
            break
    return selected


def draw_num(win, digit, row, col, color):
    # Get pixel position of the column, row combination
    col1, row1 = get_pos(col, row)
    # Adjust digit spacing
    col1 += int(SQUARE // 3)
    row1 += int(SQUARE // 8)
    # Background text to add contrast
    bg_text = FONT_75.render(str(abs(digit)), True, BLACK)
    text = FONT_72.render(str(abs(digit)), True, color)
    # Draw colored digit
    win.blit(bg_text, (col1, row1))
    win.blit(text, (col1, row1))


def draw_numbers(win, board1, color, correcting=False, incorrect=None):
    # Check each row and column
    for row in range(len(board1)):
        for col in range(len(board1[row])):
            # Get digit stored in board
            digit = board1[row][col]
            # Do not draw digit if it's 0
            if digit != 0:
                # Get pixel position of the column, row combination
                col1, row1 = get_pos(col, row)
                # If no color is specified, use the images of the different digits
                if color[0] == -1 and not correcting:
                    # Adjust digit spacing
                    col1 += int(SQUARE // 4)
                    row1 += int(SQUARE // 4)
                    # Create variable name
                    img = "num_{0}".format(abs(digit))
                    # Draw image
                    win.blit(globals()[img], (col1, row1))
                else:
                    # Change the color of the digits if the player wants to correct his input
                    if correcting and digit > 0:
                        color = GREEN
                    elif correcting and digit < 0:
                        color = RED
                    # Adjust digit spacing
                    col1 += int(SQUARE // 3)
                    row1 += int(SQUARE // 8)
                    # Background text to add contrast
                    bg_text = FONT_75.render(str(abs(digit)), True, BLACK)
                    text = FONT_72.render(str(abs(digit)), True, color)
                    # Draw colored digit
                    win.blit(bg_text, (col1, row1))
                    win.blit(text, (col1, row1))
    # Draw correct number in top right corner for all incorrect user numbers
    if incorrect:
        for (row, col) in incorrect:
            # Extract digit from dictionary
            digit = incorrect[(row, col)]
            # Get pixel position of the column, row combination
            col1, row1 = get_pos(col, row)
            # Adjust digit spacing so that the digit is in the top right corner
            col1 += int(3 * SQUARE // 4)
            row1 -= int(SQUARE // 16)
            # Background text to add contrast
            bg_text = TEXT_FONT_64.render(str(abs(digit)), True, BLACK)
            text = TEXT_FONT_64.render(str(abs(digit)), True, PURPLE)
            # Draw colored digit
            win.blit(bg_text, (col1, row1))
            win.blit(text, (col1, row1))


# Color selection panel
def select_color(win, board_color, user_color, click, selection, selected_slider=None):
    temp_colors = [board_color, user_color]
    # Calculate dimensions and position of panel
    color_box_w = TEXT_SPACING - (2 * PANEL_SPACING)
    color_box_h = 5 * TEXT_SPACING // 8
    color_box_x = X + (9 * SQUARE + 2 * PANEL_SPACING)
    color_box_y = Y + PANEL_SPACING
    # Transparent background cover
    cover = pygame.Surface((color_box_w, color_box_h))
    cover.set_alpha(BACKGROUND_ALPHA)
    cover.fill(BLACK)
    win.blit(cover, (color_box_x, color_box_y))

    # Draw metal bar frame
    # Horizontal and vertical bars
    h_bar = pygame.transform.rotate(pygame.transform.scale(bar, (color_box_w, BIG_BAR)), 180)
    v_bar = pygame.transform.rotate(pygame.transform.scale(h_bar, (color_box_h, BIG_BAR)), -90)
    win.blit(h_bar, (color_box_x + 5, color_box_y))
    win.blit(h_bar, (color_box_x + 5, color_box_y + color_box_h - BIG_BAR // 2))
    win.blit(v_bar, (color_box_x - BIG_BAR // 2, color_box_y + 5))
    win.blit(v_bar, (color_box_x + color_box_w, color_box_y + 5))

    # Calculate position of circle
    circle_x = X + 9 * SQUARE + CIRCLE_SPACING
    circle_y = Y + 3 * CIRCLE_SPACING // 2
    circle_center = gold_circle.get_rect().centerx
    # Draw background white circle and black circle behind current selected color
    pygame.draw.circle(win, WHITE, (circle_x + circle_center, circle_y + selection * CIRCLE_SPACING + circle_center),
                       4 * CIRCLE_RADIUS // 3)
    pygame.draw.circle(win, BLACK, (circle_x + circle_center, circle_y + selection * CIRCLE_SPACING + circle_center),
                       CIRCLE_RADIUS + 2)
    # For both boards
    for i in range(2):
        # Draw gold circle
        if temp_colors[i][0] == -1:
            win.blit(gold_circle, (circle_x, circle_y + i * CIRCLE_SPACING))
            if selection == i:
                # Draw white paint background
                win.blit(white_paint, (color_box_x + 145, color_box_y + 20))
        # Draw colored circle
        else:
            pygame.draw.circle(win, (temp_colors[i][0], temp_colors[i][1], temp_colors[i][2]),
                               (circle_x + circle_center, circle_y + circle_center + i * CIRCLE_SPACING), CIRCLE_RADIUS)

        if selection == i:
            temp_colors[i], selected_slider = draw_sliders(win, temp_colors[i], selected_slider, click=click)

        if temp_colors[i][0] + temp_colors[i][1] + temp_colors[i][2] < 30:
            temp_colors[i] = [-1, -1, -1]

    # Draw gold paint image
    win.blit(gold_paint, (color_box_x + 150, color_box_y + 25))

    # Check if user clicked
    if click and not selected_slider:
        if circle_x + 2 * CIRCLE_RADIUS >= click[0] >= circle_x:
            if circle_y + 2 * CIRCLE_RADIUS >= click[1] >= circle_y:
                selection = 0
            elif circle_y + 2 * CIRCLE_RADIUS + CIRCLE_SPACING >= click[1] >= circle_y + CIRCLE_SPACING:
                selection = 1
        else:
            gold_rect = gold_paint.get_rect(topleft=(color_box_x + 150, color_box_y + 25))
            # If click on gold paint, change color value to -1
            if gold_rect.collidepoint(click[0], click[1]):
                temp_colors[selection] = [-1, -1, -1]

    click = None

    return temp_colors[0], temp_colors[1], selection, click, selected_slider


def draw_sliders(win, color, selected_slider=None, click=None):
    # If gold, draw sliders as black (0, 0, 0)
    if color[0] == -1:
        color = [0, 0, 0]
    # Do for each slider
    for i, name in enumerate(["RED", "GREEN", "BLUE"]):
        # Calculate slider position
        slider_x = X + 9 * SQUARE + 160
        slider_y = Y + 150 + i * 40
        # If user has mouse down
        if click:
            # If a slider is already selected (slider number 1 to 3) and mouse x position on slider
            if selected_slider and slider_x <= click[0] <= slider_x + SLIDER_LEN:
                # Change color according to ratio of slider circle position on slider total length
                color[selected_slider - 1] = round((click[0] - slider_x) / SLIDER_LEN * 255)
            # If no slider is currently selected and click is on slider
            elif not selected_slider and slider_x <= click[0] <= slider_x + SLIDER_LEN and \
                    slider_y - SLIDER_RAD // 2 <= click[1] <= slider_y + SLIDER_RAD // 2:
                # Select slider and change color
                selected_slider = i + 1
                color[i] = round((click[0] - slider_x) / SLIDER_LEN * 255)
        # Calculate slider knob position
        slider_circle_x = round(SLIDER_LEN * color[i] / 255) + slider_x
        # Draw opaque line before knob and pale line after knob
        pygame.draw.line(win, globals()[name], (slider_x, slider_y), (slider_circle_x, slider_y), width=SLIDER_RAD // 2)
        pygame.draw.line(win, globals()["PALE_{0}".format(name)], (slider_circle_x, slider_y), (slider_x + SLIDER_LEN, slider_y),
                         width=SLIDER_RAD // 2)
        # Draw knob
        pygame.draw.circle(win, globals()[name], (slider_circle_x, slider_y), SLIDER_RAD)

    return color, selected_slider


def check_num(board1, num1, row, col):
    # Check if number is already in its own row
    for col_num in range(9):
        if num1 == board1[row][col_num] and col_num != col and num1 != 0:
            return False
    # Check if number is already in its own column
    for row_num in range(9):
        if num1 == board1[row_num][col] and row_num != row and num1 != 0:
            return False

    # Check which 3x3 square the row, col combination belongs to
    square_row = row // 3
    square_col = col // 3
    # Check if number is already in its own 3x3 square
    for i in range(9):
        for j in range(9):
            if i // 3 == square_row and j // 3 == square_col:
                if board1[i][j] == num1 and (i, j) != (row, col) and num1 != 0:
                    return False
    return True


def check_solvable(user1):
    # Create empty board
    board1 = empty_board()
    # Copy user board into empty board
    for row in range(9):
        for col in range(9):
            board1[row][col] = user1[row][col]
    # Check if it is solvable
    for row in range(9):
        for col in range(9):
            if not check_num(board1, board1[row][col], row, col):
                return None
    if solve(board1):
        for row in range(9):
            for col in range(9):
                if user1[row][col] != 0:
                    board1[row][col] = 0
    else:
        return None
    return board1


def show_solve(win, user1, temp_board=None, text_x=None, text_y=None):
    global showing
    if not showing:
        return False
    if not temp_board:
        # Create temporary board
        temp_board = empty_board()
        # Copy everything from user1 to temp_board
        for row in range(9):
            for col in range(9):
                temp_board[row][col] = user1[row][col]
        # Calculate text position
        text_x = X + 9 * SQUARE + TEXT_SPACING // 4
        text_y = 3 * MON_H // 8
    # Check if there are empty positions
    for row in range(9):
        for col in range(9):
            # If there is an empty position
            if temp_board[row][col] == 0:
                # Try a number from 1 to 9
                for num1 in range(1, 10):
                    # Draw background image and grid
                    draw_bg(win)
                    draw_grid(win)

                    # Draw text
                    solving_text = TEXT_FONT_64.render("Solving...", True, YELLOW)
                    exit_text = TEXT_FONT_48.render("Press any key", True, YELLOW)
                    exit_text_2 = TEXT_FONT_48.render("to exit", True, YELLOW)
                    win.blit(solving_text, (text_x, text_y))
                    win.blit(exit_text, (text_x, text_y + 100))
                    win.blit(exit_text_2, (text_x, text_y + 100 + 64))

                    # Draw user numbers
                    draw_numbers(win, user1, GOLD)

                    for i in range(9):
                        for j in range(9):
                            # Draw new generated numbers in blue
                            if temp_board[i][j] != user1[i][j] and temp_board[i][j] != 0 and (i, j) != (row, col):
                                draw_num(win, temp_board[i][j], i, j, BLUE1)

                    # Draw the number that the system is trying in yellow
                    draw_num(win, num1, row, col, YELLOW)

                    # Get pixel position of selected column and row
                    square_x, square_y = get_pos(col, row)
                    # Add a little bit of offset
                    square_x -= SQUARE // 8
                    square_y -= SQUARE // 8
                    win.blit(blue_square, (square_x, square_y))
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                            showing = False

                    # If the number is valid
                    if check_num(temp_board, num1, row, col):
                        # Replace empty space with number
                        temp_board[row][col] = num1
                        # Try to solve the board
                        if show_solve(win, user1, temp_board=temp_board, text_x=text_x, text_y=text_y):
                            # If solved (no empty positions left), return True
                            return True
                        # If the board can't be solved, change the number back to 0 and try again
                        temp_board[row][col] = 0
                    # If the number is not valid, the for loop repeats
                    # Draw the number that the system got wrong in red
                    draw_num(win, num1, row, col, RED)
                    # Draw red frame
                    win.blit(red_square, (square_x, square_y))
                    pygame.display.flip()

                # If none of the numbers from 1 to 9 are valid, the board can't be solved
                return False
    # If no empty positions, board is solved
    return True


def solve(board1, recursed=False):
    # Keep track of iterations
    global iterations
    # Reset number of iterations only if the function is not called recursively
    if not recursed:
        iterations = 0
    # Return False right away if too many iterations
    if iterations > MAX_ITERATIONS:
        return False
    # Check if there are empty positions
    for row in range(9):
        for col in range(9):
            # If there is an empty position
            if board1[row][col] == 0:
                # Try a number from 1 to 9
                for num1 in range(1, 10):
                    iterations += 1
                    # If the number is valid
                    if check_num(board1, num1, row, col):
                        # Replace empty space with number
                        board1[row][col] = num1
                        # Try to solve the board
                        if solve(board1, recursed=True):
                            # If solved (no empty positions left), return True
                            return True
                        # If the board can't be solved, change the number back to 0 and try again
                        board1[row][col] = 0
                    # If the number is not valid, the for loop repeats

                # If none of the numbers from 1 to 9 are valid, the board can't be solved
                return False

    # If no empty positions, board is solved
    return True


def generate():
    # Create empty board
    board1 = empty_board()

    # Generate random first row (otherwise the first row would most like be 1 2 3 4 5 6 7 8 9)
    for j in range(9):
        # Generate random valid number for each column
        while True:
            num1 = random.randint(1, 9)
            if check_num(board1, num1, 0, j):
                board1[0][j] = num1
                break

    # Generate 9 other random numbers
    for _ in range(9):
        # Find random empty space
        while True:
            row_num = random.randint(0, 8)
            col_num = random.randint(0, 8)
            if board1[row_num][col_num] == 0:
                break
        # Generate random valid number in that empty space
        while True:
            num1 = random.randint(1, 9)
            if check_num(board1, num1, row_num, col_num):
                board1[row_num][col_num] = num1
                break
    # Solve the board for the rest of the numbers
    if solve(board1):
        return board1
    # If the previous board could not be solved, call the function again
    return generate()


def final_check(board1, user1):
    # Create temporary empty board
    temp_board = empty_board()
    # Copy all then numbers from board and from user board to temporary board
    for row in range(9):
        for col in range(9):
            if board1[row][col] != 0:
                temp_board[row][col] = board1[row][col]
            elif user1[row][col] != 0:
                temp_board[row][col] = abs(user1[row][col])
    for row in range(9):
        for col in range(9):
            # If there are still empty squares, user did not complete sudoku
            if temp_board[row][col] == 0:
                return False
            # If any number does not respect sudoku rules, user did not successfully complete sudoku
            if not check_num(temp_board, temp_board[row][col], row, col):
                return False
    # If user passes all the tests, it confirms that he did complete the puzzle successfully
    return True


def draw_bg(win):
    # Get center of rectangle around background image and set it to correspond to center of user's monitor
    bg_rect = BACKGROUND.get_rect(center=(MON_W // 2, MON_H // 2))
    # Use rectangle upper left position to draw image so that the center of the monitor is the center of the image
    win.blit(BACKGROUND, (bg_rect.x, bg_rect.y))


def playing_text(win, text, color, height, m_x, m_y, icon_name, selected=False):
    # Calculate text x position
    text_x = X + 9 * SQUARE + TEXT_SPACING // 3
    # Render background text and foreground text
    txt_bg = TEXT_FONT_64.render(text, True, BLACK)
    txt = TEXT_FONT_64.render(text, True, color)
    # Draw text
    win.blit(txt_bg, (text_x + 3, height + 3))
    win.blit(txt, (text_x, height))
    # Load icon
    icon_img = pygame.transform.scale(pygame.image.load("data\\{0}.png".format(icon_name)), ICON_SIZE_1)
    # If not selected
    if not selected:
        # Draw regular icon
        icon_x = text_x - ICON_SIZE_1[0] - ICON_SPACING
        icon_y = height + (txt.get_height() - ICON_SIZE_1[0]) // 2 + 10
        win.blit(icon_img, (icon_x, icon_y))
        # Check if mouse is hovering over icon
        hovering = icon_img.get_rect(topleft=(icon_x, icon_y)).collidepoint(m_x, m_y)
    else:
        icon_pos = (text_x - ICON_SIZE_1[0] - ICON_SPACING, height + (txt.get_height() - ICON_SIZE_2[0]) // 2 + 10)
        # Draw yellow circle behind
        pygame.draw.circle(win, YELLOW, (icon_pos[0] + ICON_SIZE_2[0] // 2, icon_pos[1] + ICON_SIZE_2[1] // 2), CIRCLE)
        # Draw bigger icon
        icon_img = pygame.transform.scale(icon_img, ICON_SIZE_2)
        win.blit(icon_img, icon_pos)
        hovering = True
    return txt, hovering


def menu_text(win, text, color, height):
    # Draw text with black background, centered in the screen, at the given height
    txt_bg = TEXT_FONT_72.render(text, True, BLACK)
    txt = TEXT_FONT_72.render(text, True, color)
    win.blit(txt_bg, (MON_W // 2 - txt_bg.get_width() // 2 + 4, height + 4))
    win.blit(txt, (MON_W // 2 - txt.get_width() // 2, height))
    return txt


def menu(win, text_1, text_2, text_3):
    menu_clock = pygame.time.Clock()
    while True:
        # 80 FPS
        menu_clock.tick(80)

        # Draw background
        draw_bg(win)
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Display text
        new_txt = menu_text(win, text_1, BLUE1, MON_H // 3)
        prev_txt = menu_text(win, text_2, BLUE1, MON_H // 3 + MON_H // 9)
        solve_txt = menu_text(win, text_3, BLUE1, MON_H // 3 + 2 * MON_H // 9)

        # Temporary variables
        op_1 = False
        op_2 = False
        op_3 = False
        closed = False

        # Change text color is mouse hovers over it
        if MON_W // 2 + new_txt.get_width() // 2 >= mouse_x >= MON_W // 2 - new_txt.get_width() // 2 and \
                MON_H // 3 + new_txt.get_height() >= mouse_y >= MON_H // 3:
            menu_text(win, text_1, GREEN, MON_H // 3)
            op_1 = True
        elif MON_W // 2 + prev_txt.get_width() // 2 >= mouse_x >= MON_W // 2 - prev_txt.get_width() // 2 and \
                4 * MON_H // 9 + prev_txt.get_height() >= mouse_y >= 4 * MON_H // 9:
            menu_text(win, text_2, GREEN, 4 * MON_H // 9)
            op_2 = True
        elif MON_W // 2 + solve_txt.get_width() // 2 >= mouse_x >= MON_W // 2 - solve_txt.get_width() // 2 and \
                5 * MON_H // 9 + solve_txt.get_height() >= mouse_y >= 5 * MON_H // 9:
            menu_text(win, text_3, GREEN, 5 * MON_H // 9)
            op_3 = True

        # Change button color if mouse hovers over it
        if mouse_x >= MON_W - CLOSE[0] and mouse_y <= CLOSE[1]:
            close_button(win, RED)
            closed = True
        else:
            close_button(win, GRAY)

        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                if closed:
                    pygame.quit()
                    break
                elif op_1:
                    return 1
                elif op_2:
                    return 2
                elif op_3:
                    return 3

        # Draw cursor image over everything
        win.blit(cursor, (mouse_x, mouse_y))
        pygame.display.flip()


def change_color(color, sign):
    # If two colors are 255, it starts reducing one
    # If two colors are 0, it starts increasing one
    global color_0, color_1, color_2
    # Update color_o, color_1, color_2 to be equal to the components of current color
    for i, rgb in enumerate(color):
        variable_name = "color_{0}".format(i)
        globals()[variable_name] = rgb
    for i, rgb in enumerate(color):
        if i != 0 and rgb == 0 and color_0 == 0:
            sign = [0, 0, 0]
            if i == 1:
                sign[0] = COLOR_MULTIPLIER
            else:
                sign[i] = COLOR_MULTIPLIER
            break
        elif i != 0 and rgb == 255 and color_0 == 255:
            sign = [0, 0, 0]
            if i == 1:
                sign[0] = -COLOR_MULTIPLIER
            else:
                sign[i] = -COLOR_MULTIPLIER
            break
        elif color_1 == 255 and color_2 == 255:
            sign = [0, 0, 0]
            sign[1] = -COLOR_MULTIPLIER
            break
        elif color_1 == 0 and color_2 == 0:
            sign = [0, 0, 0]
            sign[1] = COLOR_MULTIPLIER
            break
    for i in range(3):
        variable_name = "color_{0}".format(i)
        globals()[variable_name] += sign[i]
    color = (color_0, color_1, color_2)
    return color, sign


def main():
    global showing
    # Create window and draw background
    WIN = pygame.display.set_mode((MON_W, MON_H), pygame.FULLSCREEN)
    icon = pygame.image.load('data\\sudoku.png')
    pygame.display.set_icon(icon)
    draw_bg(WIN)

    # Initialize local variables
    # By default, the game mode is regular play
    solving = False
    # Monitor state of game
    solved_once = False
    solved_twice = False
    done = False
    # Check if user has an input box selected
    selected = None
    # Check if user clicks on color selection panel
    mouse_down = False
    click = None
    slider_selection = None
    # Check if user wants to change board numbers color or user numbers color
    color_selection = 0
    # Keep track of data
    added_time = 0
    start_time = 0
    time_seconds = 0
    num_solve = 0
    difficulty = 0
    time = [0, 0, 0]
    # Keep track of colour on congratulations message
    color1 = PURPLE
    color2 = YELLOW
    sign1 = [5, 0, 0]
    sign2 = [0, 0, 0]
    # Load board color
    board_color = load_color(35)
    user_color = load_color(37)

    # Create three completely empty boards
    board = empty_board()
    user = empty_board()
    solved = empty_board()

    # Generate random confettis
    random_confetti()

    # Create menu page for the three modes
    main_choice = menu(WIN, "NEW GAME", "CONTINUE PREVIOUS", "SOLVE")

    # User chooses to start a new game
    if main_choice == 1:
        # Create menu page for the three difficulty levels
        difficulty = menu(WIN, "EASY", "INTERMEDIATE", "EXPERT")
        # Generate board
        solved = generate()
        # Keep a certain number of hints based on difficulty (easy:35-39, inter:30-34, expert:25-29)
        num_hints = random.randint(25 + (3 - difficulty) * 5, 29 + (3 - difficulty) * 5)
        for _ in range(num_hints):
            while True:
                # Find random space
                row_num = random.randint(0, 8)
                col_num = random.randint(0, 8)
                # Put solved number in space
                if board[row_num][col_num] == 0:
                    board[row_num][col_num] = solved[row_num][col_num]
                    break
        # Get game starting time
        start_time = pygame.time.get_ticks()
        # Update total number of games
        save_line(33, int(data[33]) + 1)

        playing = True

    # User chooses to continue previous game
    elif main_choice == 2:
        solved = []
        # Load previous boards
        board = load_board("board")
        user = load_board("user")
        # Load previous timer
        added_time = int(data[21])
        # Load difficulty
        difficulty = int(data[23])
        # Load number of solves
        num_solve = int(data[25])
        # Copy board into "solved"
        for row in range(9):
            temp_row = []
            for col in range(9):
                temp_row.append(board[row][col])
            solved.append(temp_row)
        # Solve board
        if not solve(solved):
            print("Board can not be solved")
            pygame.quit()
        # Start timer
        start_time = pygame.time.get_ticks()

        playing = True

    # User chooses to solve an unknown sudoku
    else:
        playing = True
        solving = True

    # Create clock to regulate FPS
    main_clock = pygame.time.Clock()

    # Main sudoku loop
    while playing:
        # 80 FPS
        main_clock.tick(80)
        # Draw background image and grid
        draw_bg(WIN)
        draw_grid(WIN)

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Display text options
        main_menu_text = playing_text(WIN, "main menu", BLUE1, 3 * MON_H // 8, mouse_x, mouse_y, "menu")
        if not done:
            reset_text = playing_text(WIN, "reset", BLUE1, MON_H // 2, mouse_x, mouse_y, "reset")
            erase_text = playing_text(WIN, "erase", BLUE1, 5 * MON_H // 8, mouse_x, mouse_y, "eraser")
            solve_text = playing_text(WIN, "solve", BLUE1, 3 * MON_H // 4, mouse_x, mouse_y, "solve")
        else:
            # When done, do not display these options
            reset_text = None
            erase_text = None
            solve_text = None

        # Temporary variables to show if mouse is hovering over text
        main_menu = False
        reset = False
        erase = False
        solve_selected = False

        # Text x position
        text_x = X + 9 * SQUARE + TEXT_SPACING // 3
        # Change text color is mouse hovers over it or its icon
        if not slider_selection:
            if text_x + main_menu_text[0].get_width() >= mouse_x >= text_x \
                    and 3 * MON_H // 8 + main_menu_text[0].get_height() >= mouse_y >= 3 * MON_H // 8 or main_menu_text[1]:
                playing_text(WIN, "main menu", GREEN, 3 * MON_H // 8, mouse_x, mouse_y, "menu", selected=True)
                main_menu = True
            elif not done:
                if text_x + reset_text[0].get_width() >= mouse_x >= text_x \
                        and MON_H // 2 + reset_text[0].get_height() >= mouse_y >= MON_H // 2 or reset_text[1]:
                    playing_text(WIN, "reset", GREEN, MON_H // 2, mouse_x, mouse_y, "reset", selected=True)
                    reset = True
                elif text_x + erase_text[0].get_width() >= mouse_x >= text_x \
                        and 5 * MON_H // 8 + erase_text[0].get_height() >= mouse_y >= 5 * MON_H // 8 or erase_text[1]:
                    playing_text(WIN, "erase", GREEN, 5 * MON_H // 8, mouse_x, mouse_y, "eraser", selected=True)
                    erase = True
                elif text_x + solve_text[0].get_width() >= mouse_x >= text_x \
                        and 3 * MON_H // 4 + solve_text[0].get_height() >= mouse_y >= 3 * MON_H // 4 or solve_text[1]:
                    playing_text(WIN, "solve", GREEN, 3 * MON_H // 4, mouse_x, mouse_y, "solve", selected=True)
                    solve_selected = True

        # Change close button color if mouse hovers over it
        if mouse_x >= MON_W - CLOSE[0] and mouse_y <= CLOSE[1]:
            close_button(WIN, RED)
            closed = True
        else:
            close_button(WIN, GRAY)
            closed = False

        # Code to execute only for regular sudokus
        if not solving:
            # If mouse button is pressed and has not yet been released, send position to sliders panel
            if mouse_down:
                click = (mouse_x, mouse_y)
            # Display color selection panel and update all the variables
            board_color, user_color, color_selection, click, slider_selection = select_color(WIN, board_color, user_color, click,
                                                                                             color_selection, slider_selection)
            # Update time only if not solved
            if not solved_once and not solved_twice and not done:
                # Calculate time
                time = get_time(start_time, added_time)
            # Display time
            # Calculate time in seconds
            time_seconds = 3600 * time[0] + 60 * time[1] + time[2]
            # Format time
            h = time_format(time[0])
            m = time_format(time[1])
            s = time_format(time[2])
            # Draw time
            time_text = TEXT_FONT_64.render("{0}:{1}:{2}".format(h, m, s), True, GREEN)
            time_x = X + 9 * SQUARE + TEXT_SPACING // 4
            time_y = 7 * MON_H // 8
            WIN.blit(time_text, (time_x, time_y))
            # Display clock image
            WIN.blit(clock_img, (time_x - ICON_SIZE_2[0], time_y))
            # Draw numbers for all the user input (if the user did not yet click on solve)
            # If the user did click on solve, draw the user's numbers in either red or green depending on their sign (-: wrong, +: right)
            draw_numbers(WIN, user, user_color, correcting=solved_once)

        # Tell draw_numbers function to use images instead of fonts for solving mode
        else:
            # Draw user number with images
            draw_numbers(WIN, user, GOLD)
            # Draw other numbers with color
            board_color = GREEN

        # Check for events
        for event in pygame.event.get():
            # If user pressed down
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            # Check for key press
            elif event.type == pygame.KEYUP:
                # Reset solved state
                solved_once = False
                # If user presses ESC
                if event.key == pygame.K_ESCAPE:
                    # Save game only in regular mode
                    if not solving:
                        save_game(board, user, time_seconds, difficulty, board_color, user_color)
                    # Quit
                    pygame.quit()
                # If a square is highlighted
                elif selected:
                    # Check if user pressed a number
                    for i in range(0, 10):
                        keypad = "keypad {0}".format(i)
                        # If the pygame key code is "1" or "keypad 1", it means that the player pressed 1
                        if event.key == pygame.key.key_code(str(i)) or event.key == pygame.key.key_code(keypad):
                            # Put the pressed number in the selected box
                            user[selected[1]][selected[0]] = i
                            # Stop the "for" loop if the key is identified (not essential, but saves some processing power)
                            break
                    # If there is not already a hint in the box on which the mouse clicked
                    if event.key == pygame.K_UP:
                        selected = move_selected(board, selected, 1, -1)
                    elif event.key == pygame.K_DOWN:
                        selected = move_selected(board, selected, 1, 1)
                    elif event.key == pygame.K_LEFT:
                        selected = move_selected(board, selected, 0, -1)
                    elif event.key == pygame.K_RIGHT:
                        selected = move_selected(board, selected, 0, 1)

            # Check for click
            elif event.type == pygame.MOUSEBUTTONUP:
                # Once mouse is released, reset slider and mouse down variables
                slider_selection = None
                mouse_down = False
                # Get mouse row and column, returns None if mouse is not in the board
                mouse_pos = get_mouse(mouse_x, mouse_y)
                # If user clicks somewhere, it resets the solved state
                solved_twice = False
                # If mouse is on close button
                if closed:
                    # Save game only in regular mode
                    if not solving:
                        save_game(board, user, time_seconds, difficulty, board_color, user_color)
                    # Close loop
                    playing = False
                    # Quit
                    pygame.quit()
                # If mouse is in board
                elif mouse_pos and not done:
                    # If there is not already a hint in the box on which the mouse clicked
                    if board[mouse_pos[1]][mouse_pos[0]] == 0:
                        # Store the column and row in "selected"
                        selected = [mouse_pos[0], mouse_pos[1]]
                # Calls main loop again if player wants to go back to the main menu
                elif main_menu:
                    # Save game only in regular mode
                    if not solving:
                        save_game(board, user, time_seconds, difficulty, board_color, user_color)
                    main()
                    # When main loop ends, all other main functions end
                    return False
                # Resets board to an empty board
                elif reset:
                    # Reset user board
                    user = empty_board()
                    # Reset solved board in solving mode
                    if solving:
                        board = empty_board()
                # If user clicks on erase and there is a box selected
                elif erase and selected:
                    # The selected box resets to 0
                    user[selected[1]][selected[0]] = 0
                # If user clicks on solve
                elif solve_selected:
                    num_solve += 1
                    selected = None
                    if not solved_once:
                        solved_once = True
                    # If user clicks on solve a second time in a row
                    else:
                        solved_twice = True
                # If user clicked anywhere else, the solved state resets and the selection resets
                elif not done:
                    solved_once = False
                    selected = None
                else:
                    selected = None

        # Corrects all the user's numbers
        if solved_once:
            if not solving:
                # Check if user's numbers are valid
                if final_check(board, user):
                    done = True
                    # Successfully completed without cheating
                    if num_solve == 1:
                        # Add 1 to total number of completed games
                        save_line(31, int(data[31]) + 1)
                        # Save high score if this time is smaller than previous high score (lower time = better)
                        previous_high_text = data[26 + difficulty].split(" ")
                        previous_high = int(previous_high_text[1])
                        if previous_high > time_seconds and previous_high != 0:
                            save_line(26 + difficulty,  "{0} {1}\n".format(previous_high_text[0], time_seconds))
                # If user got some numbers wrong
                else:
                    for row in range(9):
                        for col in range(9):
                            # Make the user's number negative if it's a wrong number
                            # (draw_numbers() function draws negative numbers in red and positive ones in green if correcting=True)
                            if user[row][col] != 0 and user[row][col] != solved[row][col]:
                                user[row][col] = -abs(user[row][col])
            # If player is in solving mode
            else:
                # Call function show_solve and put whatever it returns in variable temp_board
                temp_board = check_solvable(user)
                # Check if function returned anything
                if temp_board:
                    # Copy temporary board to board
                    for row in range(9):
                        for col in range(9):
                            board[row][col] = temp_board[row][col]
                    # Start solving animation
                    showing = True
                # If board is not solvable
                else:
                    # Display text for two seconds
                    unsolvable_text = TEXT_FONT_84.render("BOARD IS UNSOLVABLE", True, YELLOW, BLACK)
                    unsolvable_x = (MON_W - TEXT_SPACING) // 2 - unsolvable_text.get_width() // 2
                    unsolvable_y = MON_H // 2 - unsolvable_text.get_height() // 2
                    WIN.blit(unsolvable_text, (unsolvable_x, unsolvable_y))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                # Reset solved state
                solved_once = False

        # Displays all the correct numbers (in regular mode only)
        if solved_twice and not solving:
            # Dictionary of incorrect user numbers
            incorrect = {}
            # Board representing all the numbers in the boxes left empty
            correction = []
            # Copy solved board (important to do it this way because if you put list1 = list2,
            # it links the two lists and you can't modify one by itself)
            for row in solved:
                # Create temporary list
                temp_row = []
                # Take each number in the solved row
                for num in row:
                    # Append the number to the temporary list
                    temp_row.append(num)
                # Append the temporary list to "correction"
                correction.append(temp_row)

            # Check for empty spots
            for row in range(9):
                for col in range(9):
                    # If the there is already a number in the box, do not draw it (make the number equal to 0)
                    if board[row][col] != 0 or user[row][col] != 0:
                        correction[row][col] = 0
                    # If the user's number is wrong, save the number and its row, column position in the "incorrect" dictionary
                    if solved[row][col] != user[row][col] and user[row][col] != 0:
                        incorrect[(row, col)] = solved[row][col]
            # Draw purple correct numbers in empty spots and in the corner of user's errors
            draw_numbers(WIN, correction, PURPLE, incorrect=incorrect)

        # In solving mode, only display board numbers (solved) once the showing animation is done
        if not showing:
            # Draw board numbers with the digit images in regular mode or in green in solving mode
            draw_numbers(WIN, board, color=board_color)
        else:
            # Deselect selected box
            selected = None
            # Show the recursive solving process
            show_solve(WIN, user)
            # Finished showing the solving process
            showing = False

        # Draw square if user selected
        if selected:
            # Get pixel position of selected column and row
            square_x, square_y = get_pos(selected[0], selected[1])
            # Add a little bit of offset
            square_x -= SQUARE // 8
            square_y -= SQUARE // 8
            WIN.blit(blue_square, (square_x, square_y))

        # Celebrate when user completes a game
        if done:
            # Congratulations message that changes colors
            # Update colors
            color1, sign1 = change_color(color1, sign1)
            color2, sign2 = change_color(color2, sign2)
            # Create colored text with colored background
            congratulations_text = TEXT_FONT_84.render("CONGRATULATIONS", True, color1, color2)
            # Calculate middle of board
            congratulations_x = (MON_W - TEXT_SPACING) // 2 - congratulations_text.get_width() // 2
            congratulations_y = MON_H // 2 - congratulations_text.get_height() // 2
            # Create background rectangle the size of the text
            bg_rect = congratulations_text.get_rect(topleft=(congratulations_x - 10, congratulations_y - 10))
            # Shift position slightly
            bg_rect.x += 20
            bg_rect.y += 20
            # Draw background rectangle and text box
            if user_color != [-1, -1, -1]:
                pygame.draw.rect(WIN, user_color, bg_rect)
            else:
                pygame.draw.rect(WIN, BLUE1, bg_rect)
            WIN.blit(congratulations_text, (congratulations_x, congratulations_y))
            # Confetti falling randomly
            confetti(WIN)

        # Draw cursor image
        WIN.blit(cursor, (mouse_x, mouse_y))

        # Update display
        pygame.display.flip()


if __name__ == "__main__":
    try:
        main()
    # Bypass any error caused by pygame.quit() function
    except pygame.error:
        pass
