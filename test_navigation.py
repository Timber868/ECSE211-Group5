from subsystems import grid_navigation
from subsystems.utils.brick import reset_brick

if __name__ == "__main__":
    try:
        grid_navigation.main()
    except KeyboardInterrupt:
        reset_brick()
        print("Robot was interrupted")