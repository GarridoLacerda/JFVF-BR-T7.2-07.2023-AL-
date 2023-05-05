from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.constants import HEART, HEART2, HEART3

class Lifes:
    def __init__(self, obstacle_manager):
        self.obstacle_manager = obstacle_manager
        if self.obstacle_manager.hp == 3:
            self.image = HEART3
        elif self.obstacle_manager.hp == 2:
            self.image = HEART2
        else:
            self.image = HEART
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 50

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.obstacle_manager.hp == 3:
            self.image = HEART3
        elif self.obstacle_manager.hp == 2:
            self.image = HEART2
        else:
            self.image = HEART
