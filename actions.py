from cell import Cell
from tile import Tile
from people import People
from transportation import Transportation
from configuration import Configuration
from infrastructure import Infrastructure
from constants import *


class Actions:
    def __init__(self, world):
        self.world = world
        self.selected_cell: Cell = None
        self.selected_category = None

    def start_game(self):
        self.world.is_start = True

    # +Input
    # Belong to Resource command
    def update_resource(self, args):
        amount, resource_type, x, y = args
        x, y = self.format_coordinate([x, y])
        self.select_category([x, y])
        if isinstance(self.selected_category, Tile):
            self.selected_category.update_resource(int(amount), resource_type)
        else:
            index = Configuration.get_resource_types().index(resource_type)
            resources = self.selected_category.add_resource(index, int(amount))
            self.world.update_resources(resources)

    # Belong to Resources command
    def update_resources(self, args):
        r1, r2, r3, r4, x, y = args
        x, y = self.format_coordinate([x, y])
        self.select_category([x, y])
        if isinstance(self.selected_category,
                      Infrastructure) and self.selected_cell.infrastructure_type != ROAD or isinstance(
            self.selected_category, Transportation):
            # Road doesn't have resources
            resources = self.selected_category.set_resource([int(r) for r in [r1, r2, r3, r4]])
            self.world.update_resources(resources)

    def format_coordinate(self, coordinate):
        x, y = coordinate
        x = int(x) - 1
        y = int(y) - 1
        return [x, y]

    def select(self, coordinate):
        coordinate = self.format_coordinate(coordinate)
        self.select_category(coordinate)

    def select_category(self, coordinate):
        self.selected_cell = self.world.get_cell_by_world_coordinate(coordinate)
        self.selected_category = self.world.select_category(coordinate)

    def add_people(self, args):
        amount, x, y = args
        x, y = self.format_coordinate([x, y])
        self.select_category([x, y])
        people = self.selected_category.add_people(int(amount), [x, y])
        for p in people:
            self.world.objects[PEOPLE][p.id] = p

    def work(self, args):
        x, y = args
        if isinstance(self.selected_category, People) and self.move([int(x), int(y)]):
            x, y = self.format_coordinate([x, y])
            tile = self.world.get_tile_by_world_coordinate([x, y])
            tile.work(self.selected_category)

    def rain(self, speed):
        tile = self.world.get_tile_by_world_coordinate(self.selected_cell.coordinate)
        tile.rain(speed)

    def build(self, args):
        infrastructure_type, x, y = args
        x, y = self.format_coordinate([x, y])
        self.world.build_infrastructure([x, y], infrastructure_type)

    def manufacture(self, args):
        transportation_type, x, y = args
        x, y = self.format_coordinate([x, y])
        self.world.manufacture_transportation([x, y], transportation_type)

    def make_empty(self, coordinate):
        coordinate = self.format_coordinate(coordinate)
        cell = self.world.get_cell_by_world_coordinate(coordinate)
        if cell.infrastructure_id != -1 and cell.infrastructure_type != ROAD:
            infrastructure = self.world.objects[INFRASTRUCTURE][cell.infrastructure_type][cell.infrastructure_id]
            resources = infrastructure.make_empty()
            self.world.update_resources(resources)

    def take_resources(self, coordinate):
        coordinate = self.format_coordinate(coordinate)
        if isinstance(self.selected_category, Transportation) or isinstance(self.selected_category, People):
            cell = self.world.get_cell_by_world_coordinate(coordinate)
            if cell.infrastructure_id != -1 and cell.infrastructure_type != ROAD:
                infrastructure = self.world.get_object(INFRASTRUCTURE, cell.infrastructure_type,
                                                       cell.infrastructure_id)
                resources = infrastructure.take_resources(self.selected_category)
                self.world.update_resources(resources)

    def deposit(self, coordinate):
        coordinate = self.format_coordinate(coordinate)
        if isinstance(self.selected_category, Transportation) or isinstance(self.selected_category, People):
            cell = self.world.get_cell_by_world_coordinate(coordinate)
            if cell.infrastructure_id != -1 and cell.infrastructure_type != ROAD:
                infrastructure = self.world.get_object(INFRASTRUCTURE, cell.infrastructure_type,
                                                       cell.infrastructure_id)
                resources = infrastructure.deposit(self.selected_category)
                self.world.update_resources(resources)

    def move(self, coordinate):
        coordinate = self.format_coordinate(coordinate)
        if isinstance(self.selected_category, Transportation):
            return self.world.move(coordinate, TRANSPORTATION, self.selected_category.id, self.selected_category.type)
        if isinstance(self.selected_category, People):
            return self.world.move(coordinate, PEOPLE, self.selected_category.id, self.selected_category.type)

    def set_points(self, args):
        points = int(args[0])
        self.world.set_points(points)

    # +Asserts
    def get_selected_category(self, assert_name):
        return assert_name + " " + self.selected_category.type

    def get_selected_resource(self, assert_name):
        return assert_name + " " + str(self.selected_category.get_resources())

    def get_selected_people(self, assert_name):
        return assert_name + " " + str(self.selected_category.get_amount_of_people())

    def get_city_count(self, assert_name):
        return assert_name + " " + str(len(self.world.objects[INFRASTRUCTURE][CITY].keys()))

    def get_village_count(self, assert_name):
        return assert_name + " " + str(len(self.world.objects[INFRASTRUCTURE][VILLAGE].keys()))

    def get_road_count(self, assert_name):
        return assert_name + " " + str(len(self.world.objects[INFRASTRUCTURE][ROAD].keys()))

    def get_complete(self, assert_name):
        return assert_name + " " + str(False)

    def get_selected_car(self, assert_name):
        if self.selected_category.type == CAR:
            return assert_name + " " + str(1)
        return assert_name + " " + str(0)

    def get_selected_truck(self, assert_name):
        if self.selected_category.type == TRUCK:
            return assert_name + " " + str(1)
        return assert_name + " " + str(0)

    def get_car_count(self, assert_name):
        return assert_name + " " + str(len(self.world.objects[TRANSPORTATION][CAR].keys()))

    def get_truck_count(self, assert_name):
        return assert_name + " " + str(len(self.world.objects[TRANSPORTATION][TRUCK].keys()))

    def get_helicopter_count(self, assert_name):
        return assert_name + " " + str(len(self.world.objects[TRANSPORTATION][HELICOPTER].keys()))

    def get_selected_coordinate(self, assert_name):
        if self.selected_category == None:
            return assert_name + " " + str([0, 0])
        x, y = self.selected_category.coordinate
        tile_size = Configuration.get_tile_size()
        x = x // tile_size[1]
        y = y // tile_size[0]
        return assert_name + " " + str([x, y])

    def get_points(self, assert_name):
        return assert_name + " " + str(self.world.points)
