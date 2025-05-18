import pygame

def draw_gradient(screen, bass_level, width, height):
    #Normalize bass level to 0-255 range
    color_intensity = min(255, int(bass_level * 10))
    gradient_color = (255,100,color_intensity)

    screen.fill(gradient_color)