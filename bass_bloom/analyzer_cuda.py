import numpy as np 
from numba import cuda


def compute_bass_energy_cuda(data,rate,bass_range=(20,250)):
    audio_data = np.frombuffer(data, dtype=np.int16)

    #placeholder from full GPU FFT, currently CPU FFT only
    fft = np.fft.fft(audio_data)
    freq = np.fft.fftfreq(len(fft), 1/rate)
    mask = (freq >= bass_range[0]) & (freq <= bass_range[1])
    bass_energy = np.abs(fft[mask]).mean()
    return bass_energy 