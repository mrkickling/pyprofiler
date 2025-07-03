"""Classes related to terminal output"""
from __future__ import annotations
from enum import Enum


class Color(Enum):
    """Used in terminal to set colored fonts"""
    GREEN, RED, WHITE = '\033[92m', '\033[91m', '\033[0m'
    OFF = '\x1b[0m'

def text_in_color(text, color):
    """Return text string in a given color"""
    return color.value + text + Color.OFF.value
