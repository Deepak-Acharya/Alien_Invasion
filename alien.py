import pygame

from pygame.sprite import Sprite

class Alien(Sprite):
    """A class represent a single alien in the fleet."""
    def __init__(self,ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.seting = ai_game.seting
        
        #load the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        #start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #store the alien exact horizontal position
        self.x = float(self.rect.x)
        
    def check_edges(self):
        """return true if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <=0)
    def update(self):
        """move the alien to the right"""
        self.x += self.seting.alien_speed*self.seting.fleet_direction
        self.rect.x =self.x