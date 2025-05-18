import pygame
import random

def draw_gradient_by_theme(screen, bass, width, height, theme):
    intensity = min(255, int(bass * 10))

    if theme == "pink":
        color = (255, 100 + intensity // 2, 180 + intensity // 4)
    elif theme == "green":
        color = (50 + intensity // 2, 255, 120)
    else:  # random
        color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )

    screen.fill(color)