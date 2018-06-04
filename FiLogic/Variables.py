# Made by: Jacob Meadows
# Started on March 8th, 2018
"""
Variable file for [PROJECT NAME].
"""
import ctypes
import pygame


pygame.font.init()

colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255)
}
user32 = ctypes.windll.user32
monitor_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
tnr_30 = pygame.font.SysFont("Times New Roman", 30)
tnr_20 = pygame.font.SysFont("Times New Roman", 20)
