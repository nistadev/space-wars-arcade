""" Llibraries """
try:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
except:
    import simplegui
import math
import random

""" Variables Globals """
# globals for user interface
mida = raw_input("Please, choose the canvas width. (For default values, leave this field blank)")
mida2 = raw_input("Please, choose the canvas height. (For default values, leave this field blank)")
time = 0
started = False
roundWinner = " "
gameWinner = " "
powers = ['DAcc', '3ple', 'INV', '1up', 'MTR', 'SPM']
powersMessage = {'DAcc': 'Velocity decrement', '3ple': 'Extra damage missile', 'INV': 'Inverted controls', 
                 '1up': 'Extra live!', 'MTR': 'Asteroids rain!', 'SPM': 'Invincible'}
clicked = False
ntw = 3
rotacio = 0
meteo = False
m_count = 0
    
""" Classes """
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center # returns the center that we set for the image
        self.size = size # size that we set for the image
        self.radius = radius # radius that we set for the image 
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

# Art assets created by Antonio Charneco and Patriciu Nista, may be freely re-used in non-commercial projects - Please credit they.
    
# debris images
debris_info = ImageInfo([400, 300], [800, 600])
#debris_image = simplegui.load_image("https://www.dropbox.com/s/sllvou17p60x9od/debris.png?dl=1")
debris_image2 = simplegui.load_image("https://www.dropbox.com/s/i8w8hel231rnuvq/debris2.png?dl=1")

# nebula images 
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("https://www.dropbox.com/s/yv6r0szf8y9v6wb/paisatge.png?dl=1")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("https://www.dropbox.com/s/gxh8o99lw2kk1a9/principi.png?dl=1")

# ship images
ship_info = ImageInfo([30, 35], [60, 70], 23)
ship_image = simplegui.load_image("https://www.dropbox.com/s/82o3qg30a94wyst/double_ship.png?dl=1")
ship_image2 = simplegui.load_image("https://www.dropbox.com/s/d163tu2n0yzfnue/double_ship_red.png?dl=1")
ship_image3 = simplegui.load_image("https://www.dropbox.com/s/i4fgvscotykeruz/double_ship_green.png?dl=1")

# superman image
superman_blue = simplegui.load_image("https://www.dropbox.com/s/e2xb9xp9v6nh2sf/superman_blue.png?dl=1")
superman_red = simplegui.load_image("https://www.dropbox.com/s/vf1rgfo2fhej0y2/superman_red.png?dl=1")
superman_green = simplegui.load_image("https://www.dropbox.com/s/bt67352pozp6kwl/superman_green.png?dl=1")

# missile
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_info2 = ImageInfo([9,11], [18, 9], 3, 50)
missile_image_blue = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
missile_image_red = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png") 
missile_image_blue2 = simplegui.load_image("https://www.dropbox.com/s/q580ydk1uql5llu/damage%20missile.png?dl=1")
missile_image_red2 = simplegui.load_image("https://www.dropbox.com/s/q580ydk1uql5llu/damage%20missile.png?dl=1")

# powerups
powerup_random = ImageInfo([11 + 69, 11 + 46], [22, 22], 11)
powerup_slower = ImageInfo([11, 11], [22, 22], 11)
powerup_missile = ImageInfo([11 + 69, 11], [22, 22], 11)
powerup_inverted = ImageInfo([11 + 23, 11 + 46], [22, 22], 11)
powerup_live = ImageInfo([11 + 69, 11 + 23], [22, 22], 11)
powerup_meteorit = ImageInfo([11 + 23, 11 + 23], [22, 22], 11)
powerup_superman = ImageInfo([11 + 23, 11], [22, 22], 11)
powerup_image = simplegui.load_image("https://www.dropbox.com/s/d24xbpwk6hmfbeh/powerups.png?dl=1")

# meteorits
meteorit_info = ImageInfo([45, 45], [90, 90], 40)
meteorit_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

#animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound effects
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.3)
ship_thrust_sound = simplegui.load_sound("http://giladayalonvegan.vkav.org/Python/thrust.mp3")
ship_thrust_sound.set_volume(.3)
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# background soundtrack - Copyright Subgeo, free to distribute and remix, but not to sell
soundtrack = simplegui.load_sound("https://www.dropbox.com/s/l83a6n5uh2pbdlw/Subgeo%20-%20Perhouse.mp3?dl=1")
soundtrack.set_volume(.7)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, image2, info, lives, name, color, number, missile, super_missile):
        self.pos = [pos[0], pos[1]] # object position
        self.vel = [vel[0], vel[1]] # object velocity vector
        self.thrust = False # thrust value
        self.angle = angle # angle value
        self.angle_vel = 0 # angle velocity
        self.image = image # image to display
        self.image2 = image2 # superman image to display
        self.image_center = info.get_center() # center of the image to display
        self.image_size = info.get_size() # size of the image to display
        self.missile = missile # missile image for each player
        self.missile2 = super_missile # super missile image for each player
        self.radius = info.get_radius() # radius of the object
        self.lives = lives # lives of the player
        self.name = name # player name
        self.color = color # color of the player
        self.gameswon = 0 # variable that keeps the value of the wins of the player over the games
        self.acc_const = 0.2 # acceleration constant, used to apply the decrement velocity powerup
        self.powerups = {'DAcc': False, '3ple': False, 'INV': False, '1up': False, 'MTR': False, 'SPM': False} # dictionary that stores if the powerups are activated
        self.powsec = 0 # seconds of timer
        self.powsec2 = 0 # seconds of timer2
        self.powsec3 = 0 # seconds of timer3
        self.powsec4 = 0 # seconds of timer4
        self.powsec5 = 0 # seconds of timer4
        self.player = number # number of player to determine the timer to start
        self.damaged = False # determine if player was damaged
        self.extsec = 5 # seconds of energy timer (wait 5 to get more energy)
        self.destroyed = False # determine if the player was destroyed
        
    def wins(self):
        return self.gameswon
            
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def mylives(self):
        return self.lives
    
    def nickname(self):
        return self.name
    
    def draw(self,canvas):
        global rotacio
        # if thrust draw image with fire, else draw it without fire
        if self.thrust:   
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # display superman powerup if activated
        if self.powerups['SPM']:
            canvas.draw_image(self.image2, self.image_center, self.image_size,
                              self.pos, self.image_size, rotacio)
            rotacio += .01
        # draw the player name
        canvas.draw_text(self.name, [self.pos[0] - 20, self.pos[1] + self.radius + 20], 25, self.color)
        # determine if the powerup is activated and display his power, if more than one, displays one after another
        var = 35
        for e in self.powerups:
            if self.powerups[e] == True:
                if not e == 'MTR':
                    canvas.draw_text(powersMessage[e], [self.pos[0] - 20, self.pos[1] + self.radius + var], 17, '#fff')
                    var += 20
                
    def update(self):
        # update angle
        self.angle += self.angle_vel
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * self.acc_const
            self.vel[1] += acc[1] * self.acc_const
        # friction    
        self.vel[0] *= .98
        self.vel[1] *= .98
           
    def set_thrust(self, on):
        # plays the sound if thrust is on
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def aangle_vel(self, angle):
        # determine if the powerup of inverted controls is activated and update angle vel
        if self.powerups['INV']:
            if angle == 'left':
                self.angle_vel += .10
            elif angle == 'right':
                self.angle_vel -= .10
            else:
                self.angle_vel = 0
        else:
            if angle == 'left':
                self.angle_vel -= .10
            elif angle == 'right':
                self.angle_vel += .10
            else:
                self.angle_vel = 0

    def addwin(self):
        # if the player win, it adds a win
        self.gameswon += 1 
        
    def shoot(self):
        # shot method that is activated when player press the shoot key
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_pos2 = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_pos3 = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missile = Sprite(missile_pos, missile_vel, self.angle, 0, self.missile, missile_info, "", missile_sound)
        missile2 = Sprite(missile_pos2, missile_vel, self.angle, 0, self.missile, missile_info, "", missile_sound)
        missile3 = Sprite(missile_pos3, missile_vel, self.angle, 0, self.missile2, missile_info2, "", missile_sound)
        # if missile powerup is active, create 2 missiles, else only one
        if self.powerups['3ple']:
            missile_group.add(missile)
            missile_group.add(missile3)
        else:
            missile_group.add(missile)
    
    def declives(self):
        # decrement lives
        self.lives -= 1
      
    def collide(self, other_object):
        # determine collide
        p = self.pos
        q = other_object.get_pos()
        distance = dist(p, q)
        if distance > self.radius + other_object.get_radius():
            return False
        else:
            return True        
     
    def poweruped(self, powerup):
        # set the powerup and add time to the timer
        if powerup == 'DAcc':
            self.powsec += 7
        elif powerup == '3ple':
            self.powsec2 += 7
        elif powerup == 'INV':
            self.powsec3 += 7
        elif powerup == 'SPM':
            self.powsec4 += 7
        elif powerup == '1up':
            self.powsec5 += 1
            
        self.powerups[powerup] = True
                    
    def powerup_timer(self):
        global m_count, meteo
        #print self.powsec, self.powsec2, self.powsec3
        # timer for powerups
        if self.powerups['DAcc']:
            if self.powsec > 0:
                self.acc_const = 0.05
                self.powsec -= 1
            else:
                self.acc_const = 0.2
                self.powerups['DAcc'] = False
                self.powsec = 0
                
        if self.powerups['3ple']:
            if self.powsec2 > 0:
                self.powerups['3ple'] = True
                self.powsec2 -= 1
            else:
                self.powerups['3ple'] = False
                self.powsec2 = 0
                
        if self.powerups['INV']:
            if self.powsec3 > 0:
                self.powerups['INV'] = True
                self.powsec3 -= 1
            else:
                self.powerups['INV'] = False
                self.powsec3 = 0
                
        if self.powerups['SPM']:
            if self.powsec4 > 0:
                self.powerups['SPM'] = True
                self.powsec4 -= 1
            else:
                self.powerups['SPM'] = False
                self.powsec4 = 0
        
        if self.powerups['1up']:
            energy = range(5)
            if self.powsec5 > 0 and not self.lives > 44:
                if self.lives + 5 <= 45:
                    self.lives += energy[-1]
                elif self.lives + 4 <= 45:
                    self.lives += energy[3]
                elif self.lives + 3 <= 45:
                    self.lives += energy[2]
                elif self.lives + 2 <= 45:
                    self.lives += energy[1]
                elif self.lives + 1 <= 45:
                    self.lives += energy[0]
                    
                #self.lives += random.randint(2, 5)
                self.powsec5 -= 1
            else:
                self.powerups['1up'] = False
            
        if self.powerups['MTR']:
            m_count += 23
            meteo = True
            if not meteoritos.is_running():
                meteoritos.start()
            self.powerups['MTR'] = False
    
    def powerAndEnergy(self):
        if self.extsec > 0:
            self.extsec -= 1
            self.damaged = True
        else:
            self.damaged = False
            
        if started and clicked and not self.damaged:
            energy1 = 3
            energy2 = 2
            energy3 = 1
            if self.lives + 3 <= 45:
                self.lives += energy1
            elif self.lives + 2 <= 45:
                self.lives += energy2
            elif self.lives + 1 <= 45:
                self.lives += energy3
                
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, name = "", sound = None):
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
        self.name = name
        if sound:
            sound.rewind()
            sound.play()
    
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        dead = False
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
                    
        if self.age >= self.lifespan:
            dead = True
        return dead
    
    def collide(self, other_object):
        global lives
        p = self.pos
        q = other_object.get_pos()
        distance = dist(p, q)
        if distance > self.radius + other_object.get_radius():
            return False
        else:
            return True

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, clicked
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not clicked) and inwidth and inheight:
        new_round()
        clicked = True
        countdown.start()
        #soundtrack.play()
        
