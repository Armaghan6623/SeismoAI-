import segyio
import numpy as np
import os

def load_single_sgy(file_path):
    """
    Loads a single .sgy file and returns traces as a numpy array.
    Expects (167, 4001) based on Forge 2D Survey specs.
    """
    with segyio.open(file_path, ignore_geometry=True, strict=False) as f:
        # Using collect is often faster for segyio
        traces = segyio.tools.collect(f.trace[:]) 
    return traces

def load_folder(folder_path):
    """
    Scans a directory for .sgy files and loads them into a list of arrays.
    """
    all_data = []
    for file in os.listdir(folder_path):
        if file.endswith(".sgy"):
            full_path = os.path.join(folder_path, file)
            all_data.append(load_single_sgy(full_path))
    return all_data

def normalize_traces(traces):
    """
    Scales amplitudes to [-1, 1] to handle outliers (like 758 vs +/- 10).
    """
    max_amp = np.max(np.abs(traces))
    if max_amp == 0:
        return traces
    return traces / max_amp