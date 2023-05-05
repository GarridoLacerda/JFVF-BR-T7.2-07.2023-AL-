import random
from dino_runner.utils.constants import CLOUD, SCREEN_WIDTH

class Clouds:
    def __init__(self, x, y):
        self.image = CLOUD
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2

    def update(self):
        if self.rect.topright[0] < 0:

            self.rect.x = (SCREEN_WIDTH + 200) - random.randrange(30, 300, 90)
            self.rect.y = random.randrange(70, 250, 80)
        else:
            self.rect.x -= self.speed

    def draw(self, screen):
        self.update()
        screen.blit(self.image, self.rect)
