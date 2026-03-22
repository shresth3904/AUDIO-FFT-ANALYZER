import librosa, numpy
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq
from scipy.io import wavfile
from scipy.signal import butter, filtfilt, stft, istft, medfilt2d

def br_filter(waveform, upper_limit, lower_limit, sample_rate):
    nyquist = sample_rate / 2.0
    low_cut = lower_limit / nyquist
    high_cut = upper_limit / nyquist

    b, a = butter(5, [low_cut, high_cut], btype='bandstop')

    filtered_audio = filtfilt(b, a, waveform)
    return filtered_audio

def fast_ft(waveform, sample_rate):
    N = len(waveform)
    fft_complex = fft(waveform)
    fft_magnitude = np.abs(fft_complex)/N
    frequencies = fftfreq(N, 1/sampling_rate)
    
    return (fft_magnitude[:N//2], frequencies[:N//2])


audio_file = 'test_.wav'

waveform, sampling_rate = sf.read(audio_file)

if len(waveform.shape) == 2:
    print("Stereo audio detected! Crushing to mono...")
    waveform = np.mean(waveform, axis=1)
    sf.write('mono.wav', waveform, sampling_rate)
    
N = len(waveform)
print(sampling_rate)
print(len(waveform))
time = np.linspace(0, 8, len(waveform))
fft_magnitude, frequencies = fast_ft(waveform, sampling_rate)

freq, t, stft_mat = stft(waveform, fs = sampling_rate, nperseg=1024)

stft_mag = np.abs(stft_mat)
stft_angle = np.angle(stft_mat)

filtered_stft_mag = medfilt2d(stft_mag, kernel_size=(1, 31))
filtered_stft = filtered_stft_mag * np.exp(1j * stft_angle)
_, clean_waveform = istft(filtered_stft, fs = sampling_rate)

clean_waveform = clean_waveform[:N]
sf.write('med_filtered.wav', clean_waveform, sampling_rate)


filtered_audio = clean_waveform #br_filter(waveform, 10000, 9000, sampling_rate)
mag_filtered, freq_filtered = fast_ft(filtered_audio, sampling_rate)

sf.write('filtered.wav', filtered_audio, sampling_rate)



fig, axs = plt.subplots(2, 3, figsize=(10, 10))


axs[0][0].plot(frequencies, fft_magnitude, color="red")
axs[0][0].set_title("Original Frequency Spectrum")
axs[0][0].set_xlim(0, 5000)

axs[0][1].plot(time, waveform, color="blue")
axs[0][1].set_title("Original Waveform")


axs[1][0].plot(time, filtered_audio, color="green")
axs[1][0].set_title("Filtered Waveform")

axs[1][1].plot(freq_filtered, mag_filtered, color="purple")
axs[1][1].set_title("Filtred frequency spectrum")
axs[1][1].set_xlim(0, 6000)

axs[0][2].specgram(waveform, NFFT=2048, Fs=sampling_rate, noverlap=1024, cmap='magma')

# 4. Format the UI
axs[0][2].set_title("Spectrogram: Frequency Content Over Time")
axs[0][2].set_ylim(0, 8000)



plt.specgram(clean_waveform, NFFT = 2048, Fs= sampling_rate, noverlap=1024, cmap = 'magma')
plt.title("Spectrogram: Filtered")
plt.ylabel("Frequency (Hz)")
plt.xlabel("Time (Seconds)")
plt.colorbar(label="Intensity (dB)")

plt.ylim(0, 8000) 

plt.tight_layout()

plt.show()

