import os
import time
import yt_dlp
from pydub import AudioSegment
import numpy as np
import pygame

from analyzer_cpu import compute_bass_energy
from visualizer import draw_gradient

CHUNK_MS = 50  # simulate 20 FPS (50ms per frame)

# === STEP 1: Download & Convert YouTube Audio ===
def download_audio(youtube_url, output_path='output.wav'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio...")
        ydl.download([youtube_url])
    
    print("Converting to WAV...")
    audio = AudioSegment.from_mp3('temp_audio.mp3')
    audio.export(output_path, format='wav')
    os.remove('temp_audio.mp3')
    print("Conversion done!")

# === STEP 2: Simulate Real-Time Bass Visualization ===
def simulate_visualizer(wav_path):
    # Load audio
    audio = AudioSegment.from_wav(wav_path)
    samples = np.array(audio.get_array_of_samples())
    rate = audio.frame_rate
    chunk_size = int(rate * (CHUNK_MS / 1000.0))

    # Init Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Bass Bloom Visualizer")
    clock = pygame.time.Clock()

    # Frame simulation
    for i in range(0, len(samples), chunk_size):
        chunk = samples[i:i+chunk_size].astype(np.int16).tobytes()
        bass = compute_bass_energy(chunk, rate)

        draw_gradient(screen, bass, 800, 600)
        pygame.display.flip()
        clock.tick(1000 // CHUNK_MS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

    pygame.quit()

# === MAIN FLOW ===
if __name__ == "__main__":
    url = input("Paste a YouTube link: ").strip()
    wav_file = "converted_output.wav"

    download_audio(url, wav_file)
    simulate_visualizer(wav_file)