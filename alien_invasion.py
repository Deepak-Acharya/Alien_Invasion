import sys

from time import sleep

import pygame

from seting import Settings

from game_stats import GameStats

from scoreboard import Scoreboard

from button import Button

from ship import Ship

from bullet import Bullet

from alien import Alien



class AlienInvasion:
    """Overall class to manage game assets and behaviour."""
    
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        
       
        self.clock = pygame.time.Clock()
        
        #set the background color
        self.seting = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.seting.screen_width = self.screen.get_rect().width
        self.seting.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.seting.screen_width ,self.seting.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        # create an instance to store game statistics 
        self.stats = GameStats(self)
        
        
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        # start alien invasion in an active state
        #self.game_active = True
        #self.play_button = Button(self,"Play")
        self.game_active = False
        self.play_button = Button(self,"play")
    
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)
            
    def _check_events(self):
            #watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)   
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                    #move the ship to the right
                    self.ship.rect.x += 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
    def _check_keydown_events(self,event):
        """responds to keypreses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False  
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.seting.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        self.bullets.update()
            
            # get rid of bullets that have disappered.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        
    
    def _check_bullet_alien_collisions(self):
        """respond to bullet alien collisions"""
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens ,True ,True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.seting.increase_speed()
            
    def _update_screen(self):
            #redraw the screen during each pass through loop.
            self.screen.fill(self.seting.bg_color)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blitime()
            self.aliens.draw(self.screen)
            
           
            
            #draw the play button if the game is inactive
            if not self.game_active:
                self.play_button.draw_button()
            
            #Make the most recently drawn screen visible 
            pygame.display.flip()
            self.clock.tick(60)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        #make an alien
        alien = Alien(self)
        alien_width , alien_height = alien.rect.size
        
        current_x,current_y = alien_width , alien_height
        while current_y < (self.seting.screen_height - 3*alien_height):
            while current_x < (self.seting.screen_width - 2*alien_width):
                self._create_alien(current_x , current_y)
                current_x += 2*alien_width
            #finished a row ; reset x value  and incremante y value
            current_x = alien_width
            current_y += 2*alien_height
        self.aliens.add(alien)
    
    def _create_alien(self,x_position,y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    
    def _update_aliens(self):
        """update the position of all aliens inthe fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        
        # look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
            print("Ship Hit!!!")
        
        #look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()
            
        
    def _check_fleet_edges(self):
        """Respond appropriatley if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleets direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.seting.fleet_drop_speed
        self.seting.fleet_direction *= -1
        
    def _ship_hit(self):
        """respond to the ship being hit y an alien"""
        if self.stats.ship_left > 0 :
            #dectrement ship left
            self.stats.ship_left -= 1
            sleep(0.5)
        else:
            self.game_active =False
            pygame.mouse.set_visible(True)
        
        #get rid of remainig bullets and aliens
        self.bullets.empty()
        self.aliens.empty()
        
        #create new fleet and center the ship 
        self._create_fleet()
        self.ship.center_ship()
        
        #pause 
        sleep(0.5)
        
    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.seting.screen_height:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break
    
    def _check_play_button(self,mouse_pos):
        """Start a new game when the player clicks Play"""
        #deactiving play button
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.seting.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.game_active = True
            #get rid of remaining bullet and aliens
            self.bullets.empty()
            self.aliens.empty()
            
            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            #hide the mouse cursor
            pygame.mouse.set_visible(False)
if __name__ == '__main__':
    #make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()