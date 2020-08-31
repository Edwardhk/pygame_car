import pygame
import pygame.gfxdraw
import numpy as np

# Display & color
BG = (40, 42, 54)
FG = (248, 248, 242)
GREY = (68, 71, 90)
PINK = (255, 121, 198)
GREEN = (80, 250, 123)
PURPLE = (189, 147, 249)
WHITE = (248, 248, 242)
SCREEN_RESOLUTION = (1200, 800)

# Car config
CAR_HEIGHT = 20
CAR_WIDTH = 10
MAX_SPEED = 10
ROTATE_ANGLE = 8
INIT_POSITION = (200, 650)
IN_ANGLE = np.rad2deg(np.arctan(CAR_WIDTH / CAR_HEIGHT))


class Car:
    def __init__(self):
        self.speed = 1
        self.angle = 0
        self.height = CAR_HEIGHT
        self.width = CAR_WIDTH
        self.off = pygame.math.Vector2(INIT_POSITION)
        self.vel = pygame.math.Vector2(self.height / 2, 0)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.vel.rotate_ip(-ROTATE_ANGLE)
        elif keys[pygame.K_RIGHT]:
            self.vel.rotate_ip(ROTATE_ANGLE)
        if keys[pygame.K_UP]:
            self.speed = MAX_SPEED if self.speed + 1 > MAX_SPEED else self.speed + 1
        elif keys[pygame.K_DOWN]:
            self.speed = 0 if self.speed <= 3 else self.speed - 3

        # Reset
        if keys[pygame.K_r]:
            self.speed = 1
            self.angle = 0
            self.off = pygame.math.Vector2(INIT_POSITION)
            self.vel = pygame.math.Vector2(self.height / 2, 0)

    def get_polygon_edges(self):
        car_edge_angle = [IN_ANGLE, 180 - IN_ANGLE, IN_ANGLE - 180, -IN_ANGLE]
        car_edge_point = []
        for edge_angle in car_edge_angle:
            car_edge_point.append(self.off + self.vel.rotate(edge_angle))
        return car_edge_point


class GameWorld:
    def __init__(self):
        self.win = pygame.display.set_mode(SCREEN_RESOLUTION)
        self.car_arr = []

    def render(self):
        self.win.fill(BG)
        for car in self.car_arr:
            if car.speed < MAX_SPEED:
                car.speed += 0.001
            edges_xy = car.get_polygon_edges()

            # Car wheel rendering
            for edge in edges_xy:
                pygame.draw.circle(
                    self.win, PINK, (int(edge[0]), int(edge[1])), 2)

            # Car body rendering
            car.off += car.vel.normalize() * car.speed
            pygame.draw.polygon(self.win, PURPLE, edges_xy)

            # Simulate the angle of sensor
            pygame.draw.line(self.win, GREEN, car.off,
                             car.off + car.vel * 2, 2)
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
