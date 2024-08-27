"""Custom exceptions for conversion to LED matrix format."""

class TooBig(Exception):
    """Raise if image size too large (Must be 12x8)"""

class TooSmall(Exception):
    """Raise if image size too small (Must be 12x8)"""
