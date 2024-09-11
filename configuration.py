import json


class Configuration:
    config = open('configuration.json')
    data = json.load(config)

    @staticmethod
    def get_sizes():
        return Configuration.data["Sizes"]

    @staticmethod
    def get_tile_size():
        return Configuration.data["Sizes"]["Tile"]

    @staticmethod
    def get_road_size():
        return Configuration.data["Sizes"]["Road"]

    @staticmethod
    def get_tiles():
        return Configuration.data["Tiles"]

    @staticmethod
    def get_starting_resources():
        return Configuration.data["StartingResources"]

    @staticmethod
    def get_capacities():
        return Configuration.data["Capacities"]

    @staticmethod
    def get_resource_types():
        return Configuration.data["ResourceTypes"]

    @staticmethod
    def get_costs():
        return Configuration.data["Costs"]

    @staticmethod
    def get_tiles_images():
        return Configuration.data["TilesImages"]

    @staticmethod
    def get_objects_images():
        return Configuration.data["ObjectsImages"]
