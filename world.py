from tile import Tile
from infrastructure import Infrastructure
from transportation import Transportation
from configuration import Configuration
from people import People
import numpy as np
from constants import *


class World:
    def __init__(self, tiles_matrix):
        self.world_map: [] = []
        self.tiles_matrix = tiles_matrix
        self.tile_size = Configuration.get_tile_size()
        self.is_start = False
        self.resources = [0, 0, 0, 0]
        self.points = 0
        self.objects = {
            INFRASTRUCTURE: {
                CITY: {},
                VILLAGE: {},
                ROAD: {}
            },
            TRANSPORTATION: {
                CAR: {},
                TRUCK: {},
                HELICOPTER: {}
            },
            PEOPLE: {}
        }
        self.bkg = self.build_world_map()

    def build_world_map(self):
        for inx_row, row in enumerate(self.tiles_matrix):
            map_row = []
            for inx_col, col in enumerate(row):
                tile = Tile(col, [inx_row * self.tile_size[0], inx_col * self.tile_size[1]])
                map_row.append(tile)

            self.world_map.append(map_row)

    # O(1)
    def get_cell_by_world_coordinate(self, coordinate):
        tile = self.get_tile_by_world_coordinate(coordinate)
        x, y = coordinate
        col_tile = x % self.tile_size[1]
        row_tile = y % self.tile_size[0]
        return tile.tile_map[row_tile][col_tile]

    # O(1)
    def get_tile_by_world_coordinate(self, coordinate):
        x, y = coordinate
        col = x // self.tile_size[1]
        row = y // self.tile_size[0]
        return self.world_map[row][col]

    def select_category(self, coordinate):
        cell = self.get_cell_by_world_coordinate(coordinate)
        object_name, type, id = cell.get_category()
        if object_name == TILE:
            return self.get_tile_by_world_coordinate(coordinate)
        if object_name == PEOPLE:
            return self.objects[object_name][id]
        return self.objects[object_name][type][id]

    def get_object(self, object_type, sub_type, id):
        if object_type == PEOPLE:
            return self.objects[object_type][id]
        return self.objects[object_type][sub_type][id]

    def update_resources(self, resources):
        for inx, resource in enumerate(resources):
            self.resources[inx] += resource

    # _________________________________BUILDING_______________________________________
    def is_connect_to_road(self, coordinate, size, x_from, x_to, y_from, y_to):
        size_road = Configuration.get_road_size()

        # Check on each side of the infrastructure if it connects to any road with full overlap
        if y_from > 0:
            for index in range(x_from, x_to):
                cell = self.get_cell_by_world_coordinate([index, y_from - 1])
                if cell.infrastructure_type == ROAD:
                    road_start_coordinate = self.objects[INFRASTRUCTURE][ROAD][cell.infrastructure_id].coordinate
                    if road_start_coordinate[0] >= coordinate[0] and road_start_coordinate[0] + size_road[0] <= \
                            coordinate[0] + size[0]:
                        return True
        if y_to < len(self.world_map) * self.tile_size[1]:
            for index in range(x_from, x_to):
                cell = self.get_cell_by_world_coordinate([index, y_to + 1])
                if cell.infrastructure_type == ROAD:
                    road_start_coordinate = self.objects[INFRASTRUCTURE][ROAD][cell.infrastructure_id].coordinate
                    if road_start_coordinate[0] >= coordinate[0] and road_start_coordinate[0] + size_road[0] <= \
                            coordinate[0] + size[0]:
                        return True
        if x_from > 0:
            for index in range(y_from, y_to):
                cell = self.get_cell_by_world_coordinate([x_from - 1, index])
                if cell.infrastructure_type == ROAD:
                    road_start_coordinate = self.objects[INFRASTRUCTURE][ROAD][cell.infrastructure_id].coordinate
                    if road_start_coordinate[1] >= coordinate[1] and road_start_coordinate[1] + size_road[1] <= \
                            coordinate[1] + size[1]:
                        return True
        if x_to < len(self.world_map[0]) * self.tile_size[0]:
            for index in range(y_from, y_to):
                cell = self.get_cell_by_world_coordinate([x_to + 1, index])
                if cell.infrastructure_type == ROAD:
                    road_start_coordinate = self.objects[INFRASTRUCTURE][ROAD][cell.infrastructure_id].coordinate
                    if road_start_coordinate[1] >= coordinate[1] and road_start_coordinate[1] + size_road[1] <= \
                            coordinate[1] + size[1]:
                        return True
        return False

    def is_connect_to_infrastructure(self, coordinate, size, x_from, x_to, y_from, y_to):

        # Check on each side of the infrastructure if it connects to any infrastructure with full overlap
        if y_from > 0:
            for index in range(x_from, x_to):
                cell = self.get_cell_by_world_coordinate([index, y_from - 1])
                if cell.infrastructure_id != -1:
                    start_coordinate = self.objects[INFRASTRUCTURE][cell.infrastructure_type][
                        cell.infrastructure_id].coordinate
                    if start_coordinate[0] >= coordinate[0] and start_coordinate[0] + \
                            Configuration.get_sizes()[cell.infrastructure_type][0] >= \
                            coordinate[0] + size[0]:
                        return True
        if y_to < len(self.world_map) * self.tile_size[1]:
            for index in range(x_from, x_to):
                cell = self.get_cell_by_world_coordinate([index, y_to + 1])
                if cell.infrastructure_id != -1:
                    start_coordinate = self.objects[INFRASTRUCTURE][cell.infrastructure_type][
                        cell.infrastructure_id].coordinate
                    if start_coordinate[0] >= coordinate[0] and start_coordinate[0] + \
                            Configuration.get_sizes()[cell.infrastructure_type][0] >= \
                            coordinate[0] + size[0]:
                        return True
        if x_from > 0:
            for index in range(y_from, y_to):
                cell = self.get_cell_by_world_coordinate([x_from - 1, index])
                if cell.infrastructure_id != -1:
                    start_coordinate = self.objects[INFRASTRUCTURE][cell.infrastructure_type][
                        cell.infrastructure_id].coordinate
                    if start_coordinate[1] >= coordinate[1] and start_coordinate[1] + \
                            Configuration.get_sizes()[cell.infrastructure_type][1] >= coordinate[1] + size[1]:
                        return True
        if x_to < len(self.world_map[0]) * self.tile_size[0]:
            for index in range(y_from, y_to):
                cell = self.get_cell_by_world_coordinate([x_to + 1, index])
                if cell.infrastructure_id != -1:
                    start_coordinate = self.objects[INFRASTRUCTURE][cell.infrastructure_type][
                        cell.infrastructure_id].coordinate
                    if start_coordinate[1] >= coordinate[1] and start_coordinate[1] + \
                            Configuration.get_sizes()[cell.infrastructure_type][1] >= \
                            coordinate[1] + size[1]:
                        return True
        return False

    def is_valid_build(self, coordinate, type, size):
        x_from, y_from = coordinate
        x_to, y_to = coordinate[0] + size[0], coordinate[1] + size[1]

        tile_x_from, tile_x_to = x_from // self.tile_size[1], x_to // self.tile_size[1]
        if x_from % self.tile_size[1] != 0:
            tile_x_to += 1
        tile_y_from, tile_y_to = y_from // self.tile_size[0], y_to // self.tile_size[0]
        if y_from % self.tile_size[0] != 0:
            tile_y_to += 1
        if tile_y_from == tile_y_to:
            tile_y_to += 1
        if tile_x_from == tile_x_to:
            tile_x_to += 1
        # Checking that there are no deviation from the world's borders
        if tile_x_to > len(self.world_map[0]) or tile_y_to > len(self.world_map):
            return False

        # Checking if tile is Ground
        if type != PEOPLE:
            for row in range(tile_y_from, tile_y_to):
                for column in range(tile_x_from, tile_x_to):
                    if self.world_map[row][column].type_id != 1:
                        return False
        else:
            for row in range(tile_y_from, tile_y_to):
                for column in range(tile_x_from, tile_x_to):
                    if self.world_map[row][column].type_id == 2:
                        return False

        # Checking that all the cells are available
        for row in range(y_from, y_to):
            for column in range(x_from, x_to):
                cell = self.get_cell_by_world_coordinate(coordinate)
                if cell.people_id != -1 or cell.transportation_id != -1:
                    return False

                if type not in [TRUCK, CAR, HELICOPTER, PEOPLE] and cell.infrastructure_id != -1:
                    return False

        if type == ROAD:
            return self.is_connect_to_infrastructure(coordinate, size, x_from, x_to, y_from, y_to)

        if self.is_start and type not in [TRUCK, CAR, HELICOPTER, PEOPLE]:
            return self.is_connect_to_road(coordinate, size, x_from, x_to, y_from, y_to)

        return True

    def build_infrastructure(self, coordinate, type):
        size = Configuration.get_sizes()[type]
        if self.is_valid_build(coordinate, type, size):
            infrastructure = Infrastructure(coordinate, type)
            self.objects[INFRASTRUCTURE][type][infrastructure.id] = infrastructure
            self.add_object_to_cells(infrastructure)
            points = 0
            if type == CITY:
                points = 2
            if type == VILLAGE:
                points = 1
            if self.points + points > 100:
                self.points = 100
            else:
                self.points += points

    def manufacture_transportation(self, coordinate, type):
        size = Configuration.get_sizes()[type]
        if self.is_valid_build(coordinate, type, size):
            if not self.is_start or self.is_cost_valid(type):
                transportation = Transportation(coordinate, type)
                cost = Configuration.get_costs()[type]
                self.update_resources([(resource * -1) for resource in cost[:len(cost) - 1]])
                self.objects[TRANSPORTATION][type][Transportation.id] = transportation
                self.add_object_to_cells(transportation)

    def move(self, coordinate, object_type, id, type):
        object = self.get_object(object_type, type, id)
        size = Configuration.get_sizes()[type]
        if self.is_valid_build(coordinate, type, size):
            self.remove_object_from_cells(object)
            object.move(coordinate)
            self.add_object_to_cells(object)
            return True
        return False

    def remove_object_from_cells(self, object):
        size = Configuration.get_sizes()[object.type]
        coordinate = object.coordinate

        type_object = ''
        if isinstance(object, Infrastructure):
            type_object = INFRASTRUCTURE
        if isinstance(object, Transportation):
            type_object = TRANSPORTATION
        if isinstance(object, People):
            type_object = PEOPLE

        for row in range(coordinate[1], coordinate[1] + size[0]):
            for col in range(coordinate[0], coordinate[0] + size[1]):
                cell = self.get_cell_by_world_coordinate([col, row])
                cell.remove_object(type_object)

    def add_object_to_cells(self, object):
        size = Configuration.get_sizes()[object.type]
        coordinate = object.coordinate
        type_object = ''
        if isinstance(object, Infrastructure):
            type_object = INFRASTRUCTURE
        if isinstance(object, Transportation):
            type_object = TRANSPORTATION
        if isinstance(object, People):
            type_object = PEOPLE

        for row in range(coordinate[1], coordinate[1] + size[0]):
            for col in range(coordinate[0], coordinate[0] + size[1]):
                cell = self.get_cell_by_world_coordinate([col, row])
                cell.add_object(type_object, object.id, object.type)

    def is_cost_valid(self, type):
        cost = Configuration.get_costs()[type]
        for inx, resource in enumerate(self.resources):
            if cost[inx] > resource:
                return False

        return True

    def set_points(self, points):
        if points > 100:
            self.points = 100
        else:
            self.points = points
