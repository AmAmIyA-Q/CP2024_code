import numpy as np
import matplotlib.pyplot as plt

def ising_model(size, temperature):
    # Initialize a random spin configuration
    spins = np.random.choice([-1, 1], size=(size, size))
    
    # Define the energy function
    def energy(spins):
        return -np.sum(spins * np.roll(spins, 1, axis=0) +
                       spins * np.roll(spins, -1, axis=0) +
                       spins * np.roll(spins, 1, axis=1) +
                       spins * np.roll(spins, -1, axis=1))
    
    # Define the Metropolis algorithm
    def metropolis(spins, temperature):
        i, j = np.random.randint(size), np.random.randint(size)
        delta_energy = 2 * spins[i, j] * (spins[(i+1)%size, j] +
                                          spins[(i-1)%size, j] +
                                          spins[i, (j+1)%size] +
                                          spins[i, (j-1)%size])
        if delta_energy < 0 or np.random.rand() < np.exp(-delta_energy / temperature):
            spins[i, j] *= -1
    
    # Perform the simulation
    for _ in range(10000):
        metropolis(spins, temperature)
    
    # Plot the final spin configuration
    plt.imshow(spins, cmap='binary')
    plt.show()

# Example usage
ising_model(size=100, temperature=2.0)