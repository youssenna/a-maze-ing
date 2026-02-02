"""Custom exception classes for maze generation errors.

This module defines custom exceptions used throughout the maze generation
application to handle specific error conditions.
"""


class ConfigsError(Exception):
    """Raised when configuration file parsing or validation fails.

    This exception is raised for invalid file formats, missing required
    keys, or invalid configuration values.
    """
    pass


class InvalidDistinationFor42Path(Exception):
    """Raised when the 42 path destination is invalid or unreachable.

    This exception indicates that the special 42 path feature cannot
    be completed with the current maze configuration.
    """
    pass


class InvalidCoordinates(Exception):
    """Raised when maze coordinates are invalid or out of bounds.

    This exception is raised for invalid dimensions, window sizes
    exceeding screen resolution, or dimensions below minimum requirements.
    """
    pass


class InvalidEntryExitPoint(Exception):
    """Raised when entry or exit points are invalid.

    This exception is raised when entry or exit coordinates are
    outside the maze boundaries or otherwise invalid.
    """
    pass
