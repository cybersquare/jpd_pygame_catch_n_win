import pygame
from pygame.locals import *
import random, time

#Initializing
pygame.init()

collided = False
score = 0
last_tick = pygame.time.get_ticks()

#Setting up FPS to limit the number of executions per second
FPS = 60 # Execute the loop 60 times a second
FramePerSec = pygame.time.Clock()

#Creating colors 
RED   = (255, 0, 0)
WHITE = (255, 255, 255)

#Create a screen with background 
screen = pygame.display.set_mode((900,700))
pygame.display.set_caption("Catch and win")
bg = pygame.image.load("images/bg1.png")

class Enemy(pygame.sprite.Sprite): # Rocket ship
    def __init__(self):
        super().__init__() 
        self.images = [] # Image list 
        self.index = 0
        # Images for creating animation
        self.images.append(pygame.image.load("images/space_ship1.png"))
        self.images.append(pygame.image.load("images/space_ship2.png"))
        self.images.append(pygame.image.load("images/space_ship3.png"))
        self.images.append(pygame.image.load("images/space_ship4.png"))
        self.images.append(pygame.image.load("images/space_ship5.png"))
        self.image = self.images[0]
        self.surf = pygame.Surface((50, 65)) 
        self.size = self.image.get_size()
        self.rect = self.surf.get_rect(center = (random.randint(40, 900),0))
         
    def move(self):
        global collided
        self.rect.move_ip(0,5)
        self.image=self.images[self.index] # Change image for animation effect
        if self.index < 4: # Change index for selecting image from list
            self.index += 1
        else:
            self.index = 0
        # Move the enmey to top if it crosses the window
        if self.rect.bottom > 600 or collided: 
            self.rect.top = 0
            self.rect.center = (random.randint(40, 850), 0)
        
    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect, 2) 
        # Change image size
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*0.2), int(self.size[1]*0.2)))
        surface.blit(self.image, self.rect) 
 
 
class Player(pygame.sprite.Sprite): # Dan
    def __init__(self):
        super().__init__() 
        self.images = []
        self.index = 0
        self.images.append(pygame.image.load('images/dan-a.png'))
        self.images.append(pygame.image.load('images/dan-b.png'))
        self.image = self.images[0]
        self.surf = pygame.Surface((70, 100)) 
        self.rect = self.surf.get_rect(center = (50, 550)) 
        self.size = self.image.get_size()
    
    def update(self): # Move player on keypress
        pressed_keys = pygame.key.get_pressed()
        # Image selection index from the list
        if self.index:
            self.index = 0
        else:
            self.index = 1
        if self.rect.left > 0: # Move and animate character on keypress
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
                  self.image = self.images[self.index]

        if self.rect.right < 1000: # Move and animate character on keypress       
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                  self.image = self.images[self.index]
 
    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect, 2) # Check it
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))
        surface.blit(self.image, self.rect)  


class Friend(pygame.sprite.Sprite): # Balloons and apple
    def __init__(self):
        super().__init__() 
        self.images=[]
        self.images.append(pygame.image.load('images/apple.png'))
        self.images.append(pygame.image.load('images/balloon1.png'))
        self.images.append(pygame.image.load('images/balloon2.png'))
        self.images.append(pygame.image.load('images/balloon3.png'))
        self.surf = pygame.Surface((30, 65)) 
        self.rect = self.surf.get_rect(center = (random.randint(40, 900),0))
        self.image = self.images[0]
        self.size = self.image.get_size()

    def move(self):
        self.rect.move_ip(0,5)
        
 
    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect, 2) 
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*0.1), int(self.size[1]*0.2)))
        surface.blit(self.image, self.rect)  


#Setting up Sprites        
P1 = Player()
E1 = Enemy()
F1 = Friend()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
friends = pygame.sprite.Group()
enemies.add(E1)
friends.add(F1)

while True:     
    # Quit game on pressing the close button
    for event in pygame.event.get():              
        if event.type == pygame.QUIT:
            pygame.quit()
    
    screen.blit(bg, (0, 0))
    if not collided:
        P1.update()
        E1.move()

    # Create new friend sprite in every second
    now = pygame.time.get_ticks()
    if now - last_tick > 1000 and not collided:
        last_tick = pygame.time.get_ticks()
        new_friend = Friend()
        # Random selection of balloons and apple
        new_friend.image = new_friend.images[random.randint(0, 3)]
        friends.add(new_friend) # Add new sprite to sprite group

    for friend in friends:
        friend.draw(screen)
        friend.move()
        if friend.rect.top > 700:
            friends.remove(friend)
            del friend
        hit_friend = pygame.sprite.spritecollideany(P1, friends)
        if hit_friend:
            friends.remove(hit_friend) # Remove collected sprite from sprite group
            del hit_friend
            score += 1
        
    # Show game over when player collides with enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        bg = pygame.image.load("images/bg2.png")
        collided = True
        
    P1.draw(screen)
    E1.draw(screen)
    
    # Display score
    font = pygame.font.Font(None, 24)
    scoretext = font.render('Score: '+str(score), True, (0,0,0))
    textRect = scoretext.get_rect()
    textRect.topleft=[20,10]
    screen.blit(scoretext, textRect)
    
    pygame.display.update()
    FramePerSec.tick(FPS) 