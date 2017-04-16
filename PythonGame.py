"""
Python Game

Shiv Lakhanpal
"""
 
import pygame, random, sys
 
# -- Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 244, 0)
RED = (255, 0, 0)
 
# Screen dimensions
SCREEN_WIDTH = 498
SCREEN_HEIGHT = 700
 
 
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()
        self.score = 0
        self.hiscore = 0
        self.color = ""
        self.lost = False
 
        # Set height, width, color
        self.image = pygame.Surface([30, 30])
        random_num = random.randint(1, 3)
        if random_num == 1:
            self.color = "red"
            self.image.fill(RED)
        if random_num == 2:
            self.color = "green"
            self.image.fill(GREEN)
        if random_num == 3:
            self.color = "blue"
            self.image.fill(BLUE)
 
        # Set initial location of object
        self.rect = self.image.get_rect()
        self.rect.y = 10
        self.rect.x = 235
 
        # Set speed vector
        self.change_x = 0
        self.change_y = 10 # Falling down
 
    def changespeed(self, x, y):
        """ Change the speed of the player. """
        self.change_x += 5 * x # Moves left and right
        self.change_y += 0
    
    def update(self):
        """ Update the player position. """
        # Move left/right
        if self.rect.x > 0 and self.rect.x < 465:        
            self.rect.x += self.change_x
        elif self.rect.x < 0:
            self.rect.x = 1
        elif self.rect.x > 465:
            self.rect.x = 464
            
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.buckets, False)
        score = 0
        for block in block_hit_list:
            if self.rect.x <= 166 and self.color == "red":
                self.score += 1
                if self.score > self.hiscore:
                    self.hiscore += 1
            elif self.rect.x > 166 and self.rect.x < 332 and self.color == "green":
                self.score += 1
                if self.score > self.hiscore:
                    self.hiscore += 1
            elif self.rect.x >= 332 and self.color == "blue":
                self.score += 1
                if self.score > self.hiscore:
                    self.hiscore += 1
            else:
                update_hiscore(self.score)
                self.score = 0
                self.change_y = 10

            # Reset our position and color based on the top/bottom of the object
            self.rect.y = 10
            random_num = random.randint(30, 450)
            self.rect.x = random_num
            random_num = random.randint(1, 3)
            if random_num == 1:        
                self.image.fill(RED)
                self.color = "red"
            if random_num == 2:
                self.image.fill(GREEN)
                self.color = "green"
            if random_num == 3:
                self.image.fill(BLUE)
                self.color = "blue"

            self.change_y += self.score * .1
            update_score(self.score)
            if self.score > self.hiscore:
                update_hiscore(self.score)
            
 
 
class Bucket(pygame.sprite.Sprite):
    """ Wall the player can run into. """
    def __init__(self, x, y, width, height, color):
        """ Constructor for the bucket that the player can run into. """
        # Call the parent's constructor
        super().__init__()
 
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])        
        self.image.fill(color)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
 
 
# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create a 500x700 sized screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
 
# Set the title of the window
pygame.display.set_caption('CS1122 Python Game')
 
# List to hold all the sprites
all_sprite_list = pygame.sprite.Group()
 
# Make the buckets. (x_pos, y_pos, width, height)
bucket_list = pygame.sprite.Group()

red_bucket = Bucket(0, 600, 166, 160, RED)
bucket_list.add(red_bucket)
all_sprite_list.add(red_bucket)

green_bucket = Bucket(166, 600, 166, 160, GREEN)
bucket_list.add(green_bucket)
all_sprite_list.add(green_bucket)

blue_bucket = Bucket(332, 600, 166, 160, BLUE)
bucket_list.add(blue_bucket)
all_sprite_list.add(blue_bucket)
 
# Create the player paddle object
player = Player(50, 50)
player.buckets = bucket_list
 
all_sprite_list.add(player)
 
clock = pygame.time.Clock()
 
done = False

high_score = 0

def update_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = 50
    screen.blit(text, textpos)

def update_hiscore(score):
    font2 = pygame.font.Font(None, 24)
    text = font2.render("Hi Score: " + str(score), 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = 45
    textpos.centery = 35
    screen.blit(text, textpos)
 
while not done:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(3, 0)
 
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3, 0)
 
    all_sprite_list.update()
 
    screen.fill(WHITE)

    all_sprite_list.draw(screen)

    update_score(player.score)
    
    update_hiscore(player.hiscore)
 
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
