import pygame

class Ship:
    """A class to manage the ship"""

    def __init__(self,ai_game):
        """Initialize the ship and set its starting position"""

        self.screen = ai_game.screen
        self.seting = ai_game.seting
        self.screen_rect = ai_game.screen.get_rect()
        
        #load the ship images and get its rect.
        
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        
        #start each new ship at the bottom center of screen

        self.rect.midbottom = self.screen_rect.midbottom
        
        #store  a float for the ships exat horizontal position
        self.x = float(self.rect.x)
        
        #movement flag; start with a ship that not moving
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Update the ships position based on movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
    
            self.x += self.seting.ship_speed
            self.rect.x += 1
        if self.moving_left and self.rect.left > 0:
            self.x -= self.seting.ship_speed
            self.rect.x -= 1
        
        #update rect obect from self.x
        self.rect.x = self.x
    
    def blitime(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image,self.rect)
        
    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)