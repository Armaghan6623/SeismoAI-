# seismoai-viz

`seismoai-viz` provides plotting utilities for seismic trace arrays.

## Functions

- `plot_gather(traces, title="Seismic Shot Gather", show=True)`:
  plot all traces as a 2D gather image.
- `plot_trace(traces, trace_index=80, show=True)`:
  plot one trace as a waveform.
- `show_spectrum(trace, dt=0.001, show=True)`:
  plot FFT magnitude spectrum for one trace.

Use `show=False` during automated tests or headless runs.
