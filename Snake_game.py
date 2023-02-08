import tkinter
import tkinter as tk
import random

# Define game window dimensions and UI properties
GAME_SCREEN_WIDTH = 750
GAME_SCREEN_HEIGHT = 750
GAME_SPEED = 75  # Rate of which the screen updates
GAME_SCORE = 0
GRID_SQUARE_SIZE = 50
SNAKE_BODY = 2

SNAKE_DIRECTION = 'down'
SNAKE_COLOUR = "yellow"
FOOD_OBJECT_COLOUR = "red"
BACKGROUND_COLOUR = "black"
GAME_STATE = True

class Snake:
    # Initialise a constructor
    def __init__(self):
        self.snake_body_size = SNAKE_BODY
        self.snake_body_coordinates = []
        self.grid_squares = []

        # Upon bootup, create initial snake body list of coordinates
        for snake_body_length in range(0, SNAKE_BODY):
            print(f"snake body length = {snake_body_length}")
            # Snake appears in top left corner
            self.snake_body_coordinates.append([100, 100])

        for snake_x_axis, snake_y_axis in self.snake_body_coordinates:

            # Create visual of snake body by its x and y coordinates
            snake_body_part = game_screen.create_rectangle(
                                                            snake_x_axis, snake_y_axis,
                                                            snake_x_axis + GRID_SQUARE_SIZE,
                                                            snake_y_axis + GRID_SQUARE_SIZE,
                                                            fill=SNAKE_COLOUR,tag="snake")
            self.grid_squares.append(snake_body_part)


class Food:

    def __init__(self):
        food_coordinate_x_axis = random.randint(0, (GAME_SCREEN_WIDTH / GRID_SQUARE_SIZE) -1) * GRID_SQUARE_SIZE
        food_coordinate_y_axis = random.randint(0, (GAME_SCREEN_HEIGHT / GRID_SQUARE_SIZE) -1) * GRID_SQUARE_SIZE

        self.food_object_coordinates = [food_coordinate_x_axis, food_coordinate_y_axis]

        game_screen.create_oval(
                                food_coordinate_x_axis,
                                food_coordinate_y_axis,
                                food_coordinate_x_axis + GRID_SQUARE_SIZE,
                                food_coordinate_y_axis + GRID_SQUARE_SIZE,
                                fill=FOOD_OBJECT_COLOUR, tag='food')


def set_startup_game_window_position():
    game_window_width = game_window.winfo_width()
    game_window_height = game_window.winfo_height()

    screen_width = game_window.winfo_screenwidth()
    screen_height = game_window.winfo_screenheight()

    game_window_x_axis = int((screen_width/2) - (game_window_width/2))
    game_window_y_axis = int((screen_height/2) - (game_window_height/2))

    game_window.geometry(f'{game_window_width}x{game_window_height}+{game_window_x_axis}+{game_window_y_axis}')

def update_snake_position(snake, food_object):

    # Assign coordinates of the snake head
    snake_x_axis, snake_y_axis = snake.snake_body_coordinates[0]
    # print(snake.snake_body_coordinates[0])

    # Increment / Decrement x or y coordinates of the snake
    if SNAKE_DIRECTION == 'up':
        snake_y_axis -= GRID_SQUARE_SIZE
    elif SNAKE_DIRECTION == 'down':
        snake_y_axis += GRID_SQUARE_SIZE
    elif SNAKE_DIRECTION == 'right':
        snake_x_axis += GRID_SQUARE_SIZE
    elif SNAKE_DIRECTION == 'left':
        snake_x_axis -= GRID_SQUARE_SIZE

    # update coordinates of the head of the snake, by inserting to index 0
    snake.snake_body_coordinates.insert(0, (snake_x_axis, snake_y_axis))

    grid_square_coordinate = game_screen.create_rectangle(snake_x_axis, snake_y_axis,
                                          snake_x_axis + GRID_SQUARE_SIZE,
                                          snake_y_axis + GRID_SQUARE_SIZE,
                                          fill=SNAKE_COLOUR)

    snake.grid_squares.insert(0, grid_square_coordinate)

    # Check if snake position == food object position
    if snake_x_axis == food_object.food_object_coordinates[0] and \
            snake_y_axis == food_object.food_object_coordinates[1]:
        update_game_score()

        # Call a new randomised instance of the food object
        food_object = Food()
    else:
        # delete snake tail coordinates
        del snake.snake_body_coordinates[-1]
        game_screen.delete(snake.grid_squares[-1])
        del snake.grid_squares[-1]

    # Simulate automatic movement by continuously calling this function
    game_window.after(GAME_SPEED, update_snake_position, snake, food_object)

    # collision function check here
    check_if_collision(snake_x_axis, snake_y_axis)

    return

