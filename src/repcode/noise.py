import numpy as np

# 2D Array representing a list of distance d qubits experiencing bit flip errors
def sample_errors(d, p, shots, seed):
    rng = np.random.default_rng(seed)
    errors = rng.binomial(1, p, size=(shots, d))
    return errors