# new round function
def new_round():
    global powerups_group, missile_group, meteorit, a_count, meteo, count
    for i in ships:
        i.lives = 30
        i.powerups = {'DAcc':False,'3ple':False, 'INV':False, '1up':False, 'MTR': False, 'SPM': False}
        i.acc_const = 0.2
        i.extsec = 5
        i.damaged = False
        #i.destroyed = False
    if (my_ship.gameswon or my_ship2.gameswon) == 0:
        count = 10
    else:
        count = 5
    #soundtrack.rewind()
    powerups_group = set([])
    missile_group = set([])
    meteorit = set([])
    meteo = False
    a_count = 0

# new game function
def new_game():
    global powerups_group, missile_group, meteorit, a_count, meteo, clicked, started
    clicked = False
    started = False
    for i in ships:
        i.lives = 30
        i.powerups = {'DAcc':False,'3ple':False, 'INV':False, '1up':False, 'MTR': False, 'SPM': False}
        i.acc_const = 0.2
        i.extsec = 5
        i.damaged = False
        i.destroyed = False
        i.gameswon = 0
        i.vel = [0, 0]
        i.angle = 0
    
    my_ship.pos = [WIDTH / 3, HEIGHT / 2]
    my_ship2.pos = [WIDTH / 1.5, HEIGHT / 2]
    #soundtrack.rewind()
    powerups_group = set([])
    missile_group = set([])
    meteorit = set([])
    meteo = False
    a_count = 0

