from dino_runner.utils.constants import SCREEN_WIDTH, OBSTACLE_Y_POS, LARGE_OBSTACLE_Y_POS

class Obstacle:
    def __init__(self, image):
        if isinstance(image, list):
            self.image = image[0]
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = OBSTACLE_Y_POS

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        
        if self.rect.x < -self.rect.width:
            obstacles.pop()
         
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Cactus(Obstacle):
    def __init__(self, image):
        super().__init__(image)

class LargeCactus(Obstacle):
    def __init__(self, image):
        super().__init__(image)
        self.rect.y = LARGE_OBSTACLE_Y_POS



