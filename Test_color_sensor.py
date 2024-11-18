from subsystems import color_sensor_start_stop
from subsystems.utils.brick import reset_brick

if __name__ == "__main__":
    try:
        get_left_sensor_color = color_sensor_start_stop.get_left_sensor_color()
        print(get_left_sensor_color)
    except KeyboardInterrupt:
        reset_brick()
        print("Robot was interrupted")