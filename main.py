import pygame
import math
import numpy as np

RED = (255, 0, 0)
ANGLE = np.radians(10)
SCREEN_RESOLUTION = (1200, 800)

class Car:
    def __init__(self):
        self.angle = 0
        self.height = 50
        self.width = 30
        self.off = pygame.math.Vector2(400, 650)
        self.pos = pygame.math.Vector2(self.height / 2, 0)

    def move(self, keys):
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT]:
            self.rotate('L')
        elif keys[pygame.K_RIGHT]:
            self.rotate('R')
        dy += -5 * keys[pygame.K_UP]
        dy += 5 * keys[pygame.K_DOWN]
        self.off[0] += dx
        self.off[1] += dy

    def rotate(self, dir):
        if dir == 'L':
            self.angle += np.degrees(ANGLE)
            if self.angle >= 360:
                self.angle %= 360
            rx = np.cos(ANGLE) * self.pos[0] + np.sin(ANGLE) * self.pos[1]
            ry = - np.sin(ANGLE) * self.pos[0] + np.cos(ANGLE) * self.pos[1]
        elif dir == 'R':
            self.angle -= np.degrees(ANGLE)
            if self.angle < 0:
                self.angle += 360
            rx = np.cos(ANGLE) * self.pos[0] - np.sin(ANGLE) * self.pos[1]
            ry = np.sin(ANGLE) * self.pos[0] + np.cos(ANGLE) * self.pos[1]
        
        self.pos = pygame.math.Vector2(rx, ry)
        print(self.angle)


class GameWorld:
    def __init__(self):
        self.win = pygame.display.set_mode(SCREEN_RESOLUTION)
        self.car_arr = []

    def render(self):
        self.win.fill((0, 0, 0))
        for car in self.car_arr:
            pygame.draw.line(self.win, RED, car.off, car.off + car.pos)
            pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    game_world = GameWorld()
    car0 = Car()
    game_world.car_arr.append(car0)

    while True:
        # Basic setup for quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Main flow
        pygame.time.delay(10)
        keys = pygame.key.get_pressed()  # should return tuple of all keys pressed boolean
        if sum(keys) != 0:
            car0.move(keys)
        game_world.render()
