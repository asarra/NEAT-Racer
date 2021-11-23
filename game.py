import pygame, math


class Car:
    def __init__(self):
        self.surface = self.rotate_surface = pygame.transform.scale(pygame.image.load("assets/car.png"), (50, 50))
        self.pos = [750, 730]
        self.angle, self.distance = 0, 0
        self.speed = 10
        self.center = [self.pos[0] + 25, self.pos[1] + 25]
        self.radars, self.radars_for_draw = [], []
        self.is_alive = True

    def draw(self, screen):
        screen.blit(self.rotate_surface, self.pos)
        for r in self.radars:
            pos, _ = r
            pygame.draw.line(screen, (0, 255, 255), self.center, pos, 2)

    def check_collision(self, map):
        for p in self.four_points:
            if map.get_at((int(p[0]), int(p[1]))) == (0, 0, 0, 255):
                self.is_alive = False
                break

    def calc_pos(self, index, degree, len, center=True):
        if center:
            if index == 0:
                return int(self.center[index] + math.cos(math.radians(360 - (self.angle + degree))) * len)
            else:
                return int(self.center[index] + math.sin(math.radians(360 - (self.angle + degree))) * len)
        else:
            if index == 0:
                return math.cos(math.radians(360 - self.angle)) * len
            else:
                return math.sin(math.radians(360 - self.angle)) * len

    def calc_radar(self, degree, map):
        len = 0
        crashed = False
        while not crashed and len < 300:
            x = self.calc_pos(0, degree, len)
            y = self.calc_pos(1, degree, len)
            len += 1
            crashed = True if map.get_at((x, y)) == (0, 0, 0, 255) else False
        self.radars.append([(x, y), math.sqrt(((x-self.center[0])**2) + ((y-self.center[1])**2))])  # pos.xy, distance

    def update(self, map):
        self.rotate_surface = self.rot_center(self.surface, self.angle)
        self.distance += self.speed
        self.pos[0] += self.calc_pos(0, 0, self.speed, center=False)
        self.pos[1] += self.calc_pos(1, 0, self.speed, center=False)

        # calculate 4 collision points
        self.center = [int(self.pos[0]) + 25, int(self.pos[1]) + 25]
        left_top = [self.calc_pos(0, 30, self.speed), self.calc_pos(1, 30, self.speed)]
        right_top = [self.calc_pos(0, 150, self.speed), self.calc_pos(1, 150, self.speed)]
        left_bottom = [self.calc_pos(0, 210, self.speed), self.calc_pos(1, 210, self.speed)]
        right_bottom = [self.calc_pos(0, 330, self.speed), self.calc_pos(1, 330, self.speed)]
        self.four_points = [left_top, right_top, left_bottom, right_bottom]
        self.check_collision(map)
        self.radars.clear()
        for d in range(-90, 120, 45):
            self.calc_radar(d, map)

    def get_inputs(self):
        return [int(x[1]) for x in self.radars] if self.radars else [0, 0, 0, 0, 0]

    def get_reward(self):
        return self.distance / 50.0

    def rot_center(self, image, angle):
        rot_image = pygame.transform.rotate(image, angle)
        orig_rect = image.get_rect()
        orig_rect.center = rot_image.get_rect().center
        return rot_image.subsurface(orig_rect).copy()
