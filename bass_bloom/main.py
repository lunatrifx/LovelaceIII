import os
import time
from pydub import AudioSegment
import numpy as np
import pygame
import random
from utils import is_cuda_available, is_cloud_environment

from analyzer_cpu import compute_bass_energy
from visualizer import draw_gradient_by_theme

CHUNK_MS = 50  # 20 FPS
WIDTH, HEIGHT = 800, 600

# === Get audio file and name ===
print("\n🎵 Drop a .mp3 or .wav file into your project directory.")
filename = input("Enter filename (with extension): ").strip()
name = input("Enter your name: ").strip()

# === Convert to WAV if needed ===
if filename.endswith(".mp3"):
    print("Converting MP3 to WAV...")
    audio = AudioSegment.from_mp3(filename)
    filename = "converted_temp.wav"
    audio.export(filename, format="wav")
else:
    audio = AudioSegment.from_wav(filename)

# === Theme detection ===
def get_theme_color(name):
    if name.lower() == "nvidia":
        return "green"
    elif name.lower() == "Gaby":
        return "pink"
    else:
        return "random"

theme = get_theme_color(name)

# === Load audio and simulate ===
samples = np.array(audio.get_array_of_samples())
rate = audio.frame_rate
chunk_size = int(rate * (CHUNK_MS / 1000.0))

# === Visual Setup ===
if is_cloud_environment():
    print("🌩️ Detected cloud environment: disabling audio.")
    print("Visualizer will run without audio.")
    os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
pygame.init()
pygame.mixer.quit()
    
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bass Bloom")
clock = pygame.time.Clock()

# === Loop Through Audio ===
for i in range(0, len(samples), chunk_size):
    chunk = samples[i:i+chunk_size].astype(np.int16).tobytes()
    bass = compute_bass_energy(chunk, rate)

    draw_gradient_by_theme(screen, bass, WIDTH, HEIGHT, theme)
    pygame.display.flip()
    clock.tick(1000 // CHUNK_MS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

pygame.quit()
if os.path.exists("converted_temp.wav"):
    os.remove("converted_temp.wav")