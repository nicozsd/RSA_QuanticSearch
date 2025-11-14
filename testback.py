from qiskit_aer import AerSimulator
backend = AerSimulator()
print(backend.available_methods())
print(backend.available_devices())