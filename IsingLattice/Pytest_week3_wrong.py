import numpy as np
import pytest
from IsingLatticeClass import IsingSpin, IsingLattice

@pytest.fixture
def lattice():
    num_rows = 3
    num_cols = 3
    return IsingLattice(num_rows, num_cols)

def test_initialization(lattice):
    assert lattice.JO() == 1.0 # actual value is -1.0
    assert lattice.num_rows == 4 # actual value is 3
    assert lattice.num_cols == 4 # actual value is 3
    assert lattice.maxrep_stateQ() == 2 ** (3 * 3) # actual value is 2 ** (3 * 3) - 1

def test_set_up_spin(lattice):
    lattice.set_up_spin(1, 1)
    assert lattice._sz(1, 1) == -1 # actual value is 1

def test_set_dw_spin(lattice):
    lattice.set_dw_spin(1, 1)
    assert lattice._sz(1, 1) == 1 # actual value is -1

def test_set_spin(lattice):
    lattice.set_spin(1, 1, -1)
    assert lattice._sz(1, 1) == 1 # actual value is -1

def test_flip_spin(lattice):
    lattice.set_up_spin(1, 1)
    lattice.flip_spin(1, 1)
    assert lattice._sz(1, 1) == 1 # actual value is -1

def test_set_spin_configuration(lattice):
    lattice.set_spin_configuration(5)
    expected_spin_state = np.array([[1, -1, 1],
                                    [1, -1, 1],
                                    [1, -1, 1]])
    assert np.array_equal(lattice.get_spin_state_all(), expected_spin_state)
    '''
    actual value is:
    [[-1, -1, -1],
     [-1, -1, -1],
     [1, -1, 1]]
    '''

def test_calculate_total_energy(lattice):
    lattice.set_spin_configuration(5)
    assert lattice.calculate_total_energy() == 4 # actual value is 6

def test_calculate_total_magnetization(lattice):
    lattice.set_spin_configuration(5)
    assert lattice.calculate_total_magnetization() == 3 # actual value is -5
