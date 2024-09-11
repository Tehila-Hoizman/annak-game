from configuration import Configuration
import cv2 as cv
from constants import *


class People:
    id = 0

    def __init__(self, coordinate):
        People.id += 1
        self.id = People.id
        self.coordinate = coordinate
        self.type = PEOPLE
        self.resources = [0, 0, 0, 0]
        self.capacities = [1, 1, 1, 1]

    def move(self, coordinate):
        self.coordinate = coordinate

    def get_amount_of_people(self):
        return 1

    def get_resources(self):
        return self.resources

    def update_resources(self, resources):
        for inx, resource in enumerate(resources):
            self.resources[inx] += resource
        return resources

    def add_resource(self, index, amount):
        resources = [0] * len(self.resources)
        if self.resources[index] + amount <= self.capacities[index]:
            resources[index] += amount
        else:
            resources[index] = self.capacities[index]
        return self.update_resources(resources)
