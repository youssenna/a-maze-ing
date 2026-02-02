"""Main entry point for the maze generation and visualization application.

This script loads a configuration file, generates a maze based on the
specified parameters, and launches an interactive visualization using
MiniLibX graphics.

Usage:
    python a_maze_ing.py <config_file>

Args:
    config_file: Path to a .txt or .conf configuration file containing
                maze generation parameters.

Example:
    python a_maze_ing.py config.conf
"""

import sys
from configs.config_parser import parser
from render.render import mlx_render
from utils.errors import InvalidCoordinates, ConfigsError

if len(sys.argv) < 2:
    print("Error: configuration file argument missing")
    sys.exit(1)

file = sys.argv[1]

try:
    configs = parser(file)
    mlx_render(
        configs.get("WIDTH"),
        configs.get("HEIGHT"),
        configs.get("ENTRY"),
        configs.get("EXIT"),
        configs.get("OUTPUT_FILE"),
        configs.get("PERFECT"),
        configs.get("SEED")
    )

except (ModuleNotFoundError, InvalidCoordinates, ConfigsError) as e:
    print(e)
    exit()