# reset the wins handler
def reset_wins():
    for i in ships:
        i.gameswon = 0
    new_round()
    
# exit the game
def exit_game():
    timer.stop()
    p1.stop()
    p2.stop()
    energy1.stop()
    energy2.stop()
    frame.stop()
    
# key handlers to control ship   
def keydown(key):
    # player1
    if not my_ship.destroyed:
        if key == simplegui.KEY_MAP['a']:
            my_ship.aangle_vel('left')
        elif key == simplegui.KEY_MAP['d']:
            my_ship.aangle_vel('right')
        elif key == simplegui.KEY_MAP['w']:
            my_ship.set_thrust(True)
        elif key == simplegui.KEY_MAP['f']:
            my_ship.shoot()
    # player2
    if not my_ship2.destroyed:
        if key == simplegui.KEY_MAP['j']:
            my_ship2.aangle_vel('left')
        elif key == simplegui.KEY_MAP['l']:
            my_ship2.aangle_vel('right')
        elif key == simplegui.KEY_MAP['i']:
            my_ship2.set_thrust(True)
        elif key == simplegui.KEY_MAP['h']:
            my_ship2.shoot()
        
def keyup(key):
    # player1
    if not my_ship.destroyed:
        if key == simplegui.KEY_MAP['a']:
            my_ship.aangle_vel('righ')
        elif key == simplegui.KEY_MAP['d']:
            my_ship.aangle_vel('lef')
        elif key == simplegui.KEY_MAP['w']:
            my_ship.set_thrust(False)
    # player2
    if not my_ship2.destroyed:
        if key == simplegui.KEY_MAP['j']:
            my_ship2.aangle_vel('righ')
        elif key == simplegui.KEY_MAP['l']:
            my_ship2.aangle_vel('lef')
        elif key == simplegui.KEY_MAP['i']:
            my_ship2.set_thrust(False)
        

