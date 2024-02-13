import pygame, sys
import random
from pygame.locals import *

class Game:
    def __init__(self):
        #constants
        self.WIDTH = 700
        self.HEIGHT = 500
        self.FPS = 60

        #setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong Game")
        self.clock = pygame.time.Clock()

        #sprite setup

        self.bat1 = pygame.Rect(0, 0, 20, 100)
        self.bat2 = pygame.Rect(0, 0, 20, 100)
        self.bat1.center = (20, self.HEIGHT//2)
        self.bat2.center = (self.WIDTH - 20, self.HEIGHT//2)

        self.ball = pygame.Rect(0, 0, 20, 20)
        self.ball.center = (self.WIDTH//2, self.HEIGHT//2)

        #font setup
        self.font = pygame.font.SysFont(None, 55)

        #sound setup

        #variables
        self.active = False
        self.bat_speed = 8
        self.ball_speed_y = 4
        self.ball_speed_x = 6
        self.ball_direction_x = random.choice([1, -1])
        self.ball_direction_y = random.choice([1, -1])
        self.p1_score = 0
        self.p2_score = 0
        self.collision_counter = 0

    def update(self, keys):
        # collision detection

        #bat1
        if self.bat1.y <= 0:
            self.bat1.y = 0
        elif self.bat1.y >= self.HEIGHT - self.bat1.h:
            self.bat1.y = self.HEIGHT - self.bat1.h

        #bat2
        if self.bat2.y <= 0:
            self.bat2.y = 0
        elif self.bat2.y >= self.HEIGHT - self.bat2.h:
            self.bat2.y = self.HEIGHT - self.bat2.h
        
        #ball
        if self.ball.colliderect(self.bat1) or self.ball.colliderect(self.bat2):
            self.ball_direction_x *= -1
            self.collision_counter += 1 
            if self.collision_counter % 2 == 0:
                self.ball_speed_x += 1
        
        if self.ball.y <= 0 or self.ball.midbottom[1] >= self.HEIGHT:
            self.ball_direction_y *= -1
        if self.ball.midleft[0] <= 0:
            self.p2_score += 1
            self.restart()
        
        if self.ball.x >= self.WIDTH:
            self.p1_score += 1
            self.restart()
        
        #ball movement
        self.ball = self.ball.move(self.ball_speed_x*self.ball_direction_x, self.ball_speed_y*self.ball_direction_y)

        #player 1 movement
        if keys[K_w]:
            self.bat1 = self.bat1.move(0, -self.bat_speed)
        elif keys[K_s]:
            self.bat1 = self.bat1.move(0, self.bat_speed)
        
        #player 2 movement
        if keys[K_UP]:
            self.bat2 = self.bat2.move(0, -self.bat_speed)
        elif keys[K_DOWN]:
            self.bat2 = self.bat2.move(0, self.bat_speed)


    def draw(self):
        self.screen.fill((0, 0, 0))

        if not self.active:
            self.draw_text("Press any button to begin", (self.WIDTH//2, self.HEIGHT//3))
        
        self.draw_text(f"{self.p1_score}", (100, 40))
        self.draw_text(f"{self.p2_score}", (self.WIDTH - 100, 40))

        pygame.draw.rect(self.screen, (255, 255, 255), self.bat1)
        pygame.draw.rect(self.screen, (255, 255, 255), self.bat2)
        pygame.draw.rect(self.screen, (255, 255, 255), self.ball)

    def draw_text(self, text, pos):
            font_label = self.font.render(text, 1, (255,255,255))
            font_rect = font_label.get_rect(center = (pos))
            self.screen.blit(font_label, font_rect)
    
    def restart(self):
        self.ball.center = (self.WIDTH//2, self.HEIGHT//2)
        self.ball_direction_x = random.choice([1, -1])
        self.ball_direction_y = random.choice([1, -1])
        self.ball_speed_x = 6
        self.ball_speed_y = 4

    def run(self):
        #main game loop
        running = True
        while running:
            #event queue
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    self.active = True
                    
            keys = pygame.key.get_pressed()
            
            #update sprites
            if self.active:
                self.update(keys)
            
            #draw sprites
            self.draw()

            #update display            
            pygame.display.flip()
            self.clock.tick(self.FPS)           

if __name__ == "__main__":
    game = Game()
    game.run()