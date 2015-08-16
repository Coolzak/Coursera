## MiniProject #4. Pong ##
# Added not required options: spawn delay, and score backlight

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True


# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, spawn		# these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]		# ball position for spawn 
    ball_vel = [0, 0]
    def spawn():							# extra function delays spawn, for better playability
        global ball_vel, color
        timer.stop()						
        ball_vel = [random.randrange(120, 240)/60, -random.randrange(60, 180)/60]
                                            # randomizing ball velocity
        if direction != RIGHT: ball_vel[0] *= -1# spawn velocity direction      
        color = "Gray"						# returns main color score counters
        return ball_vel, color				
    timer = simplegui.create_timer(1000, spawn)# 1 sec. delay
    timer.start()
    
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2 					# these are ints
    global color							# uses in draw function
    score1 = 0								# initial score of the 1 player
    score2 = 0								# initial score of the 2 player
    paddle1_pos = HEIGHT/2					# initial position of the 1 paddle
    paddle2_pos = HEIGHT/2					# initial position of the 2 paddle
    paddle1_vel = 0							# initial velocity of the 1 paddle 
    paddle2_vel = 0							# initial velocity of the 2 paddle 
    if random.randrange(-1, 1)<0:			#| randomizing of the start direction
        direction = RIGHT					#|
    else: direction = LEFT					#|
    spawn_ball(direction)					# call the spawn function
    color = "White"							# draws score counters in light color
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel, l_collide, r_collide, color	
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT - BALL_RADIUS):
        ball_vel[1] *= -1					
    elif ball_pos[0] > (WIDTH - PAD_WIDTH - BALL_RADIUS) and r_collide:
        ball_vel[0] *= -1.1					# increases ball velocity
    elif ball_pos[0] > (WIDTH - PAD_WIDTH - BALL_RADIUS):
        spawn_ball(LEFT)					# directs spawn in backward
        score1 += 1							# increases score player #1
        color = "White"						# draws score counters in light color
    elif ball_pos[0] < (BALL_RADIUS + PAD_WIDTH) and l_collide:
        ball_vel[0] *= -1.1					# increases ball velocity
    elif ball_pos[0] < (BALL_RADIUS + PAD_WIDTH): 
        spawn_ball(RIGHT)					# directs spawn in backward
        score2 += 1							# increases score player #2
        color = "White"						# draws score counters in light color
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 4, 'Orange', 'Yellow')
    
    # update paddle's vertical position, keep paddle on the screen   
    paddle1_pos += paddle1_vel
    if paddle1_pos <= HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
        paddle1_vel = 0
    elif paddle1_pos >= (HEIGHT-HALF_PAD_HEIGHT):
        paddle1_pos = (HEIGHT - HALF_PAD_HEIGHT)
        paddle1_vel = 0
        
    paddle2_pos += paddle2_vel
    if paddle2_pos >= (HEIGHT - HALF_PAD_HEIGHT):
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
        paddle2_vel = 0
    elif paddle2_pos <= HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
        paddle2_vel = 0 
        
    # draw paddles
    canvas.draw_line((PAD_WIDTH/2, paddle1_pos-HALF_PAD_HEIGHT), (PAD_WIDTH/2, paddle1_pos+HALF_PAD_HEIGHT), PAD_WIDTH, 'Red')   
    canvas.draw_line([(WIDTH - PAD_WIDTH/2), (paddle2_pos - HALF_PAD_HEIGHT)], [(WIDTH - PAD_WIDTH/2), (paddle2_pos + HALF_PAD_HEIGHT)], PAD_WIDTH, 'Blue')
    
    # determine whether paddle and ball collide    
    if (paddle2_pos-PAD_HEIGHT/2) <= ball_pos[1] and (paddle2_pos+PAD_HEIGHT/2) >= ball_pos[1]:
        r_collide = True
    elif (paddle1_pos-PAD_HEIGHT/2) <= ball_pos[1] and (paddle1_pos+PAD_HEIGHT/2) >= ball_pos[1]:
        l_collide = True
    else: l_collide = r_collide = False
    
    # draw scores
    canvas.draw_text(str(score1), (140, 60), 60, color, 'monospace')
    canvas.draw_text(str(score2), (430, 60), 60, color, 'monospace')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 5
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel = -5
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 5
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel = -5
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel = 0

def button_handler(): 
    new_game ()

    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT, 100)	
frame.set_canvas_background('Green')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Reset', button_handler, 100)

# start frame
new_game()
frame.start()
