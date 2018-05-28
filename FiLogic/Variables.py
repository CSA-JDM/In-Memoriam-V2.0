# Made by: Jacob Meadows
# Started on March 8th, 2018
"""
Variable file for [PROJECT NAME].
"""
import ctypes


colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255)
}
user32 = ctypes.windll.user32
monitor_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)