# SeismoAI

Modular Python packages for loading, visualizing, quality-checking, modeling, and explaining decisions on real **SEG-Y** seismic data (Forge 2D Survey, 2017). Each module is a separate installable package; together they form an end-to-end pipeline.

## Requirements

- **Python** 3.9 or newer  
- **Dataset**: `.sgy` files placed under `data/` (not committed if large; see `.gitignore`)

## Repository layout

| Path | Role |
|------|------|
| `data/` | Local `.sgy` files for development and demos |
| `seismoai_io/` | Load and normalize SEG-Y traces |
| `seismoai_viz/` | Plot gathers, traces, and spectra |
| `seismoai_qc/` | QC labels and reports *(if present)* |
| `seismoai_model/` | Training and prediction *(if present)* |
| `seismoai_xai/` | Explainability *(if present)* |

## Install (local development)

The **usable** packages are **`seismoai_io`** and **`seismoai_viz`**. Install each from its own folder (below).

You *can* run `python -m pip install -e .` at the **repository root**; that only installs a tiny placeholder package (`seismoai-workspace`) so pip stops erroring. It does **not** install `seismoai_io` or `seismoai_viz`. You still need:

```powershell
python -m pip install -e .\seismoai_io
python -m pip install -e .\seismoai_viz
```

(Use quotes around paths if needed.)

**Module 1 — I/O**

```powershell
cd "path\to\SeismoAI_Project\seismoai_io"
python -m pip install -e .
```

**Module 2 — visualization** (optional: pull in I/O from PyPI once published)

```powershell
cd "path\to\SeismoAI_Project\seismoai_viz"
python -m pip install -e .
# Optional extra after both packages are on PyPI:
# python -m pip install -e ".[io]"
```

## Install from PyPI (after publishing)

Replace with your published names when available:

```bash
pip install seismoai-io
pip install seismoai-viz
```

## Quick start

**Load and inspect one file** (adjust filename to match your `data/` folder):

```python
from seismoai_io.io_logic import load_single_sgy, normalize_traces

traces, headers = load_single_sgy("data/your_file.sgy")
traces = normalize_traces(traces)
print(traces.shape, headers.shape)
```

**Plot** (requires `seismoai-viz` installed):

```python
from seismoai_viz.viz_logic import plot_gather, plot_trace, show_spectrum

plot_gather(traces)
plot_trace(traces, trace_index=0)
show_spectrum(traces[0], dt=0.001)
```

A small script `check_data.py` at the repo root can be used to verify loading for a fixed filename.

## Tests

Install **pytest** if needed: `python -m pip install pytest`

**From the repository root** (recommended — uses `pytest.ini`):

```powershell
cd "path\to\SeismoAI_Project"
python -m pytest
```

**Per package** (optional):

```powershell
cd seismoai_io
python -m pytest

cd ..\seismoai_viz
python -m pytest
```

If you accidentally copied visualization tests into `seismoai_io\test_viz.py`, remove that file so only `seismoai_viz\tests\` contains viz tests.

## Module API summary

### `seismoai-io`

- `load_single_sgy(path)` — traces array and header table  
- `load_folder(path)` — dict of filename → `(traces, headers)`  
- `normalize_traces(traces)` — scale amplitudes to approximately `[-1, 1]`

### `seismoai-viz`

- `plot_gather(traces, title=..., show=True)` — 2D gather image  
- `plot_trace(traces, trace_index=..., show=True)` — single trace waveform  
- `show_spectrum(trace, dt=0.001, show=True)` — magnitude spectrum  

Use `show=False` for headless or automated runs.

## Authors

<!-- Add both student names and GitHub handles before submission. -->

## License

<!-- Add if your course requires one. -->
