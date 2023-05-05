import pygame
import sys

from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.HP import Lifes
from dino_runner.components.clouds import Clouds
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import (
    BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH,
    TITLE, FPS, FONT_STYLE, MENU_WIDTH,
    MENU_HEIGHT, DEFAULT_TYPE
)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.executing = False
        self.end_game = False
        self.game_speed = 20
        self.speed = 2
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.half_screen_height = MENU_HEIGHT
        self.half_screen_width = MENU_WIDTH
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.lifes = Lifes(self.obstacle_manager)

        self.font = pygame.font.Font(FONT_STYLE, 22)

        self.player = Dinosaur()

        self.clouds = {
            'cloud1': Clouds((SCREEN_WIDTH + 300), 200),
            'cloud2': Clouds((SCREEN_WIDTH + 600), 240),
            'cloud3': Clouds((SCREEN_WIDTH + 900), 180),
            'cloud4': Clouds((SCREEN_WIDTH + 1200), 50)
        }

        

        self.score = 0
        self.death_count = 0

    def execute(self):
        self.executing = True

        while self.executing:
            if not self.playing and not self.end_game:
                self.show_menu()
            elif self.end_game and not self.playing:
                self.game_over()

        pygame.display.quit()
        pygame.quit()

    def reset_game(self):
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        print(self.death_count)

        while self.playing: 
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.executing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)

        for cloud in self.clouds.values():
            cloud.update()

        self.obstacle_manager.update(self, self.screen)
        self.power_up_manager.update(self)
        
        self.lifes.update()

        self.update_score()

    def update_score(self):
        if not self.playing:
            if self.end_game:
                self.game_over()
            else:
                self.death_count += 1
                if self.death_count >= 3:
                    self.end_game = True
        else:
            self.score += 1

            if self.score % 100 == 0:
                self.game_speed += 2
                self.speed += 0.25

                for cloud in self.clouds.values():
                    cloud.speed = self.speed

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((86, 193, 216))

        for cloud in self.clouds.values():
            cloud.draw(self.screen)

        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)

        self.draw_score()
        self.lifes.draw(self.screen)
        pygame.display.flip()

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time_up - pygame.time.get_ticks())/1000,2)

            if time_to_show >= 0:
                font = pygame.font.Font(FONT_STYLE, 22)
                text = font.render(f"{time_to_show}", True, (255,0,0))

                text_rect = text.get_rect()
                text_rect.x = 500
                text_rect.y = 50

                self.screen.blit(text, text_rect)

            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def draw_score(self):
        text = self.font.render(f'Score: {self.score}', True, (0,0,0))

        text_rect = text.get_rect()
        text_rect.center = (1000, 50)

        self.screen.blit(text, text_rect)

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def show_menu(self):
        self.screen.fill((255,255,255))

        if self.death_count > 0 and self.death_count < 3:
            text = self.font.render('Press "c" to continue', True, (0,0,0))
            text_rect = text.get_rect()
            text_rect.center = (self.half_screen_width, self.half_screen_height + 100)
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            self.reset_game()
            self.continue_events()

        else:
            text = self.font.render('Press any key to start', True, (0,0,0))
            text_rect = text.get_rect()
            text_rect.center = (self.half_screen_width, self.half_screen_height)
            self.screen.blit(text, text_rect)

            text = self.font.render(f'Death: {self.death_count}', True, (255,0,0))
            text_rect.center = (150, 50)
            self.screen.blit(text, text_rect)

            pygame.display.flip()

            self.handle_events_on_menu()


    def game_over(self):
        text = self.font.render('Game Over', True, (0,0,0))

        text_rect = text.get_rect()
        text_rect.center = (self.half_screen_width, self.half_screen_height)
        self.screen.blit(text, text_rect)

        text = self.font.render('Press space to quit', True, (0,0,0))
        text_rect.center = (self.half_screen_width, self.half_screen_height + 50)
        self.screen.blit(text, text_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pygame.quit()
                    sys.exit()

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.executing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def continue_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.executing = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                self.run()
