import os
from seismoai_io.io_logic import load_single_sgy

# We point to the EXACT filename from your 'ls data' command
file_name = "100_1511555540_30100_63700_20171127_150424_100.sgy"
file_path = os.path.join("data", file_name)

print(f"🚀 Attempting to load: {file_path}")

if os.path.exists(file_path):
    traces, headers = load_single_sgy(file_path)
    print("✅ SUCCESS!")
    print(f"Shape of Traces: {traces.shape}")
    print(f"Number of Headers: {len(headers)}")
else:
    print(f"❌ FAILED: The file {file_path} still can't be found.")