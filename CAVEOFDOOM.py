import pygame, random
from sys import exit
from pygame.locals import *

# initialization 
pygame.init()

#player info
x = 450
y = 840

#window info
screen_w = 500
screen_h = 600

#main menu etc
click = False

#text
white = (255, 255, 255)
font = pygame.font.Font('freesansbold.ttf', 32)
score_val = 0
textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score: " + str(score_val), True, (white))
    screen.blit(score, (x, y))

counter = 0

#main mennu etc
def main_menu():
    while True:
        #menu background
        menu_background = pygame.image.load('gameGraphics/menu1.png')
        menu_background = pygame.transform.scale(menu_background, (screen_w,screen_h)).convert()
        screen.blit(menu_background,(0,0))
       
        #menu buttons
        mx, my = pygame.mouse.get_pos()
        play_button = pygame.image.load('gameGraphics/play_button.png').convert_alpha()
        play_button = pygame.transform.scale(play_button, (400,400))
        screen.blit(play_button,(0,380))
        
        play_button_rect = play_button.get_rect(topleft=(-150, 240))

        if play_button_rect.collidepoint((mx,my)):
            if click:
                game()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        clock.tick(60)


# player movement etc


class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        global game_state
        
        # super().__init__()

        self.player_surf = pygame.image.load('gameGraphics/player_stand.png').convert_alpha()
        #scaled player image
        self.player_surf = pygame.transform.scale(self.player_surf,(500,500))
        self.rect = self.player_surf.get_rect(midbottom = (x,y), width = 10, height = 100)
        
        self.x_speed = 5
        self.health = 1
        self.score = 0

class Gem(pygame.sprite.Sprite):
    
    def __init__(self):
        self.x = random.randrange(0, screen_w)
        self.y = -20
        self.vel = 4
        self.gem_image = [pygame.image.load('gems:spikes/blueGem.png'),
                          pygame.image.load('gems:spikes/redGem.png'),
                          pygame.image.load('gems:spikes/greenGem.png'),
                          pygame.image.load('gems:spikes/yellowGem.png')]
        self.gem_image = [pygame.transform.scale(img, (90, 90)) for img in self.gem_image]
        self.counter = 0
        self.rect = self.gem_image[counter].get_rect(midbottom=(self.x, self.y), width = -500, height = 0)
        
    def update_y(self):
        global score_val
        self.y += self.vel
        self.collide = self.rect.colliderect(player.rect)
        if self.y > screen_h:
            self.y = -20
            self.x = random.randrange(0, screen_w)
            self.counter = (self.counter + 3) % len(self.gem_image)
        self.rect = self.gem_image[self.counter].get_rect(midbottom=(self.x - 150, self.y - 40))
        if self.collide:
            self.y = 0
            self.x = random.randrange(0, 490)
            self.counter  = (self.counter + 3) % len(self.gem_image)
            score_val += .5
            
class Spike(pygame.sprite.Sprite):
    
    def __init__(self):
        self.x = random.randrange(0,screen_w)
        self.y = -20
        self.vel = 6
        self.spike_image = pygame.image.load('gems:spikes/spike.png')
        self.spike_image = pygame.transform.scale(self.spike_image,(120,120))
        self.rect = self.spike_image.get_rect(midbottom = (x,y))
        self.update_y()
        
    def update_y(self):
        self.y += self.vel
        self.rect = self.spike_image.get_rect(midbottom=(self.x - 150, self.y - 40))
        if self.y > screen_h:
            self.y = -20
            self.x = random.randrange(0, screen_w)
            self.rect = self.spike_image.get_rect(midbottom=(self.x, self.y))
        self.collide = self.rect.colliderect(player.rect)
        if self.collide:
            self.y = 0
            self.x = random.randrange(0, screen_w)
            player.health -= 1
            
#window stuff

screen = pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption('Cave Of Doom')

#clock

clock = pygame.time.Clock()

#background

cave_surf = pygame.image.load('gameGraphics/background.png').convert()
cave_surf = pygame.transform.scale(cave_surf, (screen_w,screen_h)).convert()

player = Player()
gem = Gem()
spike = Spike()

def end_game():
    global score_val
    score_val = 0

#game loop
def game():
   
    running = True
    while running:
    
        clock.tick(60)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player.rect.x += player.x_speed
        elif keys[pygame.K_LEFT]:
            player.rect.x -= player.x_speed 
        player.update()

        if player.rect.x < -130:
            player.rect.x = -130
        elif player.rect.x > 260:
            player.rect.x = 260
        player.update()
            
        if player.health <= 0:
            end_game()
            running = False
            player.health = 1

        

        screen.fill((0,0,0))
        screen.blit(cave_surf,(0,0))
        screen.blit(player.player_surf,player.rect)
        
        screen.blit(gem.gem_image[gem.counter],(gem.x, gem.y))
        screen.blit(spike.spike_image, (spike.x,spike.y))
        
        show_score(textX,textY)

        pygame.display.update()
    
        gem.update_y()
        spike.update_y()
        player.update()
        
main_menu()