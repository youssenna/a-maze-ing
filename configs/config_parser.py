"""Configuration file parser for maze generation settings.

This module handles parsing and validation of configuration files that define
maze generation parameters including dimensions, entry/exit points, and
generation options.
"""

import sys
from utils import errors
from typing import Any


def parser(file: Any) -> Any:
    """Parse and validate a maze configuration file.

    Reads a configuration file in KEY=VALUE format and validates all
    required parameters for maze generation.

    Args:
        file: Path to the configuration file (.txt or .conf extension).

    Returns:
        A dictionary containing validated configuration values:
            - WIDTH (int): Maze width in cells.
            - HEIGHT (int): Maze height in cells.
            - ENTRY (tuple): Entry point coordinates (x, y).
            - EXIT (tuple): Exit point coordinates (x, y).
            - OUTPUT_FILE (str): Path for the output maze file.
            - PERFECT (bool): Whether to generate a perfect maze.
            - SEED (bool): Whether to use a fixed random seed.

    Raises:
        ConfigsError: If the file format is invalid, required keys are
                     missing, or values fail validation.
        SystemExit: If the file is not found, permission denied, or
                   coordinates are out of bounds.
    """
    if file.endswith(".txt") is False and file.endswith(".conf") is False:
        raise errors.ConfigsError(
            "Error: invalid configuration file "
            "format (expected a .txt or .conf file)"
        )

    def checker_convert(configs: Any) -> Any:
        """Validate and convert configuration values to appropriate types.

        Checks that all required keys are present and converts string values
        to their proper types (integers, booleans, tuples).

        Args:
            configs: Dictionary of raw string configuration values.

        Raises:
            ConfigsError: If validation fails for any configuration value.
        """
        keys = ["WIDTH",
                "HEIGHT",
                "ENTRY",
                "EXIT",
                "OUTPUT_FILE",
                "PERFECT",
                "SEED"
                ]
        for key in keys:
            if key in configs:
                if key in ["WIDTH", "HEIGHT"]:
                    try:
                        configs[key] = int(configs.get(key))
                    except ValueError:
                        raise errors.ConfigsError(
                            f"Error: invalid '{key}' "
                            "value (expected a positive integer)"
                        )
                    if configs[key] <= 0:
                        raise errors.ConfigsError(
                            f"Error: '{key}' must be positive integer"
                        )
                elif key == "PERFECT":
                    if configs["PERFECT"] == "True":
                        configs["PERFECT"] = True
                    elif configs["PERFECT"] == "False":
                        configs["PERFECT"] = False
                    else:
                        raise errors.ConfigsError(
                            f'Error: \'{key}\' must be '
                            'either "True" or "False" (case-sensitive)'
                        )
                elif key == "SEED":
                    if configs["SEED"] == "True":
                        configs["SEED"] = True
                    elif configs["SEED"] == "False":
                        configs["SEED"] = False
                    else:
                        raise errors.ConfigsError(
                            f'Error: \'{key}\' must be either '
                            '"True" or "False" (case-sensitive)'
                        )
                elif key == "OUTPUT_FILE":
                    if configs.get(key).endswith(".txt") is False:
                        raise errors.ConfigsError(
                            "Error: invalid output file "
                            "format (expected a .txt file)"
                        )
                elif key in ["ENTRY", "EXIT"]:
                    if "," in configs.get(key):
                        try:
                            x, y = configs.get(key).split(",")
                            x = int(x)
                            y = int(y)
                            if x < 0 or y < 0:
                                raise errors.ConfigsError(
                                    f"Error: '{key}' coordinates must "
                                    "be non-negative integers"
                                )
                            configs[key] = (x, y)
                        except ValueError:
                            raise errors.ConfigsError(
                                f"Error: invalid '{key}' coordinates format "
                                "(expected exactly two integers: x,y)"
                            )
                    else:
                        raise errors.ConfigsError(
                            f"Error: invalid '{key}' coordinates "
                            "format (expected exactly two integers: x,y)"
                        )
            else:
                raise errors.ConfigsError(
                    f"Error: missing mandatory configuration key: '{key}'"
                )

    def parsing(file_obj: Any, file: str) -> Any:
        """Parse configuration file contents into a dictionary.

        Reads lines from the file, ignoring comments and empty lines,
        and extracts KEY=VALUE pairs.

        Args:
            file_obj: An open file object to read from.
            file: The file path (used for error messages).

        Returns:
            A dictionary of validated configuration values.

        Raises:
            ConfigsError: If line format is invalid or permission denied.
        """
        configs = {}
        try:
            for line in file_obj:
                line = line.rstrip("\n")
                if not line or line[0] == '#':
                    continue
                if "=" not in line or line.count("=") != 1:
                    raise errors.ConfigsError(
                        "Error: invalid configuration line "
                        f"'{line}' (expected KEY=VALUE)"
                    )
                key, value = line.split("=", 1)
                configs.update({key.strip(): value.strip()})
        except PermissionError:
            raise errors.ConfigsError(
                f"Error: Cannot read '{file}'. Permission denied."
            )
        checker_convert(configs)
        return configs

    try:
        with open(file, "r") as f:
            try:
                configs = parsing(f, file)
                if configs["ENTRY"] == configs["EXIT"]:
                    raise errors.ConfigsError(
                        "Error: 'ENTRY' and 'EXIT' cannot be the same cell"
                    )
            except errors.ConfigsError as e:
                print(f"{e}")
                sys.exit(1)
    except FileNotFoundError:
        print(
            f"Error: Configuration file '{file}' not found. "
            "Please check the file path."
        )
        sys.exit(1)
    x_entry, y_entry = configs["ENTRY"]
    x_exit, y_exit = configs["EXIT"]
    if (not (0 <= x_entry < configs["WIDTH"])
       or not (0 <= y_entry < configs["HEIGHT"])):
        print("Error: 'ENTRY' coordinates out of maze bounds")
        sys.exit(1)
    if (not (0 <= x_exit < configs["WIDTH"])
       or not (0 <= y_exit < configs["HEIGHT"])):
        print("Error: 'EXIT' coordinates out of maze bounds")
        sys.exit(1)
    return configs
