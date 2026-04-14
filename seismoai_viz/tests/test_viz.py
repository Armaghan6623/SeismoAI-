import matplotlib

matplotlib.use("Agg")

import numpy as np
import pytest

from seismoai_viz.viz_logic import plot_gather, plot_trace, show_spectrum


@pytest.fixture
def forge_like_traces():
    t = np.linspace(0, 1, 4001)
    trace = np.sin(2 * np.pi * 50 * t) + np.random.default_rng(0).normal(0, 0.1, 4001)
    return np.tile(trace, (167, 1))


def test_plot_gather_runs(forge_like_traces):
    plot_gather(forge_like_traces, title="test", show=False)


def test_plot_trace_runs(forge_like_traces):
    plot_trace(forge_like_traces, trace_index=80, show=False)


def test_show_spectrum_runs(forge_like_traces):
    show_spectrum(forge_like_traces[80], dt=0.001, show=False)
