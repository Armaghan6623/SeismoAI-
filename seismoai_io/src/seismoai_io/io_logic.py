import segyio
import numpy as np
import os

def load_single_sgy(file_path):
    """
    Loads a single .sgy file and extracts traces as a NumPy array.
    Expected shape: (167, 4001). [cite: 8, 12]
    """
    with segyio.open(file_path, ignore_geometry=True) as f:
        traces = segyio.tools.collect(f.trace[:])
    return traces

def load_folder(folder_path):
    """
    Scans a directory for all .sgy files and returns a list of loaded traces. [cite: 24]
    """
    datasets = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".sgy"):
            full_path = os.path.join(folder_path, filename)
            datasets.append(load_single_sgy(full_path))
    return datasets

def normalize_traces(traces):
    """
    Scales trace amplitudes to a range of [-1, 1]. [cite: 24]
    Helps handle high-amplitude noise (e.g., 758 spikes). [cite: 31]
    """
    max_amp = np.max(np.abs(traces))
    if max_amp == 0:
        return traces
    return traces / max_amp