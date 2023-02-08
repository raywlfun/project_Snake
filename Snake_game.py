import tkinter
import tkinter as tk
import random

# Define game window dimensions and UI properties
GAME_SCREEN_WIDTH = 700
GAME_SCREEN_HEIGHT = 700
GAME_SPEED = 75  # Rate of which the screen updates
GAME_SCORE = 0
GAME_STATE = True

GRID_SQUARE_SIZE = 50
SNAKE_BODY = 2

SNAKE_DIRECTION = 'down'
SNAKE_COLOUR = "yellow"
FOOD_OBJECT_COLOUR = "red"
BACKGROUND_COLOUR = "black"


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

        for snake_x_axis_coordinate, snake_y_axis_coordinate in self.snake_body_coordinates:
            # Create visual of snake body by its x and y coordinates
            snake_body_part = game_screen.create_rectangle(
                                                            snake_x_axis_coordinate, snake_y_axis_coordinate,
                                                            snake_x_axis_coordinate + GRID_SQUARE_SIZE,
                                                            snake_y_axis_coordinate + GRID_SQUARE_SIZE,
                                                            fill=SNAKE_COLOUR,tag="snake")
            self.grid_squares.append(snake_body_part)


class Food:
    def __init__(self):
        food_x_axis_coordinate = random.randint(0, (GAME_SCREEN_WIDTH/GRID_SQUARE_SIZE)-1) * GRID_SQUARE_SIZE
        food_y_axis_coordinate = random.randint(0, (GAME_SCREEN_HEIGHT/GRID_SQUARE_SIZE)-1) * GRID_SQUARE_SIZE

        self.food_object_coordinates = [food_x_axis_coordinate, food_y_axis_coordinate]

        game_screen.create_oval(
                                food_x_axis_coordinate,
                                food_y_axis_coordinate,
                                food_x_axis_coordinate + GRID_SQUARE_SIZE,
                                food_y_axis_coordinate + GRID_SQUARE_SIZE,
                                fill=FOOD_OBJECT_COLOUR, tag='food')


def set_startup_game_window_position():
    # Get pixel dimensions for game window and entire screen
    game_window_pixel_width = game_window.winfo_width()
    game_window_pixel_height = game_window.winfo_height()

    screen_pixel_width = game_window.winfo_screenwidth()
    screen_pixel_height = game_window.winfo_screenheight()

    game_window_x_axis_position = int((screen_pixel_width/2) - (game_window_pixel_width/2))
    game_window_y_axis_position = int((screen_pixel_height/2) - (game_window_pixel_height/2)-30)

    # Set position of game window
    game_window.geometry(f'{game_window_pixel_width}x'
                         f'{game_window_pixel_height}+'
                         f'{game_window_x_axis_position}+'
                         f'{game_window_y_axis_position}')


def update_snake_position(snake_position, food_object_position):
    # Assign coordinates of the snake head
    snake_x_axis_coordinate, snake_y_axis_coordinate = snake_position.snake_body_coordinates[0]

    # Increment / Decrement x or y coordinates of the snake
    if SNAKE_DIRECTION == 'up':
        snake_y_axis_coordinate -= GRID_SQUARE_SIZE

    elif SNAKE_DIRECTION == 'down':
        snake_y_axis_coordinate += GRID_SQUARE_SIZE

    elif SNAKE_DIRECTION == 'right':
        snake_x_axis_coordinate += GRID_SQUARE_SIZE

    elif SNAKE_DIRECTION == 'left':
        snake_x_axis_coordinate -= GRID_SQUARE_SIZE

    # Update coordinates of the head of the snake, by inserting to index 0
    snake_position.snake_body_coordinates.insert(0, (snake_x_axis_coordinate, snake_y_axis_coordinate))

    grid_square_coordinate = game_screen.create_rectangle(
                                                          snake_x_axis_coordinate, snake_y_axis_coordinate,
                                                          snake_x_axis_coordinate + GRID_SQUARE_SIZE,
                                                          snake_y_axis_coordinate + GRID_SQUARE_SIZE,
                                                          fill=SNAKE_COLOUR)

    snake_position.grid_squares.insert(0, grid_square_coordinate)

    # Check if snake position == food object position
    if snake_x_axis_coordinate == food_object_position.food_object_coordinates[0] and \
            snake_y_axis_coordinate == food_object_position.food_object_coordinates[1]:

        update_game_score()
        # Call a new randomised instance of the food object
        food_object_position = Food()

    else:
        # Delete snake tail position
        del snake_position.snake_body_coordinates[-1]
        game_screen.delete(snake.grid_squares[-1])
        del snake_position.grid_squares[-1]

    # Simulate automatic movement by continuously calling this function
    game_window.after(GAME_SPEED, update_snake_position, snake_position, food_object_position)

    check_if_collision(snake_x_axis_coordinate, snake_y_axis_coordinate)
    return


def update_game_score():
    global GAME_SCORE
    GAME_SCORE += 1

    # Display the score
    GAME_SCORE_label.config(text='Score:{}'.format(GAME_SCORE))

    # Remove the food object, by calling the "tag" of the food class
    game_screen.delete('food')
    return


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


def check_if_collision(snake_head_x_axis_coordinate: int, snake_head_y_axis_coordinate: int):
    # Check if snake collides with walls
    if snake_head_x_axis_coordinate == GAME_SCREEN_WIDTH or \
            snake_head_x_axis_coordinate == -50:
        print("COLLIDED WITH WIDTH BOUNDARY")
        terminate_game_session()

    if snake_head_y_axis_coordinate == GAME_SCREEN_HEIGHT or \
            snake_head_y_axis_coordinate == -50:
        print("COLLIDED WITH HEIGHT BOUNDARY")
        terminate_game_session()

    # Check if snake collides with itself
    for snake_body_part in snake.snake_body_coordinates[1:]:
        if snake_head_x_axis_coordinate == snake_body_part[0] and \
                snake_head_y_axis_coordinate == snake_body_part[1]:
            print("COLLIDED WITH SNAKE")
            terminate_game_session()
    return


def terminate_game_session():
    global GAME_STATE

    GAME_STATE = False
    print(f"Collision detected: Game status = {GAME_STATE}")

    # Terminate game window and all running application processes
    game_window.destroy()
    return


while GAME_STATE is not False:
    game_window = tk.Tk()
    game_window.title("Snake game")
    game_window.resizable(False, False)

    GAME_SCORE_label = tkinter.Label(
                                     game_window,
                                     text='Score: {}'.format(GAME_SCORE),
                                     font=('verdana', 20))
    GAME_SCORE_label.pack()

    game_screen = tkinter.Canvas(game_window,
                                 bg=BACKGROUND_COLOUR,
                                 height=GAME_SCREEN_HEIGHT,
                                 width=GAME_SCREEN_WIDTH)
    game_screen.pack()

    # Refresh the game window
    game_window.update()

    # If window is closed manually
    game_window.protocol("WM_DELETE_WINDOW", terminate_game_session)

    set_startup_game_window_position()
    detect_key_pressed()
    snake = Snake()
    food_objects = Food()
    update_snake_position(snake, food_objects)

    game_window.mainloop()