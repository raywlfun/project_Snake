import tkinter
import tkinter as tk
import random

# create constants
game_screen_width = 750
game_screen_height = 750
game_speed = 100  # Rate of which the screen updates
grid_square_size = 50
snake_body = 2
snake_colour = "yellow"
food_object_colour = "red"
background_colour = "black"

class Snake:
    # Initialise a constructor
    def __init__(self):
        self.snake_body_size = snake_body
        self.snake_body_coordinates = []
        self.grid_squares = []

        # Create list of coordinates
        for i in range(0, snake_body):
            print(f"i = {i}")
            # Snake appears in top left corner
            self.snake_body_coordinates.append([0, 0])

        for snake_x_axis, snake_y_axis in self.snake_body_coordinates:
            square = game_screen.create_rectangle(snake_x_axis, snake_y_axis,
                                                  snake_x_axis + grid_square_size,
                                                  snake_y_axis + grid_square_size,
                                                  fill=snake_colour,
                                                  tag="snake")
            print(square)
            self.grid_squares.append(square)


class Food:

    def __init__(self):
        food_coordinate_x_axis = random.randint(0, (game_screen_width / grid_square_size) -1) * grid_square_size
        food_coordinate_y_axis = random.randint(0, (game_screen_height / grid_square_size) -1) * grid_square_size

        self.food_object_coordinates = [food_coordinate_x_axis, food_coordinate_y_axis]

        game_screen.create_oval(food_coordinate_x_axis, food_coordinate_y_axis,
                                food_coordinate_x_axis + grid_square_size,
                                food_coordinate_y_axis + grid_square_size,
                                fill=food_object_colour, tag='food')


def set_startup_game_window_position():
    game_window_width = game_window.winfo_width()
    game_window_height = game_window.winfo_height()

    screen_width = game_window.winfo_screenwidth()
    screen_height = game_window.winfo_screenheight()

    game_window_x_axis = int((screen_width/2) - (game_window_width/2))
    game_window_y_axis = int((screen_height/2) - (game_window_height/2))

    game_window.geometry(f'{game_window_width}x{game_window_height}+{game_window_x_axis}+{game_window_y_axis}')

def update_snake_position(snake, food_object):

    snake_x_axis, snake_y_axis = snake.snake_body_coordinates[0]

    # Increment / Decrement x or y axis coordinates of the snake
    if snake_direction == 'up':
        snake_y_axis -= grid_square_size
    elif snake_direction == 'down':
        snake_y_axis += grid_square_size
    elif snake_direction == 'right':
        snake_x_axis += grid_square_size
    elif snake_direction == 'left':
        snake_x_axis -= grid_square_size

    # update coordinates of the head of the snake, by inserting to index 0
    snake.snake_body_coordinates.insert(0, (snake_x_axis, snake_y_axis))

    grid_square_coordinate = game_screen.create_rectangle(snake_x_axis, snake_y_axis,
                                          snake_x_axis + grid_square_size,
                                          snake_y_axis + grid_square_size,
                                          fill=snake_colour)

    snake.grid_squares.insert(0, grid_square_coordinate)

    # Check if snake position == food object position
    if snake_x_axis == food_object.food_object_coordinates[0] and snake_y_axis == food_object.food_object_coordinates[1]:
        update_game_score()

        # Call a new randomised instance of the food object
        food_object = Food()

    else:
        # delete snake tail coordinates
        del snake.snake_body_coordinates[-1]

        game_screen.delete(snake.grid_squares[-1])

        del snake.grid_squares[-1]

    # Simulate automatic movement by continuously calling this function
    game_window.after(game_speed, update_snake_position, snake, food_object)


def update_game_score():
    global game_score
    game_score += 1

    # Display the score
    game_score_label.config(text='Score:{}'.format(game_score))

    # Remove the food object, by calling the "tag" of the food class
    game_screen.delete('food')

def change_snake_direction(updated_direction):

    global snake_direction

    if updated_direction == 'left':
        if snake_direction != 'right':
            snake_direction = updated_direction

    elif updated_direction == 'right':
        if snake_direction != 'left':
            snake_direction = updated_direction

    elif updated_direction == 'up':
        if snake_direction != 'down':
            snake_direction = updated_direction

    elif updated_direction == 'down':
        if snake_direction != 'up':
            snake_direction = updated_direction

    return snake_direction


def detect_key_pressed():
    # When directional key is pressed, its corresponding string label is input to the change snake direction function
    game_window.bind('<Left>', lambda event: change_snake_direction('left'))
    game_window.bind('<Right>', lambda event: change_snake_direction('right'))
    game_window.bind('<Up>', lambda event: change_snake_direction('up'))
    game_window.bind('<Down>', lambda event: change_snake_direction('down'))

    return


def check_collisions():
    pass


def game_over():
    pass

game_window = tk.Tk()
game_window.title("Snake game")
game_window.resizable(False, False)

game_score = 0
snake_direction = 'down'

game_score_label = tkinter.Label(game_window, text='Score: {}'.format(game_score), font=('consolas', 40))
game_score_label.pack()

game_screen = tkinter.Canvas(game_window, bg=background_colour, height=game_screen_height, width=game_screen_width)
game_screen.pack()

# Refresh the game window
game_window.update()

# On bootup, allocate fixed game_window starting position
set_startup_game_window_position()

# def key_pressed(event):
#     write_label= tkinter.Label(game_window, text='Key Pressed :'+event.char)
#     write_label.place(x=80, y=90)

# game_window.bind('<Left>', key_pressed)

detect_key_pressed()

snake = Snake()
food_objects = Food()

update_snake_position(snake, food_objects)

game_window.mainloop()