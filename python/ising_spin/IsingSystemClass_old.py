import numpy as np

# old vertion

class IsingSystem:
    def __init__(self, num_spins):
        self.num_spins = num_spins
        self.spins = np.ones(num_spins, dtype=int)  # Initialize all spins up

    def set_spin_configuration(self, configuration_code):
        binary_string = bin(configuration_code)[2:].zfill(self.num_spins)
        self.spins = np.array([int(bit) * 2 - 1 for bit in binary_string])

    def calculate_total_magnetization(self):
        return np.sum(self.spins)

    def calculate_total_energy(self):
        energy = 0
        for i in range(self.num_spins):
            energy += -self.spins[i] * (self.spins[(i + 1) % self.num_spins] + self.spins[(i - 1) % self.num_spins])
        return energy / 2  # Correct for double counting and divide by 2

# # Example usage:
# n = 10
# system = IsingSystem(n)

# configurations = [7, 77, 777]

# for config in configurations:
#     system.set_spin_configuration(config)
#     M = system.calculate_total_magnetization()
#     E = system.calculate_total_energy()
#     print(f"For configuration {config}:")
#     print(system.spins)
#     print(f"Total Magnetization: {M}")
#     print(f"Total Energy: {E}")
#     print()
