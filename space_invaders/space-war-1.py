# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1102
HEIGHT = 620
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60
# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)

# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font("assets/fonts/font.ttf", 64)
FONT_XL = pygame.font.Font("assets/fonts/font.ttf", 96)

''' Make stars '''
stars = []
for i in range(800):
    x = random.randrange(-100, 1102)
    y = random.randrange(-200, 620)
    r = random.randrange(1, 5)
    s = [x, y, r, r]
    stars.append(s)
# Images
ship_img = pygame.image.load('assets/images/playerShip.png')

laser_img = pygame.image.load('assets/images/laserGreen.png')

hitmob_img = pygame.image.load('assets/images/enemyShip2.png')

mob_img = pygame.image.load('assets/images/enemyShip.png')

bomb_img = pygame.image.load('assets/images/laserRed.png')

start_screen = pygame.image.load('assets/images/startscreen().png')

explosion  = pygame.image.load('assets/images/explosion.png')

Untitled  = pygame.image.load('assets/images/Untitled.png')

# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
LASER_SHOT = pygame.mixer.Sound('assets/sounds/laser_shot.ogg')
DAMAGE = pygame.mixer.Sound('assets/sounds/damage.ogg')
GAME_MUSIC = pygame.mixer.Sound('assets/sounds/game_music.ogg')

# Stages
START = 0
PLAYING = 1
END = 2


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 4
        self.shield = 3

    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)
        LASER_SHOT.play()

    def update(self, bombs):
        hit_list = pygame.sprite.spritecollide(self, bombs, True)

        for hit in hit_list:
            DAMAGE.play()
            self.shield -= 1

        if self.shield == 0:
            EXPLOSION.play()
            self.kill()

        hit_list1 = pygame.sprite.spritecollide(self,mobs,False)
        hit_list2 = pygame.sprite.spritecollide(self,hitmobs,False)

        if len(hit_list1)>0 or len(hit_list2)>0:
            self.shield = 0
            
        if self.shield == 4:
            self.image = ship_img

        if self.shield == 3:
            self.image = ship_img

        if self.shield == 2:
            self.image = ship_img

        if self.shield == 1:
            self.image = ship_img

        if self.shield == 0:
            self.kill()
            

        

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill
    
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image, shield):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.shield = shield
    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
    
    def update(self, lasers):
        hit_list = pygame.sprite.spritecollide(self, lasers, True)

        for hit in hit_list:
            DAMAGE.play()
            self.shield -= 1

        if self.shield == 0:
            player.score += 20
            EXPLOSION.play()
            self.kill()

        hit_list = pygame.sprite.spritecollide(self,lasers,False)

        if len(hit_list)>0:
            self.shield = 0
            
        if self.shield == 2:
            self.image = mob_img

        if self.shield == 1:
            self.image = mob_img

        if self.shield == 0:
            self.kill()

class hitmob(pygame.sprite.Sprite):
    def __init__(self, x, y, image, health):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = health
        
    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
    
    def update(self, lasers):
        hit_list = pygame.sprite.spritecollide(self, lasers, True)

        for hit in hit_list:
            DAMAGE.play()
            self.health -= 1

        if self.health == 0:
            EXPLOSION.play()
            self.kill()
            player.score += 10

            

class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 10

    def update(self):
        self.rect.y += self.speed
    
    
