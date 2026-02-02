import time
import random
import sys
from typing import Any
from maze.mazegen import (MazeGenerator)
from maze.pathfinder import pathfinder
from utils.errors import (InvalidCoordinates, InvalidDistinationFor42Path,
                          InvalidEntryExitPoint)

try:
    from mlx import Mlx
except ModuleNotFoundError:
    ModuleNotFoundError(
        "❌ Error: MiniLibX (mlx) module not found.\n"
        "👉 Make sure you:\n"
        "   - Built MiniLibX with `make`\n"
        "   - Installed the Python wheel (.whl)\n"
    )


"""Render module for maze visualization using MiniLibX.

This module provides functionality to render and interact with generated mazes
using the MiniLibX graphics library. It supports player movement, pathfinding
visualization, and maze regeneration.
"""


def mlx_render(width: Any, length: Any, ENTRY: Any, EXIT: Any,
               out_file: str, is_perfect: bool, seed: bool) -> Any:
    """Render and display an interactive maze using MiniLibX.

    Creates a graphical window displaying a procedurally generated maze.
    Supports player movement with arrow keys, pathfinding visualization,
    and maze regeneration.

    Args:
        width: The width of the maze in cells (minimum 6, maximum 48).
        length: The height/length of the maze in cells (minimum 6, maximum 25).
        ENTRY: A tuple (x, y) representing the entry point coordinates.
        EXIT: A tuple (x, y) representing the exit point coordinates.
        out_file: Path to the output file where maze data will be saved.
        is_perfect: If True, generates a perfect maze using backtracker
        algorithm.
            If False, uses Prim's algorithm which may create loops.
        seed: If True, uses a fixed random seed (1) for reproducible mazes.

    Raises:
        InvalidCoordinates: If window size exceeds screen resolution
        (1920x1000) or if dimensions are below minimum (6x6).
        InvalidEntryExitPoint: If entry or exit points are invalid.

    Controls:
        - Arrow keys: Move player through the maze
        - ESC: Exit the application
        - P: Show path from current position to exit
        - G: Generate a new maze
        - H: Hide path and refresh display
        - C: Change wall color randomly
    """
    width_pixel = width * 40
    length_pixel = length * 40
    if width_pixel > 1920 or length_pixel > 1000:
        raise InvalidCoordinates(
                "❌ Error: Window size exceeds screen resolution.\n"
                f"Requested: {width}x{length}\n"
                "Maximum allowed: 48x25\n"
                "👉 Please reduce WIDTH or HEIGHT to fit your screen."
        )
    if width < 6 or length < 6:
        raise InvalidCoordinates(
            "❌ Error: Invalid coordinates.\n"
            "Minimum allowed: 6x6"
        )

    output_file = out_file
    maze = MazeGenerator(width, length, ENTRY, EXIT, out_file)
    try:
        if seed:
            random.seed(1)
        if not is_perfect:
            maze.creat_maze_prims_algo()
        else:
            maze.creat_maze_bakctracker_algo()
        maze.creat_output_file(pathfinder(maze.maze, ENTRY, EXIT, width,
                                          length))
    except InvalidEntryExitPoint as e:
        print(f"Error: {e}")
        sys.exit()

    except InvalidDistinationFor42Path as e:
        print(e)
        if not is_perfect:
            maze.remove_walls_prims_algo()
        else:
            maze.remove_walls_backtracker_algo()
        maze.creat_output_file(pathfinder(maze.maze, ENTRY, EXIT, width,
                                          length))

    mlx1 = Mlx()
    k = mlx1.mlx_init()
    win = mlx1.mlx_new_window(k, width_pixel, length_pixel, "YEB&YEN Maze_gen")
    mz = maze.maze
    img = mlx1.mlx_new_image(k, width_pixel, length_pixel)
    result = mlx1.mlx_get_data_addr(img)
    data = result[0]
    size_line = result[2]

    def put_pixel(x: Any, y: Any, color: Any) -> Any:
        """Put a pixel at (x, y) with the given color in the image data.

        Args:
            x: The x-coordinate of the pixel.
            y: The y-coordinate of the pixel.
            color: The color value as an integer (RGB format).

        Note:
            Pixels outside the image boundaries are silently ignored.
        """
        if 0 <= x < width_pixel and 0 <= y < length_pixel:
            offset = y * size_line + x * 4
            if offset + 4 <= len(data):
                byte = color.to_bytes(3, 'little')
                data[offset] = byte[0]
                data[offset + 1] = byte[1]
                data[offset + 2] = byte[2]
                data[offset + 3] = 255

    bg_img, bg_width, bg_lenght = mlx1.mlx_xpm_file_to_image(
                                        k,
                                        "assets/maze_bg_40.xpm")
    pl_img, pl_width, pl_lenght = mlx1.mlx_xpm_file_to_image(
                                        k,
                                        "assets/player_idle1.xpm")

    def back_img() -> Any:
        """Render the background image by tiling it across the entire window.

        Tiles the background XPM image to cover the complete window area,
        creating a seamless background pattern for the maze.
        """
        for y in range(0, length_pixel, bg_lenght):
            for x in range(0, width_pixel, bg_width):
                mlx1.mlx_put_image_to_window(k, win, bg_img, x, y)

    back_img()
    back_img()

    def player(x: Any, y: Any) -> Any:
        """Draw the player sprite at the specified position.

        Args:
            x: The x-coordinate in pixels where the player will be drawn.
            y: The y-coordinate in pixels where the player will be drawn.
        """
        mlx1.mlx_put_image_to_window(k, win, pl_img, x, y)

    colors = [
        0xFFFFFF,  # white
        0xFF0000,  # red
        0x00FF00,  # green
        0x0000FF,  # blue
        0xFFFF00,  # yellow
        0x00FFFF,  # cyan
        0xFF00FF,  # magenta
    ]
    wall_color = random.choice(colors)

    path_end_img, path_end_width, path_end_length = mlx1.mlx_xpm_file_to_image(
        k, "assets/path_end.xpm")
    path_start_img, _, _ = mlx1.mlx_xpm_file_to_image(
        k, "assets/path_start.xpm")
    down_img, _, _ = mlx1.mlx_xpm_file_to_image(
        k, "assets/arrow_down.xpm")
    up_img, _, _ = mlx1.mlx_xpm_file_to_image(
        k, "assets/arrow_up.xpm")
    right_img, _, _ = mlx1.mlx_xpm_file_to_image(
        k, "assets/arrow_right.xpm")
    left_img, _, _ = mlx1.mlx_xpm_file_to_image(
        k, "assets/arrow_left.xpm")
    image_42, _, _, = mlx1.mlx_xpm_file_to_image(
        k, "assets/wall_1337_neon.xpm")

    def draw_42(mz: Any) -> Any:
        """Draw special '42' themed wall images on cells marked with _42_path.

        Iterates through the maze and renders the special 42 neon wall image
        on any cell that has the _42_path attribute set to True.

        Args:
            mz: The 2D maze array containing cell objects.
        """
        y_offset = 0
        for row in mz:
            x_offset = 0
            for cell in row:
                if cell._42_path is True:
                    mlx1.mlx_put_image_to_window(
                        k, win, image_42, x_offset, y_offset)
                x_offset += 40
            y_offset += 40

    directions = [down_img, up_img, right_img, left_img]

    mlx1.mlx_put_image_to_window(k,
                                 win,
                                 path_start_img,
                                 ENTRY[0] * 40 + 10,
                                 ENTRY[1] * 40 + 10)

    mlx1.mlx_put_image_to_window(k,
                                 win,
                                 path_end_img,
                                 EXIT[0] * 40 + 10,
                                 EXIT[1] * 40 + 10)
    pl_x = ENTRY[0] * 40 + 10
    pl_y = ENTRY[1] * 40 + 10

    def draw_path() -> Any:
        """Visualize the solution path from the player's current position to
        the exit.

        Calculates the shortest path using the pathfinder algorithm and renders
        directional arrow indicators on each cell of the path, showing the
        direction to travel (up, down, left, or right).
        """
        path = pathfinder(mz, (pl_x // 40, pl_y // 40), EXIT, width, length)
        direction_i = 0
        CELL = 40
        i = 1
        for x, y in path:
            for nx, ny in path[i:]:
                if ny > y and nx == x:
                    direction_i = 0
                elif ny < y and nx == x:
                    direction_i = 1
                elif nx > x and ny == y:
                    direction_i = 2
                elif nx < x and ny == y:
                    direction_i = 3
                px = x * CELL + 10
                py = y * CELL + 10
                if ((x, y) != ENTRY and (x, y) != EXIT
                   and (x, y) != (pl_x // 40, pl_y // 40)):
                    time.sleep(0.0001)
                    mlx1.mlx_put_image_to_window(k,
                                                 win,
                                                 directions[direction_i],
                                                 px,
                                                 py)
                i += 1
                break

    def draw_maze(maze: Any, color: Any, sleep: Any) -> Any:
        """Render the maze walls to the image buffer.

        Draws all walls of the maze by iterating through each cell and
        rendering its north, south, east, and west walls based on the
        cell's wall properties.

        Args:
            maze: The 2D maze array containing cell objects with wall
            properties.
            color: The color value for the walls as an integer (RGB format).
            sleep: If True, adds a small delay between drawing cells for an
                  animated effect. If False, draws immediately.
        """
        CELL = 40
        y_offset = 0
        for row in maze:
            x_offset = 0
            for cell in row:
                if cell.north:
                    for x in range(x_offset, x_offset + CELL):
                        put_pixel(x, y_offset, color)

                if cell.south:
                    for x in range(x_offset, x_offset + CELL):
                        put_pixel(x, y_offset + CELL - 1, color)

                if sleep is True:
                    time.sleep(0.001)
                    mlx1.mlx_put_image_to_window(k, win, img, 0, 0)

                if cell.west:
                    for y in range(y_offset, y_offset + CELL):
                        put_pixel(x_offset, y, color)

                if cell.east:
                    for y in range(y_offset, y_offset + CELL):
                        put_pixel(x_offset + CELL - 1, y, color)

                x_offset += CELL
            y_offset += CELL

    draw_maze(mz, wall_color, True)

    def render() -> Any:
        """Perform a complete render of the maze scene.

        Draws all visual elements in the correct order: 42 path markers,
        maze walls, the image buffer, and finally the player sprite.
        """
        draw_42(mz)
        draw_maze(mz, wall_color, False)
        mlx1.mlx_put_image_to_window(k, win, img, 0, 0)
        player(pl_x, pl_y)

    render()
    prev_x = 0
    prev_y = 0

    def regenerate_maze() -> Any:
        """Generate and display a new maze, resetting the player position.

        Creates a new maze using the same parameters as the original,
        animates the transition by erasing the old maze and drawing the new
        one, and resets the player to the entry point.
        """
        nonlocal pl_x, pl_y
        pl_x = ENTRY[0] * 40 + 10
        pl_y = ENTRY[1] * 40 + 10
        nonlocal mz
        maze = MazeGenerator(width, length, ENTRY, EXIT, output_file)
        if seed:
            random.seed(1)
        try:
            if not is_perfect:
                maze.creat_maze_prims_algo()
            else:
                maze.creat_maze_bakctracker_algo()
            maze.creat_output_file(pathfinder(maze.maze, ENTRY, EXIT, width,
                                              length))
        except InvalidDistinationFor42Path as e:
            print(e)
            if not is_perfect:
                maze.remove_walls_prims_algo()
            else:
                maze.remove_walls_backtracker_algo()
            maze.creat_output_file(pathfinder(maze.maze, ENTRY, EXIT, width,
                                              length))
        except InvalidEntryExitPoint as e:
            print(f"Error: {e}")
            sys.exit()

        new_maze = maze.maze
        back_img()
        back_img()
        draw_maze(mz, 0x000000, True)
        draw_maze(new_maze, wall_color, True)
        mlx1.mlx_put_image_to_window(
            k, win, path_start_img, ENTRY[0] * 40 + 10, ENTRY[1] * 40 + 10)
        mlx1.mlx_put_image_to_window(
            k, win, path_end_img, EXIT[0] * 40 + 10, EXIT[1] * 40 + 10)
        mz = new_maze

    def on_key(keycode: Any, param: Any) -> Any:
        """Handle keyboard input events for player interaction.

        Processes key presses to control player movement, maze regeneration,
        path visualization, and other interactive features.

        Args:
            keycode: The integer keycode of the pressed key.
            param: Additional parameter passed by MLX (unused).

        Key Bindings:
            - 65307 (ESC): Exit the application
            - 65362 (Up Arrow): Move player north
            - 65364 (Down Arrow): Move player south
            - 65361 (Left Arrow): Move player west
            - 65363 (Right Arrow): Move player east
            - 99 (C): Change wall color randomly
            - 112 (P): Show solution path
            - 103 (G): Generate new maze
            - 104 (H): Hide path and refresh display
        """
        nonlocal pl_x, pl_y, wall_color, prev_x, prev_y
        prev_x = pl_x
        prev_y = pl_y
        is_moved = False

        if keycode == 65307:
            mlx1.mlx_loop_exit(k)

        if keycode == 99:
            wall_color = random.choice(colors)
            draw_maze(mz, wall_color, True)

        if keycode == 65364 and mz[pl_y // 40][pl_x // 40].south is False:
            is_moved = True
            pl_y += 40

        elif keycode == 65362 and mz[pl_y // 40][pl_x // 40].north is False:
            is_moved = True
            pl_y -= 40

        elif keycode == 65363 and mz[pl_y // 40][pl_x // 40].east is False:
            is_moved = True
            pl_x += 40

        elif keycode == 65361 and mz[pl_y // 40][pl_x // 40].west is False:
            is_moved = True
            pl_x -= 40

        if is_moved is True:
            if (pl_x, pl_y) == (EXIT[0] * 40 + 10, EXIT[1] * 40 + 10):
                mlx1.mlx_loop_exit(k)
            mlx1.mlx_put_image_to_window(
                k, win, bg_img, prev_x - 10, prev_y - 10)
            mlx1.mlx_put_image_to_window(k, win, bg_img, pl_x - 10, pl_y - 10)
            mlx1.mlx_put_image_to_window(
                k, win, path_start_img, ENTRY[0] * 40 + 10, ENTRY[1] * 40 + 10)

        if keycode == 112:
            back_img()
            back_img()
            mlx1.mlx_put_image_to_window(
                k, win, path_start_img, ENTRY[0] * 40 + 10, ENTRY[1] * 40 + 10)
            mlx1.mlx_put_image_to_window(
                k, win, path_end_img, EXIT[0] * 40 + 10, EXIT[1] * 40 + 10)
            player(pl_x, pl_y)
            draw_path()

        if keycode == 103:
            regenerate_maze()

        if keycode == 104:
            back_img()
            back_img()
            mlx1.mlx_put_image_to_window(
                k, win, path_start_img, ENTRY[0] * 40 + 10, ENTRY[1] * 40 + 10)
            mlx1.mlx_put_image_to_window(
                k, win, path_end_img, EXIT[0] * 40 + 10, EXIT[1] * 40 + 10)
            player(pl_x, pl_y)

        render()

    mlx1.mlx_key_hook(win, on_key, None)
    mlx1.mlx_loop(k)
