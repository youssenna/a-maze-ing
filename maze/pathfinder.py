"""Pathfinding module using Breadth-First Search algorithm.

This module provides functionality to find the shortest path through a maze
from an entry point to an exit point using BFS traversal.
"""

from collections import deque
from typing import Any


def init_path(maze: Any) -> Any:
    """Initialize maze cells for BFS pathfinding.

    Resets the BFS-related attributes on all cells in the maze to prepare
    for a new pathfinding operation.

    Args:
        maze: A 2D array of cell objects representing the maze.
    """
    for row in maze:
        for cell in row:
            cell.BFSvisited = False
            cell.parent = None


def pathfinder(maze: Any, ENTRY: Any, EXIT: Any, WIDTH: Any,
               HEIGHT: Any) -> Any:
    """Find the shortest path through a maze using Breadth-First Search.

    Performs BFS traversal from the entry point to find the shortest path
    to the exit point, respecting maze walls.

    Args:
        maze: A 2D array of cell objects representing the maze.
        ENTRY: A tuple (x, y) representing the starting coordinates.
        EXIT: A tuple (x, y) representing the target coordinates.
        WIDTH: The width of the maze in cells.
        HEIGHT: The height of the maze in cells.

    Returns:
        A list of (x, y) tuples representing the path from ENTRY to EXIT,
        in order from start to finish.
    """
    init_path(maze)
    q = deque([ENTRY])
    x, y = ENTRY
    maze[y][x].BFSvisited = True
    while q:

        x, y = q.popleft()

        if (x, y) == EXIT:
            break

        directions = [
            (maze[y][x].north, x, y - 1),
            (maze[y][x].east, x + 1, y),
            (maze[y][x].south, x, y + 1),
            (maze[y][x].west, x - 1, y)
        ]

        for d, dx, dy in directions:
            if (0 <= dx < WIDTH and 0 <= dy < HEIGHT
               and d is False and maze[dy][dx].BFSvisited is False):
                maze[dy][dx].BFSvisited = True
                q.append((dx, dy))
                maze[dy][dx].parent = (x, y)

    path = []
    path.append((x, y))
    while True:
        cx, cy = maze[y][x].parent
        path.append((cx, cy))
        if (cx, cy) == ENTRY:
            break
        x = cx
        y = cy
    path.reverse()
    return path
