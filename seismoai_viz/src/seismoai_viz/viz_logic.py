import matplotlib.pyplot as plt
import numpy as np


def plot_gather(traces, title="Seismic Shot Gather", show=True):
    """
    Plot all traces as a 2D image (samples × trace index).

    Parameters
    ----------
    traces : ndarray
        Shape (n_traces, n_samples).
    title : str
        Plot title.
    show : bool
        If True, display the figure. If False, close it (for tests/headless).
    """
    plt.figure(figsize=(10, 8))
    plt.imshow(traces.T, cmap="RdBu", aspect="auto")
    plt.colorbar(label="Amplitude")
    plt.title(title)
    plt.xlabel("Trace index")
    plt.ylabel("Sample index")
    if show:
        plt.show()
    else:
        plt.close()


def plot_trace(traces, trace_index=80, show=True):
    """
    Plot one trace as a 1D waveform.

    Parameters
    ----------
    traces : ndarray
        Shape (n_traces, n_samples).
    trace_index : int
        Which trace to plot.
    show : bool
        If True, display the figure. If False, close it (for tests/headless).
    """
    plt.figure(figsize=(12, 4))
    plt.plot(traces[trace_index], color="black", lw=0.5)
    plt.title(f"Trace {trace_index} waveform")
    plt.xlabel("Sample index")
    plt.ylabel("Amplitude")
    plt.grid(True)
    if show:
        plt.show()
    else:
        plt.close()


def show_spectrum(trace, dt=0.001, show=True):
    """
    Plot the magnitude spectrum of a single trace (FFT).

    Parameters
    ----------
    trace : ndarray
        1D array of samples.
    dt : float
        Sample interval in seconds (default 1 ms).
    show : bool
        If True, display the figure. If False, close it (for tests/headless).
    """
    fft_vals = np.abs(np.fft.rfft(trace))
    freqs = np.fft.rfftfreq(len(trace), d=dt)

    plt.figure(figsize=(10, 4))
    plt.plot(freqs, fft_vals)
    plt.title("Frequency spectrum (Hz)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, 150)
    if show:
        plt.show()
    else:
        plt.close()
