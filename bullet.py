import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bulletsfirend from the ship """

    def __init__(self, ai_game):
        """Create a bullet object at the ships current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.seting = ai_game.seting
        self.color = self.seting.bullet_color
        
        # Create a bullet rect at (0,0) and then set the current poition 
        self.rect = pygame.Rect(0,0,self.seting.bullet_width, self.seting.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        #store the bullets position as a float
        self.y = float(self.rect.y)
    
    def update(self):
        """move the bullet up the screen"""
        #update the exact position of the bullet
        self.y -= self.seting.bullet_speed
        
        #update the rect position
        self.rect.y  = self.y
    
    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen,self.color,self.rect)