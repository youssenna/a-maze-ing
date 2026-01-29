import random
from typing import Any
from utils.errors import InvalidDistinationFor42Path, InvalidEntryExitPoint


class Cell:
    """
    Represents a single cell in the maze.

    Attributes:
        north (bool): True if the north wall exists.
        south (bool): True if the south wall exists.
        east (bool): True if the east wall exists.
        west (bool): True if the west wall exists.
        visited (bool): True if the cell has been visited during maze
        generation.
        _42_path (bool): True if the cell is part of the special "42 pattern"
        path.
    """
    def __init__(self) -> None:
        """Initialize a cell with all walls intact and not visited."""
        self.north: bool = True
        self.west: bool = True
        self.south: bool = True
        self.east: bool = True
        self.visited = False
        self._42_path = False


class MazeGenerator:
    """
    Generates mazes using different algorithms (Backtracker, Prim's) and can
    create a special "42 pattern" path for mazes.

    Attributes:
        x (int): Number of columns in the maze.
        y (int): Number of rows in the maze.
        maze (list[list[Cell]]): 2D grid representing the maze.
        stack (list[list[Cell]]): Helper stack used in some algorithms.
        entry (tuple[int, int]): Coordinates of the maze entry point.
        exit (tuple[int, int]): Coordinates of the maze exit point.
        out_file (str): Path to the file where the maze output will be saved.
    """
    def __init__(self, cols: int, rows: int, Entry: Any, EXIT: Any,
                 out_file: Any) -> None:
        """
        Initialize the maze generator with dimensions, entry/exit points, and
        output file.

        Args:
            cols (int): Number of columns.
            rows (int): Number of rows.
            Entry (tuple[int, int]): Entry point coordinates.
            EXIT (tuple[int, int]): Exit point coordinates.
            out_file (str): Path to the output file.
        """
        self.x = cols
        self.y = rows
        self.maze:  list[list[Cell]] = self.creat_grid()
        self.stack: list[list[Cell]] = []
        self.entry = Entry
        self.exit = EXIT
        self.out_file = out_file

    def creat_grid(self) -> list[list[Cell]]:
        """
        Create a 2D grid of Cell objects.

        Returns:
            list[list[Cell]]: A grid with all cells initialized with walls.
        """
        return [[Cell() for _ in range(self.x)] for _ in range(self.y)]

    def find_nighbors(self, cell: Any) -> list[tuple[int, int, str]]:
        """
        Find all unvisited neighbor cells of a given cell.

        Args:
            cell (tuple[int, int]): Coordinates (x, y) of the current cell.

        Returns:
            list[tuple[int, int, str]]: List of tuples with neighbor
            coordinates
            and direction relative to the current cell.
        """
        x, y = cell
        maze = self.maze
        unvisited_cells = []
        if (x - 1 >= 0 and not maze[y][x-1].visited
                and not self.maze[y][x - 1]._42_path):
            unvisited_cells.append((x-1, y, "left"))
        if (x + 1 < self.x and not maze[y][x+1].visited
                and not self.maze[y][x + 1]._42_path):
            unvisited_cells.append((x+1, y, "right"))
        if (y - 1 >= 0 and not maze[y-1][x].visited
                and not self.maze[y - 1][x]._42_path):
            unvisited_cells.append((x, y-1, "top"))
        if (y + 1 < self.y and not maze[y+1][x].visited
                and not self.maze[y + 1][x]._42_path):
            unvisited_cells.append((x, y+1, "bottom"))
        return unvisited_cells

    def creat_maze_bakctracker_algo(self) -> None:
        """
        Generate a maze using the recursive backtracker algorithm.
        Also checks and preserves the "42 pattern" if applicable.

        Raises:
            InvalidDistinationFor42Path: If the maze is too small for 42
            pattern.
            InvalidEntryExitPoint: If entry or exit points are inside the 42
            path.
        """
        entry = self.entry
        exit = self.exit
        if (self.x < 9 or self.y < 9):
            str = "Warning: invalid path for 42 pathern.\n'we will \
generat maze without 42 pathern'"
            raise InvalidDistinationFor42Path(str)
        self.creat_42_pathren()
        if (self.maze[entry[1]][entry[0]]._42_path or
           self.maze[exit[1]][exit[0]]._42_path):
            raise InvalidEntryExitPoint("Try other exit or entry point it's \
invalid (inside '42 path')")
        self.remove_walls_backtracker_algo()

    def creat_maze_prims_algo(self) -> None:
        """
        Generate a maze using Prim's algorithm.
        Also checks and preserves the "42 pattern" if applicable.

        Raises:
            InvalidDistinationFor42Path: If the maze is too small for 42
            pattern.
            InvalidEntryExitPoint: If entry or exit points are inside the 42
            path.
        """
        entry = self.entry
        exit = self.exit
        if (self.x < 9 or self.y < 9):
            str = "Warning: invalid path \
for 42 pathern.\n'we will generat maze without 42 pathern'"
            raise InvalidDistinationFor42Path(str)
        self.creat_42_pathren()
        if (self.maze[entry[1]][entry[0]]._42_path is True or
           self.maze[exit[1]][exit[0]]._42_path is True):
            raise InvalidEntryExitPoint("Try other exit or entry point it's \
invalid (inside '42 path')")
        self.remove_walls_prims_algo()

    def remove_walls_backtracker_algo(self, i: int = 0, j: int = 0) -> None:
        """
        Recursively remove walls using the backtracker algorithm starting from
        (i, j).

        Args:
            i (int): X-coordinate to start.
            j (int): Y-coordinate to start.
        """
        self.maze[j][i].visited = True
        neighbors = self.find_nighbors((i, j))
        while neighbors:
            next_cell = random.choice(neighbors)
            new_x, new_y, direction = next_cell
            self.maze[new_y][new_x].visited = True
            if direction == "left":
                self.maze[j][i].west = False
                self.maze[new_y][new_x].east = False
            elif direction == "right":
                self.maze[j][i].east = False
                self.maze[new_y][new_x].west = False
            elif direction == "top":
                self.maze[j][i].north = False
                self.maze[new_y][new_x].south = False
            elif direction == "bottom":
                self.maze[j][i].south = False
                self.maze[new_y][new_x].north = False
            self.remove_walls_backtracker_algo(new_x, new_y)
            neighbors = self.find_nighbors((i, j))

    def find_visited_cell(self, cell: tuple[int, int]) -> Any:
        """
        Find all neighboring cells that have already been visited.

        Args:
            cell (tuple[int, int]): Coordinates (x, y) of the current cell.

        Returns:
            list[tuple[int, int, str]]: List of visited neighbor cells with
            their
            coordinates and direction relative to the current cell.
        """
        x, y = cell
        maze = self.maze
        visited_cells = []
        if x - 1 >= 0 and maze[y][x-1].visited:
            visited_cells.append((x-1, y, "left"))
        if x + 1 < self.x and maze[y][x+1].visited:
            visited_cells.append((x+1, y, "right"))
        if y - 1 >= 0 and maze[y-1][x].visited:
            visited_cells.append((x, y-1, "top"))
        if y + 1 < self.y and maze[y+1][x].visited:
            visited_cells.append((x, y+1, "bottom"))
        # if visited_cells != []:
        return visited_cells
        # return None

    @staticmethod
    def remove_duplicate_and_visited(items: Any) -> Any:
        """
        Remove duplicates from a list of cells.

        Args:
            items (list[tuple[int, int, str]]): List of cells with coordinates
            and directions.

        Returns:
            list[tuple[int, int, str]]: List with duplicates removed.
        """
        none_duplicate: Any = []
        for item in items:
            if item not in none_duplicate:
                none_duplicate.append(item)
        return none_duplicate

    def remove_wall(self, cell1: tuple[int, int, str], cell2: Any) -> None:
        """
        Remove the wall between two adjacent cells.

        Args:
            cell1 (tuple[int, int, str]): Coordinates (x, y) and direction of
            the first cell.
            cell2 (tuple[int, int, str]): Coordinates (x, y) and direction of
            the second cell.
        """
        x1 = cell1[0]
        y1 = cell1[1]
        x2 = cell2[0]
        y2 = cell2[1]

        if x1 - 1 == x2 and y1 == y2:
            self.maze[y1][x1].west = False
            self.maze[y2][x2].east = False
        elif x1 + 1 == x2 and y1 == y2:
            self.maze[y1][x1].east = False
            self.maze[y2][x2].west = False
        elif x1 == x2 and y1 + 1 == y2:
            self.maze[y1][x1].south = False
            self.maze[y2][x2].north = False
        elif x1 == x2 and y1 - 1 == y2:
            self.maze[y1][x1].north = False
            self.maze[y2][x2].south = False

    def remove_walls_prims_algo(self, i: int = 0, j: int = 0) -> None:
        """
    Generate a maze using Prim's algorithm starting from the cell (i, j).

    This algorithm works by maintaining a list of frontier cells (cells
    adjacent
    to the maze) and repeatedly adding a random frontier cell to the maze while
    removing the wall between it and an already visited neighboring cell.

    Args:
        i (int): X-coordinate of the starting cell. Defaults to 0.
        j (int): Y-coordinate of the starting cell. Defaults to 0.

    Notes:
        - Uses `self.find_nighbors` to find unvisited neighboring cells.
        - Uses `self.find_visited_cell` to select which wall to remove when
          connecting the frontier cell to the maze.
        - Handles cells with the "42 pattern" if present.
        - Random choice is used both for selecting the next frontier cell and
          in case multiple visited neighbors exist.
        - Walls are removed appropriately using `self.remove_wall` or direct
          attribute manipulation depending on directions.

    Modifies:
        - `self.maze`: Updates visited status of cells and removes walls
        between
          cells to form the maze.
        - `frentier_cells`: Dynamically updated as the algorithm progresses.
    """
        self.maze[j][i].visited = True

        frentier_cells = self.find_nighbors((i, j))
        while frentier_cells:
            target_cell = random.choice(frentier_cells)
            new_x, new_y, old_direction = target_cell
            self.maze[new_y][new_x].visited = True
            frentier_cells.extend(self.find_nighbors((new_x, new_y)))
            frentier_cells = self.remove_duplicate_and_visited(frentier_cells)
            cell = self.find_visited_cell((new_x, new_y))
            if len(cell) == 1:
                i, j, new_direction = cell[0][0], cell[0][1], cell[0][2]
                if old_direction == "left" and new_direction == "right":
                    self.maze[j][i].west = False
                    self.maze[new_y][new_x].east = False
                elif old_direction == "right" and new_direction == "left":
                    self.maze[j][i].east = False
                    self.maze[new_y][new_x].west = False
                elif old_direction == "top" and new_direction == "bottom":
                    self.maze[j][i].north = False
                    self.maze[new_y][new_x].south = False
                elif old_direction == "bottom" and new_direction == "top":
                    self.maze[j][i].south = False
                    self.maze[new_y][new_x].north = False
                    i = new_x
                    j = new_y
            else:
                cell = random.choice(cell)
                self.remove_wall(target_cell, cell)
                i = cell[0]
                j = cell[1]

            frentier_cells.remove(target_cell)

    def creat_42_pathren(self) -> None:
        """
        Generate a predefined '42' shaped path inside the maze.

        The path is marked by setting the _42_path attribute of cells to True.
        Ensures the 42 pattern is centered in the maze and does not overlap
        walls.
        """
        x = self.x // 2 - 3
        y = self.y // 2 - 3
        first_y = y
        # show 4
        for move in range(0, 4):
            self.maze[y + move][x]._42_path = True
            last_y = move
        y += last_y
        for move in range(1, 3):
            self.maze[y][x + move]._42_path = True
            last_x = move
        x += last_x
        for move in range(1, 4):
            self.maze[y + move][x]._42_path = True
            last_y = move
        y += last_y
        y = first_y
        x += 2
        # show 2
        for move in range(0, 3):
            self.maze[y][x + move]._42_path = True
            last_x = move
        x += last_x
        for move in range(1, 4):
            self.maze[y + move][x]._42_path = True
            last_y = move
        y += last_y
        for move in range(1, 3):
            self.maze[y][x - move]._42_path = True
            last_x = move
        x -= last_x
        for move in range(1, 4):
            self.maze[y + move][x]._42_path = True
            last_y = move
        y += last_y
        for move in range(1, 3):
            self.maze[y][x + move]._42_path = True
            last_x = move
        x += last_x

    #  i need to fix return
    @staticmethod
    def print_walls_as_hex(cell: Cell) -> Any:
        """
        Convert the walls of a cell into a single hexadecimal character.

        Each wall corresponds to a bit: N=1, E=2, S=4, W=8 (F=all walls).

        Args:
            cell (Cell): The cell to convert.

        Returns:
            str: Hexadecimal representation of the cell's walls.
        """
        if (cell.north and cell.east and cell.south and cell.west):
            return "F"
        elif (not cell.north and cell.east and cell.south and cell.west):
            return "E"
        elif (cell.north and not cell.east and cell.south and cell.west):
            return "D"
        elif (not cell.north and not cell.east and cell.south
              and cell.west):
            return "C"
        elif (cell.north and cell.east and not cell.south and cell.west):
            return "B"
        elif (not cell.north and cell.east and not cell.south and cell.west):
            return "A"
        elif (cell.north and not cell.east and not cell.south and cell.west):
            return "9"
        elif (not cell.north and not cell.east and not cell.south
              and cell.west):
            return "8"
        elif (cell.north and cell.east and cell.south and not cell.west):
            return "7"
        elif (not cell.north and cell.east and cell.south and not cell.west):
            return "6"
        elif (cell.north and not cell.east and cell.south and not cell.west):
            return "5"
        elif (not cell.north and not cell.east and cell.south
              and not cell.west):
            return "4"
        elif (cell.north and cell.east and not cell.south and not cell.west):
            return "3"
        elif (not cell.north and cell.east and not cell.south
              and not cell.west):
            return "2"
        elif (cell.north and not cell.east and not cell.south
              and not cell.west):
            return "1"
        elif (not cell.north and not cell.east and not cell.south
              and not cell.west):
            return "0"
        return None

    # this function those not finish
    def creat_output_file(self, path: Any) -> None:
        """
        Save the maze to a file with walls in hex and the path, entry, and
        exit.

        Args:
            path (list[tuple[int, int]]): The solution path to print in the
            file.
        """
        with open(self.out_file, "w") as file:
            for y in range(self.y):
                for x in range(self.x):
                    file.write(f"{self.print_walls_as_hex(self.maze[y][x])}")
                file.write("\n")
            file.write("\n")
            file.write(f"{self.entry[0]}, {self.entry[1]}\n"
                       f"{self.exit[0]}, {self.exit[1]}\n")
            file.write(f"{self.print_path(path)}\n")

    @staticmethod
    def print_path(path: list[tuple[int, int]]) -> str:
        """
        Convert a path of coordinates into directions (N, S, E, W).

        Args:
            path (list[tuple[int, int]]): List of coordinates representing the
            path.

        Returns:
            str: String of directions representing the path.
        """
        # prev move
        x1, y1 = path[0]
        path_directions = ""
        for i in range(1, len(path)):
            # next move
            x2, y2 = path[i]
            if x1 == x2 and y1 - 1 == y2:
                path_directions += "N"
            elif x1 == x2 and y1 + 1 == y2:
                path_directions += "S"
            elif x1 - 1 == x2 and y1 == y2:
                path_directions += "W"
            elif x1 + 1 == x2 and y1 == y2:
                path_directions += "E"
            x1, y1 = path[i]
        return path_directions

    # def debug_print(self) -> None:
    #     """
    #     Print the maze to the terminal for debugging purposes.

    #     Displays walls as "====" for top walls and "||" for side walls.
    #     """
    #     for y in range(self.y):
    #         # top walls
    #         for x in range(self.x):
    #             print("====" if self.maze[y][x].north else "=   ", end="")
    #         print("=")

    #         # side walls
    #         for x in range(self.x):
    #             print("||  " if self.maze[y][x].west else "    ", end="")
    #         print("||")

    #     # bottom border
    #     print("====" * self.x + "=")
