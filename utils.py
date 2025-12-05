import random as generator
import heapq

COLOURS = {
    1: "\033[92m",  # Road = green
    2: "\033[93m",  # Hill = yellow
    8: "\033[94m",  # Water = blue
    9: "\033[91m",  # Obstacle = red
}

PATH_COLOUR = "\033[97;1m"   # Path = bright withe
RESET = "\033[0m"   # RESET is used to stop using any colour and return to normal text

class Grid:
    def __init__(self, width=10, height=10, obstacle_prob=0.2):
        # Initialise the grid size and obstacle probability
        self.width = width
        self.height = height
        self.obstacle_prob = obstacle_prob
        self.grid = self._generate_grid()

    def _generate_grid(self):
        """
        Terrain types:
        1 = road (cost 1)
        2 = hill (cost 2)
        8 = water (cost 8)
        9 = obstacle (impassable)
        """
        grid = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):

                if generator.random() >= self.obstacle_prob:
                    # Random terrain
                    row.append(generator.choice([1, 2, 8]))
                else:
                    # Random obstacle
                    row.append(9)
            # Fills the grid with rows
            grid.append(row)

        # Make start/goal always obstacles free
        grid[0][0] = 1
        grid[self.height - 1][self.width - 1] = 1
        return grid

    def is_valid(self, x, y):
        return (
            # Return if a cell is inside the grid and crossable
            0 <= x < self.width
            and 0 <= y < self.height
            and self.grid[y][x] != 9   # 9 = obstacle
        )

    def cost(self, x, y):
        # Return movement cost of a cell
        return self.grid[y][x]

    def display_no_path(self):
        # Print the grid with no terrain colours if no path is found.
        for row in self.grid:
            print(" ".join(f"{cell}" for cell in row))

    def display_with_path(self, path):
        # Print the grid with terrain colours and highlight the path if A* algorithm finds a path
        path_set = set(path)
        
        print("\nGRID WITH PATH:\n")

        for y in range(self.height):
            row_str = ""
            for x in range(self.width):

                cell = self.grid[y][x]

                # Path highlighted in BRIGHT WHITE
                if (x, y) in path_set:
                    colour = PATH_COLOUR
                else:
                    # Print grid with terrain colours
                    colour = COLOURS[cell]
                row_str += f"{colour}{cell}{RESET} "
                
            print(row_str)

class Robot:
    def __init__(self, grid, start=(0, 0), goal=None):
        # Robot moves from start toward the goal
        self.grid = grid
        self.x, self.y = start
        if goal is None:
            goal = (grid.width - 1, grid.height - 1)
        self.goal_x, self.goal_y = goal

    def get_position(self):
        return (self.x, self.y)

    def at_goal(self):
        return self.x == self.goal_x and self.y == self.goal_y

    def move(self, direction):
        # Try to move the robot in a direction
        dx, dy = 0, 0
        if direction == 'up': dy = -1
        elif direction == 'down': dy = 1
        elif direction == 'left': dx = -1
        elif direction == 'right': dx = 1
        else:
            print("Invalid direction.")
            return False

        new_x = self.x + dx
        new_y = self.y + dy
        # It checks if the new position of the robot is possible
        if self.grid.is_valid(new_x, new_y):
            self.x, self.y = new_x, new_y
            return True
        return False

def A_Star(grid, start, goal):
    
    directions = [(0,1), (0,-1), (1,0), (-1,0)]  # Four allowed movements 
    open_list = []
    heapq.heappush(open_list, (0, start))

    parent_map = {}
    g_value = {start: 0}

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan Distance: it is good for grids without diagonal movements

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            # Reconstruct path
            path = []
            while current in parent_map:
                path.append(current)
                current = parent_map[current]
            # Add the start to the path
            path.append(start)
            # Reverse the path to see the path from start to goal
            path.reverse()
            return path

        for dx, dy in directions:
            # Check the neighbors for each direction
            nx = current[0] + dx
            ny = current[1] + dy
            neighbor = (nx, ny)

            if not grid.is_valid(nx, ny):
                continue

            # Cost based on terrain type
            candidate_g = g_value[current] + grid.cost(nx, ny)

            if neighbor not in g_value or candidate_g < g_value[neighbor]:
                parent_map[neighbor] = current
                g_value[neighbor] = candidate_g
                f_value = candidate_g + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_value, neighbor))

    return None