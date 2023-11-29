import numpy as np
import serial
import matplotlib.pyplot as plt
from numpy.fft import fft, ifft, fftshift
import librosa
import librosa.display
from scipy.signal import correlate
import os

plots = lambda rows = 1, cols = 1, size = (20, 10): plt.subplots(rows, cols, figsize = size)
ser = serial.Serial('COM11', 115200, timeout=0)

SAMPLE = 'sample.wav'
fs = 48000
ts = 1/fs
total_samples = fs*1
n = np.arange(total_samples)
audio_sample, sr = librosa.load(SAMPLE, sr=48000)

tiempo = np.arange(total_samples)
datos = np.arange(total_samples)

def plot_waves(waves, sr, start = None, signal_len = None, title = None):
  rows = len(waves)

  # Busca el máximo de cada uno de los arreglos, para después buscar el máximo
  # entre todos los arreglos
  max_y = np.amax([np.amax(wave) for wave in waves])

  _, ax1 = plots(rows)
  ax1 = ax1.flatten()

  for i, wave in enumerate(waves):
    librosa.display.waveshow(wave, sr = sr, ax = ax1[i])
    ax1[i].set_title(title[i], fontsize = 16, fontweight = 'bold')
    ax1[i].set_ylim(-max_y, max_y)
    ax1[i].set_xlim(0, 50)

    if start:
      ax1[i].axvline(start[i]/sr, color = 'r', linestyle = '--')
      ax1[i].axvline(start[i]/sr + signal_len/sr, color = 'g', linestyle = '--')


  plt.tight_layout()
  plt.show()

for i in range(total_samples):
    while True:
        try:
            dato = int(((ser.readline()).decode()).strip())
            print("Ya salí")
            break     
        except ValueError:
            dato = 0
            print("sigo aquí :)")

    datos[i] = dato

ser.close()

plot_waves([datos, audio_sample], sr,
           title = ['SIGNAL MICRO 1', 'SIGNAL SAMPLE'])

"""
_, ax = plots()
ax.plot(n*ts, datos, 'o',label = 'Wacha perro3')
ax.legend()
plt.show()
"""

def find_yes(signal, target_signal):
  corr = correlate(signal, target_signal, mode = 'full')
  start_pos = np.argmax(corr) - len(target_signal) + 1
  return corr, start_pos

corr_ambulancia, start_motor = find_yes(datos, audio_sample)

plot_waves(corr_ambulancia, sr,
           title = 'Correlacion')

# Create the array that would contain only our positive frequency data
#Final = []
#Final2 = []
Final3 = np.arange(total_samples / 2)
print(total_samples/2)
Y3 = np.arange(total_samples)
YS3 = np.arange(total_samples)

# Transform the array in time, so now is in frequency, and we shift it
#Y = fft(y)
#YS = np.abs(fftshift(Y))

#Y2 = fft(y2)
#YS2 = np.abs(fftshift(Y2))

Y3 = fft(datos)
#print(Y3)
YS3 = np.abs(fftshift(Y3))


if len(YS3)%2 == 1:
    freqs = np.arange(0, len(Final3)) +.5
else:
    freqs = np.arange(0, len(Final3))

print(len(freqs))

# Sort the shifted array, so we only have the positive frequencies
for i in n:
    if i < len(n)//2:
        #Final.append(YS[i + len(YS)//2])
        #Final2.append(YS2[i + len(YS2)//2])
        Final3[i] = YS3[i + len(YS3)//2]
        #np.append(Final3, YS3[i + len(YS3)//2])

# Search the maximum value within the signal we are interested and it's corresponding frequency
#print(Final3)
freq = np.argmax(Final3)
Final3[0] = 6

print(freq)

print("The higgest frequency on the signal is: " + str(freq) + " Hz")


_,ax2 = plots()
ax2.plot(freqs, Final3, 'o', label = 'Wacha pt. 2')
ax2.legend()
plt.show()

print(datos)
print(Final3)