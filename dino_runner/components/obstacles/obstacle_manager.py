import pygame
import random
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.obstacle import Cactus, LargeCactus
from dino_runner.utils.constants import LARGE_CACTUS, BIRD, SMALL_CACTUS

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.hp = 3

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
            if not obstacle.collided:
                if game.player.dino_rect.colliderect(obstacle.rect):
                    obstacle.collided = True
                    self.hp -= 1
                    if self.hp <= 0:
                        pygame.time.delay(500)
                        game.playing = False
                    game.death_count += 1
                    self.obstacles.remove(obstacle) # remover o obstáculo colidido
                    break
            obstacle.update(game.game_speed, self.obstacles)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.collided = False
        self.obstacles.clear()
        self.hp = 3
