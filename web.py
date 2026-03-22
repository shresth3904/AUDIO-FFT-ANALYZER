import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import io
from scipy.fft import fft, fftfreq
from scipy.signal import butter, filtfilt


@st.cache_data
def generate_demo_audio(sample_rate=44100, duration=6.0):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    freq_low = 440.0   
    freq_high = 3000.0   

    wave_low = np.sin(2 * np.pi * freq_low * t)
    wave_high = np.sin(2 * np.pi * freq_high * t)
    wave_mid =np.sin(2* np.pi * 1000.0 * t)

    mixed_signal = wave_low*0.5

    for i in range(len(t)):
        if ((i // 100)%4 == 1):
            mixed_signal[i] += 0.25*wave_high[i]
        if ((i // 10000)%4 == 1):
            mixed_signal[i] += 0.25*wave_mid[i]
        elif ((i // 10000)%4 == 3):
            mixed_signal[i] += 0.25*wave_mid[i]
    return mixed_signal, sample_rate


@st.cache_data
def fast_ft(waveform, sample_rate):
    N = len(waveform)
    fft_complex = fft(waveform)
    fft_magnitude = np.abs(fft_complex) / N
    frequencies = fftfreq(N, 1/sample_rate)
    return fft_magnitude[:N//2], frequencies[:N//2]

def universal_filter(waveform, filter_type, cutoffs, sample_rate):
    nyquist = sample_rate / 2.0
    
    if isinstance(cutoffs, list) or isinstance(cutoffs, tuple):
        Wn = [c / nyquist for c in cutoffs]
    else:
        Wn = cutoffs / nyquist
        
    btype_map = {
        "Low Pass": "lowpass",
        "High Pass": "highpass",
        "Band Pass": "bandpass",
        "Band Reject": "bandstop"
    }
    
    b, a = butter(4, Wn, btype=btype_map[filter_type])
    return filtfilt(b, a, waveform)

def array_to_bytes(audio_array, sample_rate):
    buffer = io.BytesIO()
    sf.write(buffer, audio_array, sample_rate, format='WAV')
    buffer.seek(0)
    return buffer


st.set_page_config(page_title="Universal DSP Equalizer", layout="wide")
st.title("Universal DSP Audio Equalizer")

st.sidebar.header("1. Audio Source")

use_demo = st.sidebar.checkbox("Load Synthetic Demo Audio (440Hz + 3000Hz)", value=True)
uploaded_file = st.sidebar.file_uploader("OR Upload a custom WAV file", type=["wav"])

waveform = None
sampling_rate = None

if uploaded_file is not None:
    waveform, sampling_rate = sf.read(uploaded_file)
    if len(waveform.shape) == 2:
        waveform = np.mean(waveform, axis=1)
elif use_demo:
    waveform, sampling_rate = generate_demo_audio()
    
if waveform is not None:
    N = len(waveform)
    duration = N / sampling_rate
    time = np.linspace(0, duration, N)
    nyquist_limit = int(sampling_rate / 2.0) - 1

    st.sidebar.header("2. Filters")
    filter_choice = st.sidebar.selectbox(
        "Select Filter", 
        ["Low Pass", "High Pass", "Band Pass", "Band Reject"]
    )

    if filter_choice in ["Low Pass", "High Pass"]:
        st.sidebar.subheader(f"{filter_choice} Cutoff (Hz)")
        cutoff = st.sidebar.slider(
            "Frequency", 
            min_value=20, max_value=nyquist_limit, value=min(1350, nyquist_limit), step=10
        )
        cutoffs_to_pass = cutoff
        plot_title_hz = f"Cutoff: {cutoff} Hz"
    else:
        st.sidebar.subheader(f"{filter_choice} Boundaries (Hz)")
        cutoffs = st.sidebar.slider(
            "Frequency Range", 
            min_value=20, max_value=nyquist_limit, value=(min(500, nyquist_limit), min(3000, nyquist_limit)), step=10
        )
        cutoffs_to_pass = list(cutoffs)
        plot_title_hz = f"Range: {cutoffs[0]} Hz - {cutoffs[1]} Hz"

    original_mag, original_freq = fast_ft(waveform, sampling_rate)
    filtered_audio = universal_filter(waveform, filter_choice, cutoffs_to_pass, sampling_rate)
    filtered_mag, filtered_freq = fast_ft(filtered_audio, sampling_rate)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Audio")
        st.audio(array_to_bytes(waveform, sampling_rate), format="audio/wav")
    with col2:
        st.subheader(f"Filtered Audio ({filter_choice})")
        st.audio(array_to_bytes(filtered_audio, sampling_rate), format="audio/wav")

    st.subheader("Signal Physics")
    fig, axs = plt.subplots(4, 2, figsize=(14, 12))

    axs[0][0].plot(original_freq, original_mag, color="red")
    axs[0][0].set_title("Original Frequency Spectrum")
    axs[0][0].set_xlim(0, min(8000, nyquist_limit))

    axs[0][1].plot(time[:1000], waveform[:1000], color="blue")
    axs[0][1].set_title("Original Waveform (Microscopic View)")

    axs[1][0].plot(filtered_freq, filtered_mag, color="purple")
    axs[1][0].set_title(f"{filter_choice} Spectrum ({plot_title_hz})")
    axs[1][0].set_xlim(0, min(8000, nyquist_limit))

    axs[1][1].plot(time[:1000], filtered_audio[:1000], color="green")
    axs[1][1].set_title("Filtered Waveform (Microscopic View)")
    
    axs[2][0].plot(time, waveform, color="blue")
    axs[2][0].set_title("Original Waveform (FULL)")
    
    axs[2][1].plot(time, filtered_audio, color="green")
    axs[2][1].set_title("Filtered Waveform (FULL)")

    axs[3][0].specgram(waveform + 1e-10, Fs=sampling_rate, NFFT=1024, cmap='magma')
    axs[3][0].set_title("Original Spectrogram")
    axs[3][0].set_ylabel("Frequency (Hz)")
    axs[3][0].set_xlabel("Time (sec)")
    axs[3][0].set_ylim(0, min(8000, nyquist_limit))

    axs[3][1].specgram(filtered_audio + 1e-10, Fs=sampling_rate, NFFT=1024, cmap='magma')
    axs[3][1].set_title("Filtered Spectrogram")
    axs[3][1].set_xlabel("Time (sec)")
    axs[3][1].set_ylim(0, min(8000, nyquist_limit))

    plt.tight_layout()
    st.pyplot(fig)

else:
    st.info("Awaiting audio input. Upload a WAV file or enable the Demo Audio.")
