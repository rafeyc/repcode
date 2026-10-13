import numpy as np

# Majority vote decoder - "cheats" by looking directly at the qubits. Returns array of successful and failed error corrections.
def majority_vote(errors):
    distance = errors.shape[1]
    one_count = errors.sum(axis=1)
    failed = one_count > distance / 2
    return failed