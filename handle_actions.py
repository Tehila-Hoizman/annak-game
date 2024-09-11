from actions import Actions


class Handle_actions:
    def __init__(self, world):
        self.actions = Actions(world)
        self.actions_dict = {
            "Resource": self.actions.update_resource,
            "People": self.actions.add_people,
            "Build": self.actions.build,
            "Manufacture": self.actions.manufacture,
            "MakeEmpty": self.actions.make_empty,
            "Resources": self.actions.update_resources,
            "Deposit": self.actions.deposit,
            "Move": self.actions.move,
            "SetPoints": self.actions.set_points,
            "Select": self.actions.select,
            "Work": self.actions.work,
            "Rain": self.actions.rain,
            "TakeResources": self.actions.take_resources,
            "SelectedCategory": self.actions.get_selected_category,
            "SelectedResource": self.actions.get_selected_resource,
            "SelectedPeople": self.actions.get_selected_people,
        }
        self.asserts_dict = {
            "SelectedCategory": self.actions.get_selected_category,
            "SelectedResource": self.actions.get_selected_resource,
            "SelectedPeople": self.actions.get_selected_people,
            "CityCount": self.actions.get_city_count,
            "VillageCount": self.actions.get_village_count,
            "RoadCount": self.actions.get_road_count,
            "SelectedComplete": self.actions.get_complete,
            "SelectedCar": self.actions.get_selected_car,
            "SelectedTruck": self.actions.get_selected_truck,
            "CarCount": self.actions.get_car_count,
            "TruckCount": self.actions.get_truck_count,
            "HelicopterCount": self.actions.get_helicopter_count,
            "SelectedCoordinates": self.actions.get_selected_coordinate,
            "Points": self.actions.get_points,
        }

    def handle_start(self, inp):
        for st in inp.start:
            self.actions_dict[st.name](st.arguments)

    def handle_input(self, inp):
        for step in inp.steps:
            self.actions_dict[step.name](step.arguments)

    def handle_assert(self, inp):
        for command in inp.asserts:
            self.asserts_dict[command](command)

    def start_game(self):
        self.actions.start_game()
