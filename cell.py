from constants import *


class Cell:
    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.infrastructure_type = ''
        self.infrastructure_id = -1
        self.transportation_type = ''
        self.transportation_id = -1
        self.people_id = -1

    def get_category(self):
        if self.people_id != -1:
            return [PEOPLE, '', self.people_id]
        if self.transportation_id != -1:
            return [TRANSPORTATION, self.transportation_type, self.transportation_id]
        if self.infrastructure_id != -1:
            return [INFRASTRUCTURE, self.infrastructure_type, self.infrastructure_id]
        return [TILE, '', -1]

    def remove_object(self, type_object):
        if type_object == PEOPLE:
            self.people_id = -1
        if type_object == TRANSPORTATION:
            self.transportation_id = -1
            self.transportation_type = ''
        if type_object == INFRASTRUCTURE:
            self.infrastructure_id = -1
            self.infrastructure_type = ''

    def add_object(self, type_object, id, type):
        if type_object == PEOPLE:
            self.people_id = id
        if type_object == TRANSPORTATION:
            self.transportation_id = id
            self.transportation_type = type
        if type_object == INFRASTRUCTURE:
            self.infrastructure_id = id
            self.infrastructure_type = type
