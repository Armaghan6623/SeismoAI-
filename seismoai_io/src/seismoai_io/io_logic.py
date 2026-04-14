import os

import numpy as np
import pandas as pd
import segyio

_TEXT_HEADER_BYTES = 3200
_BINARY_HEADER_BYTES = 400
_TRACE_HEADER_BYTES = 240


def _be_i16(buf: bytes, offset: int) -> int:
    return int.from_bytes(buf[offset : offset + 2], byteorder="big", signed=True)


def _be_i32(buf: bytes, offset: int) -> int:
    return int.from_bytes(buf[offset : offset + 4], byteorder="big", signed=True)


def _le_i16(buf: bytes, offset: int) -> int:
    return int.from_bytes(buf[offset : offset + 2], byteorder="little", signed=True)


def _le_i32(buf: bytes, offset: int) -> int:
    return int.from_bytes(buf[offset : offset + 4], byteorder="little", signed=True)


def _infer_binary_header_layout(binary_header: bytes) -> tuple[int, int, str]:
    """
    Infer sample count, sample format code, and byte order from the SEG-Y binary header.
    """
    valid_codes = {1, 2, 3, 5, 8}

    candidates = []
    for byteorder in ("big", "little"):
        i16 = _be_i16 if byteorder == "big" else _le_i16
        ns_21 = i16(binary_header, 20)  # bytes 21-22
        fc_25 = i16(binary_header, 24)  # bytes 25-26
        ns_69 = i16(binary_header, 68)  # bytes 69-70 (rev2 override)
        fc_89 = i16(binary_header, 88)  # bytes 89-90 (rev2 override)

        num_samples = ns_69 if ns_69 > 0 else ns_21
        format_code = fc_89 if fc_89 in valid_codes else fc_25

        score = 0
        if 1 <= num_samples <= 50000:
            score += 2
        if format_code in valid_codes:
            score += 2
        if 1 <= ns_21 <= 50000:
            score += 1
        if fc_25 in valid_codes:
            score += 1

        candidates.append((score, num_samples, format_code, byteorder))

    best = max(candidates, key=lambda x: x[0])
    _, num_samples, sample_format_code, byteorder = best
    if num_samples <= 0:
        raise RuntimeError("Could not infer a valid samples-per-trace from binary header.")
    if sample_format_code not in valid_codes:
        raise RuntimeError("Could not infer a supported SEG-Y sample format code.")
    return num_samples, sample_format_code, byteorder


def _ibm_to_ieee_f32(ibm_words: np.ndarray) -> np.ndarray:
    """
    Convert IBM 32-bit float words (SEG-Y format code 1) to IEEE float32.
    """
    ibm_words = ibm_words.astype(np.uint32, copy=False)
    if ibm_words.size == 0:
        return np.array([], dtype=np.float32)

    sign = (ibm_words >> 31) & 0x1
    exponent = (ibm_words >> 24) & 0x7F
    fraction = ibm_words & 0x00FFFFFF

    out = np.zeros_like(ibm_words, dtype=np.float64)
    nonzero = fraction != 0
    if np.any(nonzero):
        mantissa = fraction[nonzero].astype(np.float64) / float(1 << 24)
        power = (exponent[nonzero].astype(np.int32) - 64) * 4
        out[nonzero] = mantissa * np.power(16.0, power)

    out = out.astype(np.float32)
    out[sign == 1] *= -1.0
    return out


def _load_single_sgy_fallback(file_path: str) -> tuple[np.ndarray, pd.DataFrame]:
    """
    Minimal raw SEG-Y loader used when segyio cannot open the file due to
    size/trace-count inconsistencies.
    """
    with open(file_path, "rb") as f:
        f.seek(_TEXT_HEADER_BYTES, os.SEEK_SET)
        binary_header = f.read(_BINARY_HEADER_BYTES)
        if len(binary_header) != _BINARY_HEADER_BYTES:
            raise RuntimeError("SEG-Y binary header is missing or truncated.")

        num_samples, sample_format_code, byteorder = _infer_binary_header_layout(binary_header)
        i32 = _be_i32 if byteorder == "big" else _le_i32

        if sample_format_code == 1:  # IBM float32
            bytes_per_sample = 4
            dtype = np.dtype(">u4" if byteorder == "big" else "<u4")
        elif sample_format_code == 5:  # IEEE float32
            bytes_per_sample = 4
            dtype = np.dtype(">f4" if byteorder == "big" else "<f4")
        elif sample_format_code == 2:  # int32
            bytes_per_sample = 4
            dtype = np.dtype(">i4" if byteorder == "big" else "<i4")
        elif sample_format_code == 3:  # int16
            bytes_per_sample = 2
            dtype = np.dtype(">i2" if byteorder == "big" else "<i2")
        elif sample_format_code == 8:  # int8
            bytes_per_sample = 1
            dtype = np.dtype("i1")
        else:
            raise RuntimeError(f"Unsupported SEG-Y sample format code: {sample_format_code}")

        traces_list: list[np.ndarray] = []
        headers_list: list[dict] = []

        while True:
            trace_header = f.read(_TRACE_HEADER_BYTES)
            if not trace_header or len(trace_header) != _TRACE_HEADER_BYTES:
                break

            sample_bytes = f.read(num_samples * bytes_per_sample)
            if len(sample_bytes) != num_samples * bytes_per_sample:
                break

            samples = np.frombuffer(sample_bytes, dtype=dtype)
            if sample_format_code == 1:
                samples = _ibm_to_ieee_f32(samples)
            else:
                samples = samples.astype(np.float32, copy=False)

            traces_list.append(samples)
            headers_list.append(
                {
                    "trace_sequence_line": i32(trace_header, 0),
                    "cdp": i32(trace_header, 20),
                    "offset": i32(trace_header, 36),
                    "source_x": i32(trace_header, 72),
                    "source_y": i32(trace_header, 76),
                    "group_x": i32(trace_header, 80),
                    "group_y": i32(trace_header, 84),
                    "num_samples": num_samples,
                    "sample_format_code": sample_format_code,
                    "byte_order": byteorder,
                }
            )

        if not traces_list:
            raise RuntimeError("No traces could be read from the SEG-Y file.")

        traces = np.stack(traces_list, axis=0)
        headers = pd.DataFrame(headers_list)
        return traces, headers

def load_single_sgy(file_path):
    """
    Load a single SEG-Y file and return its trace samples and headers.
    """
    try:
        with segyio.open(file_path, ignore_geometry=True, strict=False) as sgy_file:
            sgy_file.mmap()
            traces = segyio.tools.collect(sgy_file.trace[:])
            headers = pd.DataFrame(dict(header) for header in sgy_file.header[:])
        return traces, headers
    except RuntimeError:
        return _load_single_sgy_fallback(file_path)

def load_folder(folder_path):
    """Load every `.sgy` file in a directory into a filename-keyed mapping."""
    files = sorted(
        file_name for file_name in os.listdir(folder_path) if file_name.lower().endswith(".sgy")
    )
    return {f: load_single_sgy(os.path.join(folder_path, f)) for f in files}

def normalize_traces(traces):
    """
    Scale trace amplitudes to the range [-1, 1] using max-absolute normalization.
    """
    max_val = np.max(np.abs(traces))
    if max_val == 0:
        return traces
    return traces / max_val