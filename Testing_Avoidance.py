from subsystems import Avoidance
from subsystems.utils.brick import reset_brick

if __name__ == "__main__":
    try:
        Avoidance.avoid_block_left()
    except KeyboardInterrupt:
        reset_brick()
        print("Robot was interrupted")