class Fleet:

    def __init__(self, mobs, hitmobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 8
        self.bomb_rate = 30

    def move(self):
        reverse = False
        all_mobies = mobs.sprites() + hitmobs.sprites()
        for a in all_mobies:
            if self.moving_right:
                a.rect.x += self.speed
                if a.rect.right >= WIDTH:
                    reverse = True
            else:
                a.rect.x -= self.speed
                if a.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for a in all_mobies:
                a.rect.y += 32
                

            

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()

def setup():
    global ship,mobs,stage,player,bombs,lasers,fleet, hitmobs
    
    # Make game objects
    ship = Ship(444, 536, ship_img)
    hitmob1 = hitmob(128, 64, hitmob_img,1)
    hitmob2 = hitmob(256, 64, hitmob_img,1)
    hitmob3 = hitmob(384, 64, hitmob_img,1)
    hitmob4 = hitmob(512, 64, hitmob_img,1)
    hitmob5 = hitmob(640, 64, hitmob_img,1)
    hitmob6 = hitmob(128, -100, hitmob_img,1)
    hitmob7 = hitmob(256, -100, hitmob_img,1)
    hitmob8 = hitmob(384, -100, hitmob_img,1)
    hitmob9 = hitmob(512, -100, hitmob_img,1)
    hitmob10 = hitmob(640, -100, hitmob_img,1)
    
    mob6 = Mob(116, -30, mob_img,3)
    mob7 = Mob(243, -30, mob_img,3)
    mob8 = Mob(370, -30, mob_img,3)
    mob9 = Mob(497, -30, mob_img,3)
    mob10 = Mob(624, -30, mob_img,3)
    mob11 = Mob(116, -195, mob_img,3)
    mob12 = Mob(243, -195, mob_img,3)
    mob13 = Mob(370, -195, mob_img,3)
    mob14 = Mob(497, -195, mob_img,3)
    mob15 = Mob(624, -195, mob_img,3)

    # Make sprite groups
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0

    lasers =pygame.sprite.Group()

    mobs = pygame.sprite.Group()
    mobs.add(mob6, mob7, mob8, mob9, mob10, mob11, mob12, mob13, mob14, mob15)

    hitmobs = pygame.sprite.Group()
    hitmobs.add(hitmob1, hitmob2, hitmob3, hitmob4, hitmob5, hitmob6, hitmob7, hitmob8, hitmob9, hitmob10)

    bombs = pygame.sprite.Group()


    fleet = Fleet(mobs, hitmobs)

    # set stage
    stage = START

# Game helper functions
    
def show_title_screen():
    screen.blit(start_screen, [0,0])
    title_text = FONT_LG.render("Press space to begin", 1, WHITE)
    screen.blit(title_text, [55, 75])


def show_death_screen():
    death_text = FONT_LG.render("3 Strikes, You're Out", 1, RED)
    screen.blit(explosion, [350, 350])
    screen.blit(death_text, [178, 275])
    screen.blit(Untitled, [325, 50])

def show_win_screen():
    wun_text = FONT_LG.render("HOME RUN!", 1, GREEN)
    screen.blit(wun_text, [178, 275])
    
    
def show_stats(player):
    score_text = FONT_MD.render("score: " + str(player.score), 1, WHITE)
    shield_text = FONT_MD.render("shield:",1, WHITE)

    if ship.shield == 5:
        shield_display = FONT_MD.render("5",1, WHITE)
    elif ship.shield == 4:
        shield_display = FONT_MD.render("4",1, WHITE)
    elif ship.shield == 3:
        shield_display = FONT_MD.render("3",1, WHITE)

    elif ship.shield == 2:
        shield_display = FONT_MD.render("2",1, WHITE)
    elif ship.shield == 1:
        shield_display = FONT_MD.render("1",1, WHITE)
    else:
        shield_display = FONT_MD.render("XXX",1, WHITE)

    if ship.shield == 5:
        pygame.draw.rect(screen, WHITE, [20,100,100,18])
        pygame.draw.rect(screen, GREEN, [20,100,100,18])
    elif ship.shield == 4:
        pygame.draw.rect(screen, WHITE, [20,100,100,18])
        pygame.draw.rect(screen, GREEN, [20,100,80,18])
    elif ship.shield == 3:
        pygame.draw.rect(screen, WHITE, [20,100,100,18])
        pygame.draw.rect(screen, GREEN, [20,100,60,18])
    elif ship.shield == 2:
        pygame.draw.rect(screen, WHITE, [20,100,100,18])
        pygame.draw.rect(screen, GREEN, [20,100,40,18])
    elif ship.shield == 1:
        pygame.draw.rect(screen, WHITE, [20,100,100,18])
        pygame.draw.rect(screen, GREEN, [20,100,20,18])
    else:
        pygame.draw.rect(screen, RED, [20,100,0,18])

    




    
    screen.blit(score_text, [32, 32])
    screen.blit(shield_text, [32,64])
    screen.blit(shield_display, [118,64])
    
# Game loop
setup()
done = False
GAME_MUSIC.play()

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()

                    
            elif stage == END:
                if event.key == pygame.K_SPACE:
                    setup()

    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        
        player.update(bombs)
        lasers.update()
        hitmobs.update(lasers)
        mobs.update(lasers)
        bombs.update()
        fleet.update()
    if stage == PLAYING:
        if len(player) == 0:
            stage = END
        if len(mobs)== 0:
            stage = END
        

    for r in stars:
        r[1]+=2


        if r[1] > 620:
            r[1]= random.randrange(-800,-200)
            r[0]= random.randrange(-500,1102)
             

        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    ''' stars '''
    for s in stars:
        pygame.draw.ellipse(screen, WHITE, s)

    
    lasers.draw(screen)
    player.draw(screen)
    bombs.draw(screen)
    hitmobs.draw(screen)
    mobs.draw(screen)
    show_stats(player)

    if stage == START:
        show_title_screen()
    if stage == END:
        if len(player) == 0:
            show_death_screen()
        else:
            show_win_screen()

    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