def update_game_score():
    global GAME_SCORE
    GAME_SCORE += 1

    # Display the score
    GAME_SCORE_label.config(text='Score:{}'.format(GAME_SCORE))

    # Remove the food object, by calling the "tag" of the food class
    game_screen.delete('food')


def change_snake_direction(updated_direction: str):

    global SNAKE_DIRECTION

    if updated_direction == 'left':
        if SNAKE_DIRECTION != 'right':
            SNAKE_DIRECTION = updated_direction

    elif updated_direction == 'right':
        if SNAKE_DIRECTION != 'left':
            SNAKE_DIRECTION = updated_direction

    elif updated_direction == 'up':
        if SNAKE_DIRECTION != 'down':
            SNAKE_DIRECTION = updated_direction

    elif updated_direction == 'down':
        if SNAKE_DIRECTION != 'up':
            SNAKE_DIRECTION = updated_direction

    return SNAKE_DIRECTION


def detect_key_pressed():
    # When directional key is pressed, its corresponding string label is input to the change snake direction function
    game_window.bind('<Left>', lambda event: change_snake_direction('left'))
    game_window.bind('<Right>', lambda event: change_snake_direction('right'))
    game_window.bind('<Up>', lambda event: change_snake_direction('up'))
    game_window.bind('<Down>', lambda event: change_snake_direction('down'))

    return


def check_if_collision(snake_head_x_axis, snake_head_y_axis):

    # Check if snake collides with walls
    if snake_head_x_axis == GAME_SCREEN_WIDTH or \
            snake_head_x_axis == -50:
        print("COLLIDED WITH WIDTH BOUNDARY")
        terminate_game_session()

    if snake_head_y_axis == GAME_SCREEN_HEIGHT or \
            snake_head_y_axis == -50:
        print("COLLIDED WITH HEIGHT BOUNDARY")
        terminate_game_session()

    # Check if snake collides with itself
    for snake_body_part in snake.snake_body_coordinates[1:]:
        if snake_head_x_axis == snake_body_part[0] and \
                snake_head_y_axis == snake_body_part[1]:
            print("COLLIDED WITH SNAKE")
            terminate_game_session()

def terminate_game_session():
    global GAME_STATE

    print(f"Collision detected: Game status = {GAME_STATE}")
    GAME_STATE = False

    # Terminate game window and all running application processes
    game_window.destroy()

while GAME_STATE == True:

    game_window = tk.Tk()
    game_window.title("Snake game")
    game_window.resizable(False, False)



    GAME_SCORE_label = tkinter.Label(game_window,
                                     text='Score: {}'.format(GAME_SCORE),
                                     font=('times new roman', 40))
    GAME_SCORE_label.pack()

    game_screen = tkinter.Canvas(game_window,
                                 bg=BACKGROUND_COLOUR,
                                 height=GAME_SCREEN_HEIGHT,
                                 width=GAME_SCREEN_WIDTH)
    game_screen.pack()

    # Refresh the game window
    game_window.update()

    # On bootup, allocate fixed game_window starting position
    set_startup_game_window_position()

    detect_key_pressed()

    snake = Snake()
    food_objects = Food()

    update_snake_position(snake, food_objects)

    game_window.mainloop()