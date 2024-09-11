from configuration import Configuration
from people import People
import cv2 as cv
from constants import *


class Transportation:
    id = 0

    def __init__(self, coordinate, type):
        Transportation.id += 1
        self.id = Transportation.id
        self.coordinate = coordinate
        self.type = type
        self.resources = [0, 0, 0, 0, 0]
        self.capacities = Configuration.get_capacities()[type]
        self.index_of_people = Configuration.get_resource_types().index(PEOPLE)
        self.people = []

    def update_resources(self, resources):
        for inx, resource in enumerate(resources):
            self.resources[inx] += resource
        return resources[:self.index_of_people]

    def add_resource(self, index, amount):
        resources = [0] * len(self.resources)
        if self.resources[index] + amount <= self.capacities[index]:
            resources[index] += amount
        else:
            resources[index] = self.capacities[index]
        return self.update_resources(resources)

    # Belong ro Resources function
    def set_resource(self, resources):
        resources_to_update = [0] * len(self.resources)

        for inx, resource in enumerate(resources):
            resources_to_update[inx] += resource - self.resources[inx]
        return self.update_resources(resources_to_update)

    def move(self, coordinate):
        self.coordinate = coordinate

    def add_people(self, amount, coordinate):
        people_array = []
        if self.resources[self.index_of_people] + amount > self.capacities[self.index_of_people]:
            amount = self.capacities[self.index_of_people] - self.resources[self.index_of_people]
        for inx in range(amount):
            people = People(coordinate)
            self.people.append(people.id)
            people_array.append(people)
        self.resources[self.index_of_people] += amount
        return people_array

    def get_amount_of_people(self):
        return self.resources[self.index_of_people]

    def get_resources(self):
        return self.resources
