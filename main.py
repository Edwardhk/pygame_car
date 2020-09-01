import pygame
import numpy as np

# Display & color
BG = (32, 34, 43)
FG = (248, 248, 242)
BLACK = (98, 114, 164)
GREY = (68, 71, 90)
PINK = (255, 121, 198)
GREEN = (80, 250, 123)
PURPLE = (189, 147, 249)
WHITE = (248, 248, 242)
SCREEN_RESOLUTION = (1400, 800)

# Car config
INIT_POSITION = (200, 650)
CAR_HEIGHT = 20
CAR_WIDTH = 10

ACCELERATION = 0.3
BRAKE = 0.5
INIT_SPEED = 1
MAX_SPEED = 10

ROTATE_ANGLE = 5
IN_ANGLE = np.rad2deg(np.arctan(CAR_WIDTH / CAR_HEIGHT))


class Car:
    def __init__(self):
        self.speed = INIT_SPEED
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
            self.speed = MAX_SPEED if self.speed + \
                ACCELERATION > MAX_SPEED else self.speed + ACCELERATION
        elif keys[pygame.K_DOWN]:
            self.speed = 0 if self.speed <= BRAKE else self.speed - BRAKE

        # Reset
        if keys[pygame.K_r]:
            self.speed = INIT_SPEED
            self.off = pygame.math.Vector2(INIT_POSITION)
            self.vel = pygame.math.Vector2(self.height / 2, 0)

    def get_polygon_edges(self):
        car_edge_angle = [IN_ANGLE, 180 - IN_ANGLE, IN_ANGLE - 180, -IN_ANGLE]
        car_edge_point = []
        for edge_angle in car_edge_angle:
            car_edge_point.append(self.off + self.vel.rotate(edge_angle))
        return car_edge_point
    
    def render_car(self, win):
        edges_xy = self.get_polygon_edges()

        # Car wheel rendering
        # for edge in edges_xy:
        #     pygame.draw.circle(
        #         win, GREEN, (int(edge[0]), int(edge[1])), 3)

        # Car body rendering
        pygame.draw.polygon(win, BLACK, edges_xy)

        # Car sensor rendering
        pygame.draw.line(win, PINK, self.off,
                            self.off + self.vel * 2, 2)
        pygame.draw.line(win, PINK, self.off,
                            self.off + self.vel.rotate(62) * 4, 1)
        pygame.draw.line(win, PINK, self.off,
                            self.off + self.vel.rotate(-62) * 4, 1)


class GameWorld:
    def __init__(self):
        self.win = pygame.display.set_mode(SCREEN_RESOLUTION)
        self.car_arr = []

    def render(self):
        self.win.fill(BG)
        for car in self.car_arr:
            if car.speed < MAX_SPEED and car.speed != 0:
                car.speed += 0.001
            car.off += car.vel.normalize() * car.speed
            car.render_car(self.win)
            pygame.display.update()

    def show_info(self):
        FONT_SIZE = 18
        car_info = pygame.font.SysFont('Consolas', FONT_SIZE)
        for car in self.car_arr:
            self.win.blit(car_info.render(
                f'Car#0 speed: {car.speed:.3f}/{MAX_SPEED}', 1, GREEN), (0, 0))
            self.win.blit(car_info.render(
                f'Car#0 velocity:  {car.vel}', 1, GREEN), (0, FONT_SIZE))
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
        game_world.show_info()
