# program template for Spaceship

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
rock_group = set ()
missile_group = set ()
explosion_group = set ()

class ImageInfo:													
    def __init__(self, center, size, radius = 0, 					
                 lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):											
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(0.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group (sprite_group, canvas):
    # draws and updates a multiple sprites
    for new_sprite in set (sprite_group):
        if not new_sprite.update():
            new_sprite.draw(canvas)
            new_sprite.update()
        else:
            sprite_group.remove (new_sprite)       

def group_collide (group, something):
    global explosion_group
    for rock in set (group):
        if rock.collide(something):
            explosion_pos = rock.pos
            explosion = Sprite(explosion_pos, [0, 0], 0, 0, explosion_image, 
                               explosion_info, explosion_sound)
            explosion_group.add (explosion)
            group.discard(rock)
            
            return True

def group_group_collide (missile_group, rock_group):
    for missile in set (missile_group):
        if group_collide (rock_group, missile):
            missile_group.discard(missile)
            return True       
        
# Ship class
class Ship:
    
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self,canvas):
        if not self.thrust:
            canvas.draw_image (self.image, self.image_center, self.image_size, 
                           self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image (self.image, (self.image_center[0]*3, self.image_center[1]), self.image_size, 
                           self.pos, self.image_size, self.angle)
        
    def update(self):
        global ship_thrust_sound, forward
        
        # update position
        self.pos[0] = (self.pos[0] +self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] +self.vel[1]) % HEIGHT
        
        # update angle
        self.angle += self.angle_vel*0.98
        
        # update velocity
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += 0.1*forward[0]
            self.vel[1] += 0.1*forward[1]
            ship_thrust_sound.play()
        else: 
            ship_thrust_sound.rewind()
            self.vel[0] *= 0.985
            self.vel[1] *= 0.985

    def get_radius(self):
        return self.radius            
            
    def get_position(self):
        return self.pos            
            
    def thrust_on(self, thrust):        
        self.thrust = thrust    
    
    #draws missile shoot
    def shoot(self):
        global missile_group
        new_missile = Sprite([self.pos[0]+ forward[0] * self.radius, self.pos[1]+ forward[1] * self.radius], 
                           [self.vel[0] + forward[0]*4, self.vel[1] + forward[1]*4], 
                           0, 0, missile_image, missile_info, missile_sound)
        return missile_group.add (new_missile)
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            for age in range (self.age):
                canvas.draw_image(self.image, [self.image_center[0]*self.age, self.image_center[1]], 
                                  self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                           self.pos, self.image_size, self.angle)
        
    def update(self):
        # update angle
        self.angle += self.angle_vel
        self.age +=1
        if self.lifespan <= self.age:
            return True
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
        
    # detects collisions Sprites with other objects
    def collide (self, something):
        smth_pos = something.get_position()
        smth_rad = something.get_radius()
        sprite_pos = Sprite.get_position(self)
        sprite_rad = Sprite.get_radius(self)
        if dist(sprite_pos, smth_pos) <= smth_rad + sprite_rad:
            return True
        else:
            return False
        
# draw handler        
def draw(canvas):
    global time, lives, score, started, rock_group, missile_group, explosion_
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # draw UI
    if group_collide (rock_group, my_ship):
        lives -=1
    if group_group_collide (missile_group, rock_group):
        score +=100        
    canvas.draw_text('lives', (50, 50), 20, 'White')
    canvas.draw_text(str(lives), (65, 70), 20, 'White')
    canvas.draw_text('score', (WIDTH-100, 50), 20, 'White')
    canvas.draw_text(str(score), (WIDTH-80, 70), 20, 'White')

    # draw ship
    my_ship.draw(canvas)
        
    # update ship and sprites
    my_ship.update()
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())    
    
    # call function for draws and updates rocks and missiles
    process_sprite_group (rock_group, canvas)
    process_sprite_group (missile_group, canvas)
    process_sprite_group (explosion_group, canvas)

    if lives == 0:
        started = False
        rock_group = set ()
        missile_group = set ()   
        soundtrack.rewind()
        
# key_handlers
def key_down(key):
    if key==simplegui.KEY_MAP["left"]:
        my_ship.angle_vel -= math.pi/45
    elif key==simplegui.KEY_MAP["right"]:
        my_ship.angle_vel += math.pi/45
    elif key==simplegui.KEY_MAP["up"]:
        my_ship.thrust_on(True)
    elif key==simplegui.KEY_MAP["space"]:
        my_ship.shoot()
    
def key_up(key):
    if key==simplegui.KEY_MAP["up"]:
        my_ship.thrust_on(False)
    elif key==simplegui.KEY_MAP["left"]:
        my_ship.angle_vel += math.pi/45
    elif key==simplegui.KEY_MAP["right"]:
        my_ship.angle_vel -= math.pi/45
        
    
# timer handler that spawns a rock    
def rock_spawner():
    global spawn_pos, rock_group
    choice = random.choice((-1, 1))
    spawn_pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
    spawn_vel = [random.random() * choice * 2, random.random() * choice * 2]
    spawn_ang = random.random() * choice * 0.1					
    distance = dist(spawn_pos, my_ship.get_position())
    while started and distance > 200 and len (rock_group) < 12:
        new_rock = Sprite(spawn_pos, spawn_vel, 0, spawn_ang, 
                        asteroid_image, asteroid_info)
        return rock_group.add (new_rock)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        lives = 3
        score = 0    
        started = True
        soundtrack.play()
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#new_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, math.pi/360, asteroid_image, asteroid_info)
new_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, 
                   missile_image, missile_info, missile_sound)


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
