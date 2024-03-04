import random
import math

def initialize_spins(N):
    spins = [random.choice([-1, 1]) for _ in range(N)]
    return spins

def calculate_energy(spins, J):
    energy = 0
    N = len(spins)
    for i in range(N):
        energy += -J * spins[i] * spins[(i + 1) % N]
    return energy

def monte_carlo_simulation(N, J, temperature, num_steps, spins, energy):

    for _ in range(num_steps):
        i = random.randint(0, N - 1)
        old_spin = spins[i]
        new_spin = -old_spin
        delta_energy = 2 * J * old_spin * (spins[(i - 1) % N] + spins[(i + 1) % N])
        if delta_energy <= 0 or random.random() < math.exp(-delta_energy / temperature):
            spins[i] = new_spin
            energy += delta_energy
    return spins, energy

# # Example usage
# N = 10  # Number of spins
# J = 1  # Interaction strength
# temperature = 2.0  # Temperature
# num_steps = 0  # Number of Monte Carlo steps


# spins = initialize_spins(N)
# energy = calculate_energy(spins, J)
# print("Initial spins:", spins)
# print("Initial energy:", energy)

# spins, energy = monte_carlo_simulation(N, J, temperature, num_steps, spins, energy)
# print("Final spins:", spins)
# print("Final energy:", energy)