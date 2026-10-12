import numpy as np

def sample_errors(d, p, shots, seed):
    rng = np.random.default_rng(seed)
    error_list = rng.binomial(1, p, size=(shots, d))
    return error_list
