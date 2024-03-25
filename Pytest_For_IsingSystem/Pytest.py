import pytest
import numpy as np
from IsingSystemClass import IsingSpin, IsingSystem

@pytest.fixture
def ising_system():
    return IsingSystem(4)  # 创建一个包含4个自旋的 Ising 系统

def test_isingspin_init():
    spin = IsingSpin()
    assert spin.sz == 1

def test_isingspin_set_up():
    spin = IsingSpin()
    spin.set_up()
    assert spin.sz == 1

def test_isingspin_set_dw():
    spin = IsingSpin()
    spin.set_dw()
    assert spin.sz == -1

def test_isingspin_set_sz_valid():
    spin = IsingSpin()
    spin.set_sz(1)
    assert spin.sz == 1

def test_isingspin_set_sz_invalid():
    spin = IsingSpin()
    with pytest.raises(AssertionError):
        spin.set_sz(0)

def test_isingspin_flip():
    spin = IsingSpin()
    spin.flip()
    assert spin.sz == -1

def test_isingsystem_init(ising_system):
    assert ising_system.J == -1.0
    assert ising_system.num_spins == 4
    assert ising_system.maxrep_state == 15  # 2^4 - 1

def test_isingsystem_JO(ising_system):
    assert ising_system.JO() == -1.0

def test_isingsystem_change_J(ising_system):
    ising_system.change_J(-2.0)
    assert ising_system.J == -2.0

def test_isingsystem_num_spins(ising_system):
    assert ising_system.num_spins == 4

def test_isingsystem_maxrep_stateQ(ising_system):
    assert ising_system.maxrep_stateQ() == 15

def test_isingsystem_set_up_spin(ising_system):
    ising_system.set_up_spin(2)
    assert ising_system.spin[2].sz == 1

def test_isingsystem_set_dw_spin(ising_system):
    ising_system.set_dw_spin(2)
    assert ising_system.spin[2].sz == -1

def test_isingsystem_set_spin(ising_system):
    ising_system.set_spin(2, 1)
    assert ising_system.spin[2].sz == 1

def test_isingsystem_flip_spin(ising_system):
    ising_system.flip_spin(2)
    assert ising_system.spin[2].sz == -1

def test_isingsystem_set_spin_configuration(ising_system):
    ising_system.set_spin_configuration(5)  # 101 in binary
    assert ising_system.spin[0].sz == -1
    assert ising_system.spin[1].sz == 1
    assert ising_system.spin[2].sz == -1
    assert ising_system.spin[3].sz == 1

def test_isingsystem_get_spin_state(ising_system):
    ising_system.set_spin_configuration(5)  # 101 in binary
    assert ising_system.get_spin_state()[0] == -1
    assert ising_system.get_spin_state()[1] == 1
    assert ising_system.get_spin_state()[2] == -1
    assert ising_system.get_spin_state()[3] == 1


def test_isingsystem_calculate_total_energy(ising_system):
    ising_system.set_spin_configuration(5)  # 101 in binary
    assert ising_system.calculate_total_energy() == -4.0  # Expected total energy for this configuration

def test_isingsystem_calculate_total_magnetization(ising_system):
    ising_system.set_spin_configuration(5)  # 101 in binary
    assert ising_system.calculate_total_magnetization() == 0  # Expected total magnetization for this configuration
