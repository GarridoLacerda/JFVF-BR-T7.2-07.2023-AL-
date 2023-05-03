import random
import pygame

from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.obstacle import Cactus, LargeCactus
from dino_runner.utils.constants import LARGE_CACTUS, BIRD, SMALL_CACTUS

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        
        if len(self.obstacles) == 0:
            obstacle_type = random.choice([Cactus, LargeCactus, Bird])
            if obstacle_type == Cactus:
                image = SMALL_CACTUS[random.randint(0, 2)]
            elif obstacle_type == LargeCactus:
                image = LARGE_CACTUS[random.randint(0, 2)]
            else:
                image = BIRD
            self.obstacles.append(obstacle_type(image))
        
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False
                break           
    
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
