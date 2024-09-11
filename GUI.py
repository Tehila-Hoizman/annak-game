import numpy as np
from configuration import Configuration
from constants import *
import cv2 as cv


class Gui:
    def __init__(self, world):
        self.world = world
        height, width = len(self.world.tiles_matrix) * Configuration.get_tile_size()[1] * CELL_HEIGHT, len(
            self.world.tiles_matrix[0]) * \
                        Configuration.get_tile_size()[0] * CELL_WIDTH
        self.bkg = np.zeros((height, width, 3), np.uint8)
        self.draw_world_map()

    def draw_world_map(self):
        for inx_row, row in enumerate(self.world.tiles_matrix):
            for inx_col, col in enumerate(row):
                tile = self.world.world_map[inx_row][inx_col]
                self.draw_tile(tile.type, tile.coordinate)
        self.draw_grid_lines()

    def draw_tile(self, type, coordinate):
        img = cv.imread(TILE_URL + Configuration.get_tiles_images()[type])
        img = cv.resize(img,
                        (CELL_HEIGHT * Configuration.get_tile_size()[1], CELL_WIDTH * Configuration.get_tile_size()[0]))
        height, width, _ = img.shape
        x, y = coordinate[0] * CELL_WIDTH, coordinate[1] * CELL_HEIGHT
        self.bkg[x:x + width, y:y + height] = img

    def draw_object(self, object_type, type, coordinate):
        size = Configuration.get_sizes()[type]
        img = ''
        if object_type == TRANSPORTATION:
            img = cv.imread(TRANSPORTATION_URL + Configuration.get_objects_images()[type])
        elif object_type == INFRASTRUCTURE:
            img = cv.imread(INFRASTUCTURE_URL + Configuration.get_objects_images()[type])
        elif object_type == PEOPLE:
            img = cv.imread(PEOPLE_URL + Configuration.get_objects_images()[type])
        img = cv.resize(img, (CELL_HEIGHT * size[1], CELL_WIDTH * size[0]))
        height, width, _ = img.shape
        x, y = coordinate[0] * CELL_WIDTH, coordinate[1] * CELL_HEIGHT
        self.bkg[x:x + height, y:y + width] = img

    def draw(self):

        for car in self.world.objects[TRANSPORTATION][CAR].values():
            self.draw_object(TRANSPORTATION, CAR, car.coordinate)

        for truck in self.world.objects[TRANSPORTATION][TRUCK].values():
            self.draw_object(TRANSPORTATION, TRUCK, truck.coordinate)

        for helicopter in self.world.objects[TRANSPORTATION][HELICOPTER].values():
            self.draw_object(TRANSPORTATION, HELICOPTER, helicopter.coordinate)

        for people in self.world.objects[PEOPLE].values():
            self.draw_object(PEOPLE, PEOPLE, people.coordinate)

        for city in self.world.objects[INFRASTRUCTURE][CITY].values():
            self.draw_object(INFRASTRUCTURE, CITY, city.coordinate)

        for village in self.world.objects[INFRASTRUCTURE][VILLAGE].values():
            self.draw_object(INFRASTRUCTURE, VILLAGE, village.coordinate)

        for road in self.world.objects[INFRASTRUCTURE][ROAD].values():
            self.draw_object(INFRASTRUCTURE, ROAD, road.coordinate)

        self.draw_grid_lines()

    def draw_grid_lines(self):
        for inx_row, row in enumerate(self.world.tiles_matrix):
            self.bkg = cv.line(self.bkg, (0, Configuration.get_tile_size()[1] * inx_row * CELL_HEIGHT), (
            len(self.world.tiles_matrix[0]) * Configuration.get_tile_size()[0] * CELL_WIDTH,
            Configuration.get_tile_size()[0] * CELL_WIDTH * inx_row), (255, 0, 0), 2)

        for inx_col, col in enumerate(self.world.tiles_matrix[0]):
            self.bkg = cv.line(self.bkg, (Configuration.get_tile_size()[0] * inx_col * CELL_WIDTH, 0), (
            Configuration.get_tile_size()[1] * CELL_HEIGHT * inx_col,
            len(self.world.tiles_matrix) * Configuration.get_tile_size()[1] * CELL_HEIGHT), (255, 0, 0), 2)

        for inx_row, row in enumerate(self.world.tiles_matrix):
            for inx_col, col in enumerate(row):
                tile = self.world.world_map[inx_row][inx_col]
                for inx, r in enumerate(tile.tile_map):
                    self.bkg = cv.line(self.bkg,
                                       (tile.tile_map[inx][0].coordinate[1] * CELL_HEIGHT, inx * CELL_HEIGHT),
                                       (Configuration.get_tile_size()[1]* CELL_WIDTH, CELL_WIDTH * inx), (0, 0, 0), 1)

                for inx, c in enumerate(tile.tile_map[0]):
                    self.bkg = cv.line(self.bkg, (inx * CELL_WIDTH, tile.tile_map[inx][1].coordinate[0] * CELL_WIDTH),
                                       (CELL_HEIGHT * inx, Configuration.get_tile_size()[0] * CELL_HEIGHT),
                                       (0, 0, 0), 1)
