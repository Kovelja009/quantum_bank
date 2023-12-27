import matplotlib.pyplot as plt

# Calculate probabilities for different numbers of qubits (n)
n_values = list(range(1, 21))  # Considering n from 1 to 20
probabilities = [(2/3)**n for n in n_values]

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(n_values, probabilities, marker='o', linestyle='-', color='purple')
plt.xlabel('Broj kubita (n)')
plt.ylabel('Verovatnoća uspeha')
plt.title('Verovatnoća uspeha u zavisnosti od broja kubita')
plt.grid(True)
plt.show()