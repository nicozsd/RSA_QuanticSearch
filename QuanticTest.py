#Quebras RSA
import breakCode

#circuito quantico
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.primitives import StatevectorSampler

#Plotagem de graficos
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

#Geração RSA
from sympy import randprime, nextprime, mod_inverse, gcd

# Tipagem
from typing import TypedDict

'''
p - Primo 1
q - Primo 2
n - Modulo RSA, Produto de p e q
phi_n - Totiente de Euler
e - Expoente publico
d - Expoente privado
(n - e) - Chave publica
(n - d) - Chave privada
'''
def generate_rsa_keypair(_n = 100):
    limit = 10**_n
    
    p = nextprime(randprime(10**99, limit - 1))
    q = nextprime(randprime(10**99, limit - 1))
    
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    e = 65537
    if gcd(e, phi_n) != 1:        
        e = randprime(3, 10**6)
        while gcd(e, phi_n) != 1:
            e = randprime(3, 10**6)
    
    d = mod_inverse(e, phi_n)

    return {
        "p": p,
        "q": q,
        "n": n,
        "phi_n": phi_n,
        "e": e,
        "d": d
    }

# === SISTEMA QUÂNTICO ===
class SysParametersType(TypedDict):
    qubits: int

def Plot_Graph(_counts):
    plot_histogram(_counts)
    plt.show()

def Set_Bell_State(_qubits):
    qc = QuantumCircuit(_qubits)
    qc.h(0)
    qc.cx(0, 1)
    return qc

def exec_Analisys_CPU(_qubits):
    qc = Set_Bell_State(_qubits)
    qc.measure_all()

    sampler = StatevectorSampler()
    job     = sampler.run([qc], shots=1024)
    result  = job.result()
    
    counts = result[0].data.meas.get_counts()
    #Plot_Graph(counts)
        
    max_key = max(counts, key=counts.get)
    return int(max_key, 2) % 1000  

def exec_Analisys_GPU(_qubits):
    qc = Set_Bell_State(_qubits)
    qc.measure_all()

    simulator = AerSimulator(method='statevector', device='GPU')
    job = simulator.run(qc, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    max_key = max(counts, key=counts.get)
    return int(max_key, 2) % 1000

def Sys_Parameters() -> SysParametersType:
    return {
        'qubits_GPU': 27,
        'qubits_CPU': 20
    }

# === EXECUÇÃO PRINCIPAL ===
params = Sys_Parameters()
keys = generate_rsa_keypair()

print("\nChave RSA Privada: \n", (keys['n'], keys['d']))
print("\nChave RSA Pública: \n", (keys['n'], keys['e']))

# Executa análise quântica antes da quebra
quantum_bias = exec_Analisys_GPU(params['qubits_GPU'])
#quantum_bias = exec_Analisys_CPU(params['qubits_CPU'])
print(f"\n→ Resultado quântico (entanglement modulação): {quantum_bias}")

# Passa o valor quântico como 'seed' pro fatorador
breakCode.try_factor(keys['n'], timeout_seconds=120, quantum_seed=quantum_bias, break_mode=2)