# seismoai-io

`seismoai-io` provides helper functions for loading and normalizing seismic SEG-Y data.

## Functions

- `load_single_sgy(file_path)`: load one SEG-Y file and return traces plus trace headers.
- `load_folder(folder_path)`: load every `.sgy` file in a folder.
- `normalize_traces(traces)`: scale amplitudes to the range `[-1, 1]`.
