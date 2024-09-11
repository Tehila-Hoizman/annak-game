from world import World
from input import Input
from handle_actions import Handle_actions
import cv2 as cv
from GUI import Gui
import json

if __name__ == '__main__':
    # Receiving the input values
    inp = Input("input.txt")
    inp.parse_and_store()

    # Handles "+World"
    size_matrix = [[int(col) for col in row] for row in inp.world.data]
    world = World(size_matrix)
    handle_actions = Handle_actions(world)

    # Handles "+Start"
    handle_actions.handle_start(inp)

    handle_actions.start_game()

    # Handles "+Input"
    handle_actions.handle_input(inp)

    # Handles "+Asserts"
    handle_actions.handle_assert(inp)
    gui = Gui(world)
    bkg = gui.bkg
    while True:
        gui.bkg = bkg.copy()
        gui.draw()
        cv.imshow("Display window", gui.bkg)
        k = cv.waitKey(1000)
