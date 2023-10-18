class Settings:
    """A class to staore all setting for Alien Invasion"""

    def __init__(self):
        """Initialize the game setting """
        #screen setting
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        #ship setting 
        self.ship_speed = 1.5
        self.ship_limit =3 
        
        #Bullet setting 
        self.bullet_speed = 2.5
        self.bullet_width = 3 
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3
        
        #alien setting
        self.alien_speed =1.0
        self.fleet_drop_speed = 10
        
        
        
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Intitialize seting that change throughout the game"""
        self.ship_speed =1.5
        self.bullet_speed =2.5
        self.alien_speed = 1.0
        #fleet direction 1 represent right ; -1 represent left 
        self.fleet_direction = 1
    
    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scal