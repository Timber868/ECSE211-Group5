from subsystems import new_nav
from subsystems.utils.brick import reset_brick

if __name__ == "__main__":
    try:
        new_nav.nav_main()
    except KeyboardInterrupt:
        reset_brick()
        print("Robot was interrupted")
