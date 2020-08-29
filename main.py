import pygame
import numpy as np

class Car:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.height = 50
        self.width = 50

    def move(self, keys):
        dx = 0
        dy = 0
        dx += -5 * keys[pygame.K_LEFT]
        dx += 5 * keys[pygame.K_RIGHT]
        dy += -5 * keys[pygame.K_UP]
        dy += 5 * keys[pygame.K_DOWN]
        self.x += dx
        self.y += dy

class GameWorld:
    def __init__(self):
        self.win = pygame.display.set_mode((800, 800))
        self.car_arr = []

    def render(self):
        self.win.fill((0, 0, 0))
        for car in self.car_arr:
            pygame.draw.rect(self.win, (255, 0, 0),
                             (car.x, car.y, car.height, car.width))
            pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    game_world = GameWorld()
    car0 = Car()
    game_world.car_arr.append(car0)

    while True:
        # Basic setup for quitting
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()

        # Main flow
        pygame.time.delay(10)
        keys = pygame.key.get_pressed() # should return tuple of all keys pressed boolean
        if sum(keys) != 0:
            car0.move(keys)
        game_world.render()