def draw(canvas):
    global time, started, winner
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image2, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image2, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    if meteo:
        canvas.draw_text('Asteroids rain! ', [WIDTH / 2.70, HEIGHT / 1.2], 60, "Red")
    
    # players nicknames
    canvas.draw_text(str(my_ship.nickname()), [50, 40], 22, "White")
    canvas.draw_text(str(my_ship2.nickname()), [WIDTH-300, 40], 22, "White")
    
    # player 1 wins
    if my_ship.gameswon == 0:
        pass
    elif my_ship.gameswon > 0:
        lloc = 0
        for i in range(my_ship.gameswon):
            canvas.draw_circle([217.5 + lloc, 35], 5, 1, my_ship.color, my_ship.color)
            lloc += 20
    
    canvas.draw_circle([217.5, 35], 5, 1, "Black")
    canvas.draw_circle([237.5, 35], 5, 1, "Black")
    canvas.draw_circle([257.5, 35], 5, 1, "Black")
    # player 2 wins
    if my_ship2.gameswon == 0:
        pass
    elif my_ship2.gameswon > 0:
        lloc2 = 0
        for i in range(my_ship2.gameswon):
            canvas.draw_circle([(WIDTH-132.5) + lloc2, 35], 5, 1, my_ship2.color, my_ship2.color)
            lloc2 += 20
            
    canvas.draw_circle([WIDTH-132.5, 35], 5, 1, "Black")
    canvas.draw_circle([WIDTH-112.5, 35], 5, 1, "Black")
    canvas.draw_circle([WIDTH-92.5, 35], 5, 1, "Black")
    
    # Energy Bars
    UPDISTANCE = 55
    canvas.draw_line([50, UPDISTANCE], [(50 + my_ship.mylives() * 5), UPDISTANCE], 12, my_ship.color)
    canvas.draw_polygon([[49, UPDISTANCE - 5], [200, UPDISTANCE - 5], [200, UPDISTANCE + 5], [49, UPDISTANCE + 5]], 2, "Black")
    canvas.draw_polygon([[200, UPDISTANCE - 5], [275, UPDISTANCE - 5], [275, UPDISTANCE + 5], [200, UPDISTANCE + 5]], 2, "Black")
    canvas.draw_line([WIDTH-300, UPDISTANCE], [((WIDTH - 300) + my_ship2.mylives() * 5), UPDISTANCE], 12, my_ship2.color)
    canvas.draw_polygon([[WIDTH-300, UPDISTANCE - 5], [WIDTH - 150, UPDISTANCE - 5], [WIDTH - 150, UPDISTANCE + 5], [WIDTH-300, UPDISTANCE + 5]], 2, "Black")
    canvas.draw_polygon([[WIDTH-150, UPDISTANCE - 5], [WIDTH - 75, UPDISTANCE - 5], [WIDTH - 75, UPDISTANCE + 5], [WIDTH-150, UPDISTANCE + 5]], 2, "Black")
    
    # draw ship and sprites
    for d in ships:
        if not d.destroyed:
            d.draw(canvas)

    # update ship and sprites
    for i in ships:
        if not i.destroyed:
            i.update()

    process_sprite_group(missile_group, canvas)
    process_sprite_group(powerups_group, canvas)
    process_sprite_group(meteorit, canvas)
    meteorit_disapear(meteorit)
    
    # call helper functions to determine collides
    for i in ships:
        powerups_collide(powerups_group, i)    
    
    for e in ships:
        group_collide(missile_group, e)
        group_collide(meteorit, e)
    
    if not clicked:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    if not started and clicked:
        canvas.draw_text(str(count), [WIDTH / 2.1, HEIGHT / 1.5], 50, "White")
        canvas.draw_text(roundWinner, [WIDTH / 3.2, HEIGHT / 1.2], 35, "White")
    
    if not clicked and not started:
        canvas.draw_text(gameWinner, [WIDTH / 3.5, HEIGHT / 1.2], 35, "White")
    

""" Funcions """
# formulas
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# draw sprites
def process_sprite_group(group, canvas):
    for sprite in set(group):
        sprite.draw(canvas)
        if sprite.update():
            group.remove(sprite)

# collide functions
def group_collide(group, other_object):
    global started, clicked, count, roundWinner, gameWinner
    for o in set(group):
        if o.collide(other_object):
            other_object.extsec = 5
            if started and not other_object.mylives() == 0:
                if not other_object.powerups['SPM']:
                    other_object.declives()
            
            if other_object.mylives() == 0 and started:
                started = False
                clicked = True
                count = 5
                if other_object.nickname() == my_ship2.name:
                    other_object.destroyed = True
                    other_object.pos[0] = random.randrange(0, WIDTH)
                    other_object.pos[1] = random.randrange(0, HEIGHT)
                    my_ship.addwin()
                    roundWinner = "Player " + str(my_ship.name) + " win this round."
                elif other_object.nickname() == my_ship.name:
                    other_object.destroyed = True
                    other_object.pos[0] = random.randrange(0, WIDTH)
                    other_object.pos[1] = random.randrange(0, HEIGHT)
                    my_ship2.addwin()
                    roundWinner = "Player " + str(my_ship2.name) + " win this round."
                    
                    
                if (my_ship.wins() >= ntw) or (my_ship2.wins() >= ntw):
                    started = False
                    clicked = False
                    count = 10
                    if my_ship.wins() >= ntw:
                        roundWinner = " "
                        gameWinner = "Player " + str(my_ship.name) + " win the game."
                    if my_ship2.wins() >= ntw:
                        roundWinner = " "
                        gameWinner = "Player " + str(my_ship2.name) + " win the game."
                    new_game()
                
                if not started and clicked:
                    new_round()
                    countdown.start()
            group.remove(o)

def powerups_collide(group1, group2):
    global started
    for o in set(group1):
        if o.collide(group2):
            if o.name == "Rnd":
                group2.poweruped(random.choice(powers))
                group1.remove(o)
            else:
                group2.poweruped(o.name)
                group1.remove(o)

def meteorit_disapear(group):
    for i in group:
        if i.pos[1] > HEIGHT - i.radius:
            group.remove(i)

