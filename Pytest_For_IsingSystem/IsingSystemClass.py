import numpy as np

class IsingSpin:
    def __init__(self):
        self.sz = 1  # 默认构造函数，将自旋初始化为+1

    def get_sz(self):
        return self.sz  # 返回当前自旋的值

    def set_up(self):
        self.sz = 1  # 将自旋设置为+1，表示向上

    def set_dw(self):
        self.sz = -1  # 将自旋设置为-1，表示向下

    def set_sz(self, sz_spec):
        # 设置自旋为给定的值，参数必须是+1或-1，否则会触发断言错误
        assert sz_spec == 1 or sz_spec == -1
        self.sz = sz_spec

    def flip(self):
        self.sz *= -1  # 翻转自旋的方向，由+1变为-1，或由-1变为+1


# # 测试 IsingSpin 类的功能
# ising_spin = IsingSpin()
# print("Initial sz:", ising_spin.get_sz())

# ising_spin.set_dw()
# print("After setting down:", ising_spin.get_sz())

# ising_spin.flip()
# print("After flipping:", ising_spin.get_sz())


class IsingSystem:
    def __init__(self, num_spins):
        self.J = -1.0
        self.num_spins = num_spins
        self.maxrep_state = 2 ** num_spins - 1
        self.spin = [IsingSpin() for _ in range(num_spins)]

    def JO(self):
        return self.J
    
    def change_J(self, new_J):
        self.J = new_J

    def num_spins(self):
        return self.num_spins

    def maxrep_stateQ(self):
        return self.maxrep_state

    def _sz(self, site_idx):
        return self.spin[site_idx]._sz()

    def set_up_spin(self, site_idx):
        self.spin[site_idx].set_up()

    def set_dw_spin(self, site_idx):
        self.spin[site_idx].set_dw()

    def set_spin(self, site_idx, s_spec):
        self.spin[site_idx].set_sz(s_spec)

    def flip_spin(self, site_idx):
        self.spin[site_idx].flip()

    def set_spin_configuration(self, configuration_code):
        binary_string = bin(configuration_code)[2:].zfill(self.num_spins)
        spin_array = np.array([int(bit) * 2 - 1 for bit in binary_string])
        for i in range(self.num_spins):
            self.spin[i].set_sz(spin_array[i])
    
    def get_spin_state(self):
        return np.array([self.spin[i].get_sz() for i in range(self.num_spins)])
    
    def calculate_total_energy(self):
        energy = 0
        for i in range(self.num_spins):
            energy += -self.J * self.spin[i].get_sz() * (self.spin[(i + 1) % self.num_spins].get_sz() +
                                                         self.spin[(i - 1) % self.num_spins].get_sz())
        return energy / 2

    def calculate_total_magnetization(self):
        return np.sum([self.spin[i].get_sz() for i in range(self.num_spins)])

# # Example usage:
# n = 10
# system = IsingSystem(n)

# configurations = [7, 77, 777]

# for config in configurations:
#     system.set_spin_configuration(config)
#     M = system.calculate_total_magnetization()
#     E = system.calculate_total_energy()
#     print(f"For configuration {config}:")
#     print(system.get_spin_state())
#     print(f"Total Magnetization: {M}")
#     print(f"Total Energy: {E}")
#     print()