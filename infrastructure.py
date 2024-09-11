from configuration import Configuration
from people import People
import cv2 as cv
from constants import *
class Infrastructure:
    id = 0

    def __init__(self, coordinate, type):
        self.coordinate = coordinate
        self.type = type
        Infrastructure.id += 1
        self.id = Infrastructure.id
        self.resources = [0, 0, 0, 0, 0 if type == ROAD else Configuration.get_starting_resources()[type]]
        self.capacities = [0, 0, 0, 0] if type == ROAD else Configuration.get_capacities()[type]
        self.objects = {
            CAR: [],
            TRUCK: [],
            HELICOPTER: [],
            PEOPLE: []
        }
        self.index_of_people = Configuration.get_resource_types().index("People")

    def update_resources(self, resources):
        for inx, resource in enumerate(resources):
            self.resources[inx] += resource
        return resources[:self.index_of_people]

    # Belong ro Resources function
    def set_resource(self, resources):
        resources_to_update = [0] * len(self.resources)

        for inx, resource in enumerate(resources):
            resources_to_update[inx] += resource - self.resources[inx]
        return self.update_resources(resources_to_update)

    def add_resource(self, index, amount):
        resources = [0] * len(self.resources)
        if self.resources[index] + amount <= self.capacities[index]:
            resources[index] += amount
        else:
            resources[index] = self.capacities[index]
        return self.update_resources(resources)

    # The function does not yet handle the emptying of transport vehicles
    def make_empty(self):
        resources = [(resource * -1) for resource in self.resources]
        return self.update_resources(resources)

    def take_resources(self, object):
        resources = [0] * len(self.resources)
        for inx, resource in enumerate(object.resources):
            capacity = object.capacities[inx] - resource
            if capacity <= self.resources[inx]:
                object.resources[inx] += capacity
                resources[inx] = capacity * -1
            else:
                object.resources[inx] += self.resources[inx]
                resources[inx] = self.resources[inx] * -1
        return self.update_resources(resources)

    def deposit(self, object):
        resources = [0] * len(self.resources)
        for inx, resource in enumerate(object.resources):
            capacity = self.capacities[inx] - self.resources[inx]
            if capacity <= resource:
                object.resources[inx] -= capacity
                resources[inx] = capacity
            else:
                object.resources[inx] -= resource
                resources[inx] = resource
        return self.update_resources(resources)

    def add_people(self, amount, coordinate):
        people_array = []
        if self.resources[self.index_of_people]+amount > self.capacities[self.index_of_people]:
            amount = self.capacities[self.index_of_people] - self.resources[self.index_of_people]
        for inx in range(amount):
            people = People(coordinate)
            self.objects[PEOPLE].append(people.id)
            people_array.append(people)
        self.resources[self.index_of_people] += amount
        return people_array
    def get_resources(self):
        return self.resources[:self.index_of_people]

    def get_amount_of_people(self):
        return self.resources[self.index_of_people]

