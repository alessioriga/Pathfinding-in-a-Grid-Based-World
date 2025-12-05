from utils import *

if __name__ == "__main__":
    grid = Grid()
    robot = Robot(grid)

    print("\nLEGEND:")
    print(f"{COLOURS[1]}1{RESET} = Road (cost 1)")
    print(f"{COLOURS[2]}2{RESET} = Hill (cost 2)")
    print(f"{COLOURS[8]}8{RESET} = Water (cost 8)")
    print(f"{COLOURS[9]}9{RESET} = Obstacle (impassable)")
    
    print("\nStart:", robot.get_position())
    print("Goal:", (robot.goal_x, robot.goal_y))

    path = A_Star(grid, robot.get_position(), (robot.goal_x, robot.goal_y))

    if path:
        print("\nPath found (row = y,col= x):")
        for (x, y) in path:
            print(f"({y}, {x})", end=" ")
        print()

        print("Total cost:", sum(grid.cost(x,y) for x,y in path))
        print("Steps:", len(path)-1)

        grid.display_with_path(path)
    else:
        print("\nNo path found.")
        grid.display_no_path()