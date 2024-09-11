from cell import Cell
from configuration import Configuration
from people import People
import cv2 as cv
from constants import *


class Tile:
    def __init__(self, tile_type_id, coordinate):
        self.type_id = tile_type_id
        self.coordinate = coordinate
        self.tile_map = []
        self.size = Configuration.get_tile_size()
        self.type = list(Configuration.get_tiles().keys())[list(Configuration.get_tiles().values()).index(self.type_id)]
        self.resource_amount = 0
        self.resource_type = ""
        self.amount_of_people = 0
        self.init_resource()
        self.build_tile_map()

    def init_resource(self):
        if self.type in Configuration.get_starting_resources():
            self.resource_amount = Configuration.get_starting_resources()[self.type]
            self.resource_type = Configuration.get_resource_types()[self.type_id - 3]

    def build_tile_map(self):
        for height in range(self.size[1]):
            row = []
            for width in range(self.size[0]):
                row.append(Cell([self.coordinate[0] + height, self.coordinate[1] + width]))
            self.tile_map.append(row)

    def get_cell_by_coordinate(self, coordinate):
        x, y = coordinate
        col_tile = x % self.size[1]
        row_tile = y % self.size[0]
        return self.tile_map[row_tile][col_tile]

    def update_resource(self, amount, resource_type):
        if self.resource_type == resource_type:
            self.resource_amount = amount

    def add_people(self, amount, coordinate):
        cell = self.get_cell_by_coordinate(coordinate)
        if cell.people_id == -1:
            people = People(coordinate)
            cell.people_id = people.id
            self.amount_of_people += 1
            return [people]
        return []

    def work(self, people):
        if self.type_id not in [1, 2]:
            index = Configuration.get_resource_types().index(self.resource_type)
            people.add_resource(index, self.resource_amount)
            self.resource_amount = 0

    def rain(self, speed):
        if self.type == 'Forest' or self.type == 'Field':
            self.resource_amount += 1

    def get_resources(self):
        selected_resource = [0] * 4
        if self.resource_type:
            selected_resource[Configuration.get_resource_types().index(self.resource_type)] = self.resource_amount
        return selected_resource

    def get_amount_of_people(self):
        return self.amount_of_people
