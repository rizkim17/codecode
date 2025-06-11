from tkinter import *
import random

# Global variables
# Window settings
WIDTH = 900
HEIGHT = 300

# Paddle settings
PAD_W = 10  # Paddle width
PAD_H = 100  # Paddle height

# Ball settings
BALL_SPEED_UP = 1.05  # How much ball speed increases with each hit
BALL_MAX_SPEED = 40  # Maximum ball speed
BALL_RADIUS = 30  # Ball radius

INITIAL_SPEED = 20
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED

# Player scores
PLAYER_1_SCORE = 0  # Initialize score to 0
PLAYER_2_SCORE = 0  # Initialize score to 0

# Global variable for distance to the right edge of the playing field
right_line_distance = WIDTH - PAD_W

def update_score(player):
    """
    Updates the score for the specified player.
    """
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == "right":
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)

def spawn_ball():
    """
    Resets the ball to the center and sets its initial direction.
    """
    global BALL_X_SPEED
    # Place the ball in the center
    c.coords(BALL, WIDTH / 2 - BALL_RADIUS / 2,
             HEIGHT / 2 - BALL_RADIUS / 2,
             WIDTH / 2 + BALL_RADIUS / 2,
             HEIGHT / 2 + BALL_RADIUS / 2)
    # Set ball direction towards the losing player,
    # but reduce speed to initial speed
    BALL_X_SPEED = (BALL_X_SPEED / abs(BALL_X_SPEED)) * INITIAL_SPEED
    # Reset Y speed to initial speed as well for consistent restart
    global BALL_Y_SPEED
    BALL_Y_SPEED = INITIAL_Y_SPEED if 'INITIAL_Y_SPEED' in globals() else INITIAL_SPEED # Ensure INITIAL_Y_SPEED is defined or use INITIAL_SPEED


def bounce(action):
    """
    Handles ball bouncing logic.
    """
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == "strike":  # Hit by a paddle
        BALL_Y_SPEED = random.randrange(-10, 10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED *= -1 # Just reverse direction if max speed reached
    else:  # Ricochet (vertical bounce)
        BALL_Y_SPEED *= -1

# Setup window
root = Tk()
root.title("Pong")

# Animation area
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#003380")
c.pack()

# Playing field elements
# Left line
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
# Right line
c.create_line(WIDTH - PAD_W, 0, WIDTH - PAD_W, HEIGHT, fill="white")
# Center line
c.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="white")

# Game elements
# Create ball
BALL = c.create_oval(WIDTH / 2 - BALL_RADIUS / 2,
                     HEIGHT / 2 - BALL_RADIUS / 2,
                     WIDTH / 2 + BALL_RADIUS / 2,
                     HEIGHT / 2 + BALL_RADIUS / 2, fill="white")

# Left paddle
LEFT_PAD = c.create_line(PAD_W / 2, 0, PAD_W / 2, PAD_H, width=PAD_W, fill="yellow")

# Right paddle
RIGHT_PAD = c.create_line(WIDTH - PAD_W / 2, 0, WIDTH - PAD_W / 2,
                          PAD_H, width=PAD_W, fill="yellow")

# Score display
p_1_text = c.create_text(WIDTH - WIDTH / 6, PAD_H / 4,
                         text=PLAYER_1_SCORE,
                         font="Arial 20",
                         fill="white")

p_2_text = c.create_text(WIDTH / 6, PAD_H / 4,
                         text=PLAYER_2_SCORE,
                         font="Arial 20",
                         fill="white")

# Global variables for ball speed (redundant with BALL_X_SPEED, BALL_Y_SPEED but kept for consistency with source)
BALL_X_CHANGE = 20 # This variable is not used in move_ball function as BALL_X_SPEED is used.
BALL_Y_CHANGE = 0 # This variable is not used in move_ball function as BALL_Y_SPEED is used.

def move_ball():
    """
    Moves the ball and handles collisions with walls and paddles.
    """
    # Determine coordinates of the ball's sides and its center
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2

    # If we are far from the vertical lines, just move the ball
    if ball_right + BALL_X_SPEED < right_line_distance and \
       ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    # If the ball touches the right or left boundary of the field
    elif ball_right >= right_line_distance or ball_left <= PAD_W:
        # Check which side (right or left) we touched
        if ball_right >= WIDTH / 2: # Ball is on the right half
            # If true, compare the ball's center position with the right paddle's position.
            # And if the ball is within the paddle, perform a bounce.
            if c.coords(RIGHT_PAD)[1] <= ball_center <= c.coords(RIGHT_PAD)[3]: #
                bounce("strike")
            else:
                update_score("left")
                spawn_ball()
        else: # Ball is on the left half
            # Same for the left player
            if c.coords(LEFT_PAD)[1] <= ball_center <= c.coords(LEFT_PAD)[3]: #
                bounce("strike")
            else:
                update_score("right")
                spawn_ball()
    else: # If the ball is about to fly out of bounds, move it to the edge. 
        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance - ball_right, BALL_Y_SPEED)
        else:
            c.move(BALL, PAD_W - ball_left, BALL_Y_SPEED)

    # Horizontal bounce (top/bottom walls)
    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce("ricochet")

# Set global variables for paddle speed
PAD_SPEED = 20  # Paddle movement speed
LEFT_PAD_SPEED = 0  # Left paddle speed
RIGHT_PAD_SPEED = 0  # Right paddle speed

def move_pads():
    """
    Moves both paddles according to their current speeds.
    """
    # Create a dictionary where paddles correspond to their speeds
    PADS = {LEFT_PAD: LEFT_PAD_SPEED,
            RIGHT_PAD: RIGHT_PAD_SPEED}

    # Move paddles with their specified speeds
    for pad in PADS:
        c.move(pad, 0, PADS[pad]) # Only move vertically

        # If the paddle moves out of the playing field, put it back in place 
        if c.coords(pad)[1] < 0: # Top edge out of bounds
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT: # Bottom edge out of bounds
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])

def main():
    """
    Main game loop.
    """
    move_ball()
    move_pads()
    # Call itself every 30 milliseconds
    root.after(30, main)

# Set focus on Canvas to respond to key presses
c.focus_set()

def movement_handler(event):
    """
    Handles key presses for paddle movement.
    """
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == "w":
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "s":
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED

# Bind this function to Canvas
c.bind("<KeyPress>", movement_handler)

def stop_pad(event):
    """
    Handles key releases to stop paddle movement.
    """
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in ("w", "s"):
        LEFT_PAD_SPEED = 0
    elif event.keysym in ("Up", "Down"):
        RIGHT_PAD_SPEED = 0

# Bind this function to Canvas
c.bind("<KeyRelease>", stop_pad)

# Start the game loop
main()

# Run the window
root.mainloop()