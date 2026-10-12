import numpy as np
from repcode.noise import sample_errors

def test_p_zero_gives_all_zeroes():
    zeros = np.zeros((8, 5))
    errors = sample_errors(5, 0, 8, None)
    assert np.array_equal(zeros, errors)

def test_p_one_gives_all_ones():
    ones = np.ones((8, 5))
    errors = sample_errors(5, 1, 8, None)
    assert np.array_equal(ones, errors)

def test_output_shape():
    errors = sample_errors(7, 0.3, 11, None)
    assert errors.shape == (11, 7)

def test_values_are_binary():
    errors = sample_errors(4, 0.5, 8, None)
    assert np.isin(errors, [0,1]).all()

def test_mean_close_to_p():
    errors = sample_errors(5, 0.3, 100_000, None)
    assert abs(errors.mean() - 0.3) < 0.01

def test_same_seed_reproducible():
    a = sample_errors(5, 0.3, 10, 1)
    b = sample_errors(5, 0.3, 10, 1)
    assert np.array_equal(a, b)

def test_diff_seed_different():
    a = sample_errors(5, 0.3, 10, 1)
    b = sample_errors(5, 0.3, 10, 2)
    assert not np.array_equal(a, b)