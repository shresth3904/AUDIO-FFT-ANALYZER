# Interactive DSP Audio Equalizer & Analyzer

A full-stack, real-time Digital Signal Processing (DSP) web portal built with Python. Upload raw audio, apply professional-grade infinite impulse response (IIR) filters, and mathematically analyze acoustic physics through frequency spectrums and time-frequency spectrograms.

**Built with:** Python | SciPy | NumPy | Streamlit

---

## Overview

This application provides a powerful suite of signal processing tools wrapped in an intuitive web interface. It combines advanced mathematical algorithms with real-time audio visualization to enable professional-grade audio analysis and manipulation.

### Key Features

- **Real-time Audio Processing** — Upload and process audio files instantly
- **Frequency Analysis** — Generate 1D frequency spectrums via Fast Fourier Transform
- **Time-Frequency Analysis** — Visualize audio evolution with spectrograms
- **Professional Filtering** — Apply Butterworth IIR filters (low-pass, high-pass, band-pass, notch)
- **Web-Based Interface** — Access via Streamlit with concurrent user support

---

## Mathematical Foundations

This application is built on three fundamental pillars of signal processing.

### 1. The Fast Fourier Transform (FFT)

An audio file is essentially a 1D array of pressure values over time (the Time Domain). While useful for playback, it is mathematically useless for analyzing pitch or tuning.

The **Fast Fourier Transform** is an algorithm that computes the Discrete Fourier Transform (DFT) in $O(N \log N)$ time. It mathematically decomposes a complex audio wave into its constituent pure sine waves (frequencies).

The DFT is defined by:

$$X_k = \sum_{n=0}^{N-1} x_n e^{-i 2\pi k n / N}$$

In this portal, the FFT generates the **1D Frequency Spectrum**, showing the exact amplitude of every frequency present in the entire audio file. However, standard FFTs are temporally blind—they average the entire file into a single static snapshot.

### 2. The Short-Time Fourier Transform (STFT) & Spectrograms

To analyze how frequencies evolve over time (e.g., spoken words or percussive impacts), we use the **Short-Time Fourier Transform (STFT)**.

Instead of running one massive FFT on millions of samples, the STFT slices the audio into microscopic, overlapping windows (e.g., 1024 samples). It calculates the FFT for each window and stacks results side-by-side to create a 2D matrix.

This matrix is rendered as a **Spectrogram**—a heat map where:

- **X-Axis:** Time (Seconds)
- **Y-Axis:** Frequency (Hertz)
- **Color Intensity:** Logarithmic amplitude (Decibels)

This visualization is critical for distinguishing harmonic energy (horizontal lines, like human voice) from percussive transients (vertical broadband spikes, like impact sounds).

### 3. Butterworth IIR Filters

To manipulate audio, this engine uses **Butterworth filters**. In DSP, filter design involves trade-offs between roll-off steepness and phase distortion.

The Butterworth topology is chosen for its **maximally flat magnitude response** in the passband. Unlike Chebyshev or Elliptic filters, Butterworth filters introduce no mathematical ripple or resonant ringing into surviving frequencies.

The squared frequency response of an $n$-th order Butterworth low-pass filter is:

$$|H(j\omega)|^2 = \frac{1}{1 + (\omega / \omega_c)^{2n}}$$

#### Supported Filter Types

- **Low Pass** — Removes high frequencies (treble); passes bass
- **High Pass** — Removes low frequencies (bass/rumble); passes treble
- **Band Pass** — Isolates a specific frequency window; removes everything outside
- **Band Reject (Notch)** — Targets and attenuates a specific frequency window; preserves surrounding audio

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or conda package manager

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd project\ FFT
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Local Execution

Run the application on your local machine:

```bash
python -m streamlit run web.py
```

The application will open in your default browser at `http://localhost:8501`.

### Deployment

This portal is designed for cloud deployment (Streamlit Community Cloud, Docker containers, etc.).

**Note:** The architecture requires C-libraries for audio processing. Two package manifests are provided:

- **requirements.txt** — Python dependencies (numpy, scipy, matplotlib, streamlit, soundfile)
- **packages.txt** — Linux/Debian OS dependencies (libsndfile1 via apt-get)

---

## Project Structure

```
project FFT/
├── app.py              # (Available—describe purpose)
├── web.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── packages.txt        # System dependencies (for deployment)
└── readme.md          # This file
```

---

## Dependencies

| Package  | Purpose                                    |
|----------|-------------------------------------------|
| numpy    | Numerical computing and array operations |
| scipy    | Scientific computing (signal processing) |
| matplotlib | Data visualization                    |
| streamlit | Web UI framework                         |
| soundfile | Audio file I/O                          |

---

