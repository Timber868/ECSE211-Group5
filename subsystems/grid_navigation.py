# We assume the starting point is the bottom right corner of the grid and the robot is facing up
# Each row in the grid is a column in the real world
# The starting point is (8, 9) in the grid (bottom right corner)
# The goal is to reach (8, 6) in the grid (bottom middle cell)
# When a cell is visited, it is marked with 1
# When a cell is blocked, it is marked with -1
# We are traversing 9 blocks at a time (3x3)

# import the color functions
from subsystems.motor_arm_settings import open_catcher, close_catcher, stop_sensor_arm, rotate_sensor_arm, rotate_initial_position_arm, arm_limits
from subsystems.motor_settings import wheel_position, rotate, rotate_right
from subsystems.collect_color_sensor_data import collect_color_sensor_data
from subsystems.utils.brick import EV3ColorSensor
import time
import threading

grid = [[0 for i in range(9)] for j in range(9)]        #initialize the grid (9x9)

COLOR_SENSOR_LEFT = EV3ColorSensor(4)
COLOR_SENSOR_RIGHT = EV3ColorSensor(2)
threeXthree_counter = 1
range_to_fill_x = None
range_to_fill_y = None
red_lines_counter = 0
red_detected = False

# ----------------- Functions -----------------------------------
def rgb_to_string(rgb_arr):
    if rgb_arr == [None, None, None]:
        return "None"
    if rgb_arr[0] > 200 and rgb_arr[1] < 100 and rgb_arr[2] < 100:
        return "RED"
    return "None"

def advance_step():
    """
    If red_detected is True, the robot moves forward or rotates based on whether the robot is at the end of a line (line index is multiple of 9)
    When the robot rotates, it first moves back a little to avoid the wall in front
    If red_detected is False, the robot moves forward
    """
    # case 1: red line
    if red_detected:
        if red_lines_counter % 9 == 0:          # end of straight line: go back a little and rotate left (to avoid the wall in front)
            wheel_position(-180, -180, 1)
            rotate(90, 0.1)
        else:
            wheel_position(180, 180, 0.5)       # any "normal" red line: go forward a little
        red_lines_counter += 1
    else:
        wheel_position(120, 120, 0.5)           # no red line: go forward a little

def check_color():
    """
    Measures the color on the ground and sets the global variable red_detected to True if both sensors detect red
    """
    while True:
        right_color = []
        left_color = []

        collect_color_sensor_data(right_color, left_color)

        right_color = rgb_to_string(right_color)
        left_color = rgb_to_string(left_color)

        if right_color == "RED" and left_color == "RED":
            red_detected = True
        else:
            red_detected = False

def polling_action():
    """
    Checks if global variable red_detected is True and performs the necessary actions
    If red_detected is True, the grid's completion is updated and the robot moves forward or rotates based on the decision in advance_step()
    If red_detected is False, the robot moves forward (see advance_step())
    """

    # tuples of ranges to fill the grid
    while True:
        if red_detected:

            if threeXthree_counter == 1:
                range_to_fill_x = (6, 9)
                range_to_fill_y = (6, 9)
            if threeXthree_counter == 2:
                range_to_fill_x = (6, 9)
                range_to_fill_y = (3, 6)
            if threeXthree_counter == 3:
                range_to_fill_x = (6, 9)
                range_to_fill_y = (0, 3)
            if threeXthree_counter == 4:
                range_to_fill_x = (3, 6)
                range_to_fill_y = (0, 3)
            if threeXthree_counter == 5:
                range_to_fill_x = (0, 3)
                range_to_fill_y = (0, 3)
            if threeXthree_counter == 6:
                range_to_fill_x = (0, 3)
                range_to_fill_y = (3, 6)
            if threeXthree_counter == 7:
                range_to_fill_x = (0, 3)
                range_to_fill_y = (6, 9)
            if threeXthree_counter == 8:
                range_to_fill_x = (3, 6)
                range_to_fill_y = (6, 9)
                    

            # fill the grid with 1s
            for i in range(range_to_fill_y[0], range_to_fill_y[1]):
                for j in range(range_to_fill_x[0], range_to_fill_x[1]):
                    grid[i][j] = 1

            # visual representation of current grid completion
            for line in grid:
                print(*line)
            print("-----------------")

            # check if the grid is complete (complete when there are 3 incomplete rows (containing at least one 0))
            incomplete_rows = len([i for i in range(9) if 0 in grid[i]])
            print("Incomplete rows: ", incomplete_rows)
            if incomplete_rows == 3:
                print("Traversal complete!")
                exit()

            # move forward
            advance_step()
    else:
        advance_step()


def main():
    check_color_thread = threading.Thread(target=check_color)
    check_color_thread.start()

    while True:
        polling_action()



# i=1
# while i < 9:
#     traverse_map()
#     threeXthree_counter += 1
#     for line in grid:
#         print(*line)
#     print("-----------------")
#     time.sleep(0.5)
#     i += 1

if __name__ == "__main__":
    main()