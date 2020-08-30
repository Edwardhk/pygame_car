import pygame
import math
import numpy as np

# Display & color
BG = (40, 42, 54)
FG = (248, 248, 242)
PINK = (255, 121, 198)
GREEN = (80, 250, 123)
SCREEN_RESOLUTION = (1200, 800)

# Car config
MAX_SPEED = 30
ROTATE_ANGLE = 15
INIT_POSITION = (200, 650)


class Car:
    def __init__(self):
        self.speed = 1
        self.angle = 0
        self.height = 50
        self.width = 30
        self.off = pygame.math.Vector2(INIT_POSITION)
        self.pos = pygame.math.Vector2(self.height / 2, 0)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.pos.rotate_ip(-ROTATE_ANGLE)
        elif keys[pygame.K_RIGHT]:
            self.pos.rotate_ip(ROTATE_ANGLE)
        if keys[pygame.K_UP]:
            self.speed = MAX_SPEED if self.speed + 3 > MAX_SPEED else self.speed + 2
        elif keys[pygame.K_DOWN]:
            self.speed = 0 if self.speed <= 10 else self.speed - 10

        # Reset 
        if keys[pygame.K_r]:
            self.speed = 1
            self.angle = 0
            self.off = pygame.math.Vector2(INIT_POSITION)
            self.pos = pygame.math.Vector2(self.height / 2, 0)


class GameWorld:
    def __init__(self):
        self.win = pygame.display.set_mode(SCREEN_RESOLUTION)
        self.car_arr = []

    def render(self):
        self.win.fill(BG)
        for car in self.car_arr:
            print(f"Current speed: {car.speed}")
            car.speed += 0.01
            car_head = car.off + car.pos
            pygame.draw.line(self.win, PINK, car.off, car_head, 10)
            car.off += car.pos.normalize() * car.speed
            pygame.draw.line(self.win, GREEN, car_head,
                             car.off + car.pos.rotate(30) * 3, 1)
            pygame.draw.line(self.win, GREEN, car_head,
                             car.off + car.pos.rotate(-30) * 3, 1)
            # pygame.draw.circle(self.win, GREEN, (int(dest[0]), int(dest[1])), 4)
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
        pygame.time.delay(50)
        keys = pygame.key.get_pressed()  # should return tuple of all keys pressed boolean
        if sum(keys) != 0:
            car0.move(keys)
        game_world.render()
