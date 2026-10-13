import numpy as np
from repcode.decoders import majority_vote

def test_three_case():
    errors = np.array([[0, 0, 0],
                       [0, 1, 0],
                       [1, 1, 0],
                       [1, 1, 1]])
    expected = np.array([0, 0, 1, 1])
    assert np.array_equal(majority_vote(errors), expected)

def test_five_case():
    errors = np.array([[0, 0, 0, 0, 0],
                       [0, 1, 0, 1, 0],
                       [1, 1, 0, 1, 0],
                       [1, 1, 1, 1, 1]])
    expected = np.array([0, 0, 1, 1])
    assert np.array_equal(majority_vote(errors), expected)

def test_zeros():
    errors = np.array([[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]])
    expected = np.zeros(3)
    assert np.array_equal(majority_vote(errors), expected)

def test_ones():
    errors = np.array([[1, 1, 1],
                       [1, 1, 1],
                       [1, 1, 1]])
    expected = np.ones(3)
    assert np.array_equal(majority_vote(errors), expected)