def widthFunct(value):
    global WIDTH
    if value == "" or value == "None":
        value = 0
        
    value2 = int(value)
    if value2 >= 800:
        WIDTH = value2
    else:
        WIDTH = 800
        
def heightFunct(value):
    global HEIGHT, mida_canvas
    mida_canvas = False
    if value == "" or value == "None":
        value = 0
        
    value2 = int(value)
    if value2 >= 600:
        HEIGHT = value2
        mida_canvas = True
    else:
        HEIGHT = 600
        mida_canvas = True
        
    
""" Timers """
# timer handler that spawns a powerup    
def powerup_spawner():
    global powerups_group, powerups_sprites
    powerup_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    powerup_vel = [0, 0]
    powerup_avel = 0
    powerups_sprites = [Sprite(powerup_pos, powerup_vel, 0, powerup_avel, powerup_image, powerup_slower, "DAcc"),
                        Sprite(powerup_pos, powerup_vel, 0, powerup_avel, powerup_image, powerup_random, "Rnd"),
                        Sprite(powerup_pos, powerup_vel, 0, powerup_avel, powerup_image, powerup_missile, "3ple"),
                        Sprite(powerup_pos, powerup_vel, 0, powerup_avel, powerup_image, powerup_live, "1up"),
                        Sprite(powerup_pos, powerup_vel, 0, powerup_avel, powerup_image, powerup_inverted, "INV"),
                        Sprite(powerup_pos, powerup_vel, 0, powerup_avel, powerup_image, powerup_meteorit, "MTR"),
                        Sprite(powerup_pos, powerup_vel, 0, powerup_avel, powerup_image, powerup_superman, "SPM")]
    
    if started:
        for i in ships:
            if dist(powerup_pos, i.get_pos()) < 100:
                pass
        else:
            if len(powerups_group) < 5:
                powerups_group.add(random.choice(powerups_sprites))

def meteorits_spawner():
    global meteorit, m_count, meteo
    meteorit_pos = [random.randrange(0, WIDTH), 0]
    meteorit_vel = [0, 2] #[random.random() * .6 - .3, random.random() * .6 - .3]
    meteorit_avel = random.random() * .2 - .1
    meteorit_sprite = Sprite(meteorit_pos, meteorit_vel, 0, meteorit_avel, meteorit_image, meteorit_info)
    
    if meteo:
        if m_count > 0:
            if m_count % 2 == 1:
                meteorit.add(meteorit_sprite)
            m_count -= 1
        else:
            meteo = False
            m_count = 0
            meteoritos.stop()
                
def countdown_timer():
    global count, started, roundWinner, gameWinner
    if count > 1:
        count -= 1
    else:
        for i in ships:
            i.destroyed = False
        started = True
        roundWinner = " "
        gameWinner = " "
        countdown.stop()
        

""" initialize stuff """
# size of frame 
widthFunct(mida)
heightFunct(mida2)

# frame
frame = simplegui.create_frame("Space Wars", WIDTH, HEIGHT)

# players
my_ship = Ship([WIDTH / 3, HEIGHT / 2], [0, 0], 0, ship_image, superman_blue, ship_info, 10, "Antonio", "#22f", 1, missile_image_blue, missile_image_blue2)
my_ship2 = Ship([WIDTH / 1.5, HEIGHT / 2], [0, 0], 0, ship_image2, superman_red, ship_info, 10, "Pat", "#f22", 2, missile_image_red, missile_image_red2)
ships = [my_ship, my_ship2]

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
frame.add_button("New Game", new_game)
frame.add_label("")
frame.add_button("Reset Game", reset_wins)
frame.add_label("")
frame.add_button("Exit", exit_game)
timer = simplegui.create_timer(8500, powerup_spawner)
meteoritos = simplegui.create_timer(1000, meteorits_spawner)
countdown = simplegui.create_timer(1000, countdown_timer)
energy1 = simplegui.create_timer(2500, my_ship.powerAndEnergy)
energy2 = simplegui.create_timer(2500, my_ship2.powerAndEnergy)
p1 = simplegui.create_timer(1000, my_ship.powerup_timer)
p2 = simplegui.create_timer(1000, my_ship2.powerup_timer)

# get things rolling

if mida_canvas:
    new_game()
    timer.start()
    frame.start()
    p1.start()
    p2.start()
    energy1.start()
    energy2.start()
