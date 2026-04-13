import matplotlib.pyplot as plt
import numpy as np

def plot_gather(traces, title="Seismic Shot Gather"):
    """
    Plots all 167 traces as a 2D image.
    Uses 'RdBu' colormap which is standard for seismic data.
    """
    plt.figure(figsize=(10, 8))
    # aspect='auto' is vital because we have 4001 samples vs 167 traces
    plt.imshow(traces.T, cmap='RdBu', aspect='auto')
    plt.colorbar(label='Amplitude')
    plt.title(title)
    plt.xlabel('Trace Number (0-166)')
    plt.ylabel('Sample Index (0-4000)')
    plt.show()

def plot_trace(traces, trace_index=80):
    """
    Plots a single 1D waveform. 
    This is the best way to see the 758 amplitude spikes.
    """
    plt.figure(figsize=(12, 4))
    plt.plot(traces[trace_index], color='black', lw=0.5)
    plt.title(f"Trace {trace_index} Waveform")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

def show_spectrum(trace, dt=0.001): # dt = 1ms 
    """
    Calculates and plots the frequency content (FFT) of a trace in Hz.
    """
    fft_vals = np.abs(np.fft.rfft(trace))
    freqs = np.fft.rfftfreq(len(trace), d=dt) # Use real-world sample interval
    
    plt.figure(figsize=(10, 4))
    plt.plot(freqs, fft_vals)
    plt.title("Frequency Spectrum (Hz)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, 150) # Most seismic data is in the 0-150Hz range
    plt.show()
    
    plt.figure(figsize=(10, 4))
    plt.plot(freqs, fft_vals)
    plt.title("Frequency Spectrum")
    plt.xlabel("Frequency")
    plt.ylabel("Magnitude")
    plt.show()