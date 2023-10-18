class GameStats:
    """Track Statistics for alien invasion"""
    
    def __init__(self,ai_game):
        """Initialize statistics """
        self.seting = ai_game.seting
        self.reset_stats()
    
    def reset_stats(self):
        """initialize statistic taht can change during the game"""
        self.ship_left = self.seting.ship_limit
        self.score =0