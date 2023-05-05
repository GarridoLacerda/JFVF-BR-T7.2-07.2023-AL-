import random
import pygame

from dino_runner.components.power_ups.shield import Shield

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.to_appear = 0

    def update(self, game):
        player = game.player

        if len(self.power_ups) == 0 and self.to_appear == game.score:
            self.power_ups.append(Shield())
            self.to_appear += random.randint(200, 300)

        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)

            if player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                player.has_power_up = True
                player.type = power_up.type
                player.power_up_time_up = power_up.start_time + (power_up.duration * 1000)

                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups.clear()
        self.to_appear = random.randint(200,300)
