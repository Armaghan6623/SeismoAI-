import numpy as np
# Point exactly to your logic file
#from seismoai_io.src.seismoai_io.io_logic import normalize_traces
from seismoai_io.io_logic import normalize_traces

def test_normalize():
    # Creating a mock trace with that 758 spike mentioned in the project
    data = np.array([[-10, 0, 758]]) 
    norm = normalize_traces(data)
    
    # Check if the max value is now 1.0
    assert np.max(norm) == 1.0
    print("Normalization test passed!")

if __name__ == "__main__":
    test_normalize()