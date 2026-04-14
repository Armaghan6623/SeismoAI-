import os

import numpy as np
import pandas as pd

from seismoai_io.io_logic import load_folder, load_single_sgy, normalize_traces


class DummySegyFile:
    def __init__(self, traces, headers):
        self.trace = traces
        self.header = headers
        self.mmap_called = False

    def mmap(self):
        self.mmap_called = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_load_single_sgy_returns_traces_and_headers(monkeypatch):
    traces = np.array([[1.0, -1.0], [0.5, 0.25]])
    headers = [{"cdp": 1, "offset": 10}, {"cdp": 2, "offset": 20}]
    dummy_file = DummySegyFile(traces, headers)

    def fake_open(path, ignore_geometry=True, strict=False, **_kwargs):
        return dummy_file

    monkeypatch.setattr("seismoai_io.io_logic.segyio.open", fake_open)
    monkeypatch.setattr("seismoai_io.io_logic.segyio.tools.collect", lambda data: np.array(data))

    loaded_traces, loaded_headers = load_single_sgy("fake.sgy")

    assert dummy_file.mmap_called is True
    np.testing.assert_array_equal(loaded_traces, traces)
    pd.testing.assert_frame_equal(loaded_headers, pd.DataFrame(headers))


def test_load_folder_loads_only_sgy_files(monkeypatch, tmp_path):
    (tmp_path / "a.sgy").write_text("placeholder", encoding="utf-8")
    (tmp_path / "b.SGY").write_text("placeholder", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("ignore", encoding="utf-8")

    def fake_load_single_sgy(path):
        return f"loaded:{os.path.basename(path)}"

    monkeypatch.setattr("seismoai_io.io_logic.load_single_sgy", fake_load_single_sgy)

    loaded = load_folder(str(tmp_path))

    assert loaded == {
        "a.sgy": "loaded:a.sgy",
        "b.SGY": "loaded:b.SGY",
    }


def test_normalize_traces_scales_by_max_abs_value():
    traces = np.array([[0.0, 758.0, -10.0]])

    normalized = normalize_traces(traces)

    assert np.max(normalized) == 1.0
    assert np.min(normalized) == -10.0 / 758.0