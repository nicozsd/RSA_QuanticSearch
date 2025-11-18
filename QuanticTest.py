import breakCode
import time
import os
from openpyxl import Workbook, load_workbook

# Qiskit
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.primitives import StatevectorSampler

# Plot
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# RSA
from sympy import randprime, mod_inverse, gcd
from typing import TypedDict

def_type   = 2
break_mode = 1

exec_mode  = "CPU" if def_type == 1 else "GPU"

breakMode_desc = {
    1: "Trial Division",
    2: "Randomized Trial Division",
    3: "Pollard Rho",
    4: "Pollard p-1",
    5: "All Classical Methods",
    6: "Mini Quadratic Sieve"
}

# =====================================================================
# === FUNÇÃO EXCEL =====================================================
def save_or_update_excel(filename, qubits, metodo_quebra, modo_execucao, dados: dict):

    if not os.path.exists(filename):
        wb = Workbook()
        ws = wb.active
        ws.title = "Resultados"

        ws.append([
            "qubits",
            "metodo_quebra",
            "execucao",
            "bias_quântico",
            "tempo_RSA",
            "tempo_Quantum",
            "tempo_Break",
            "tempo_Total",
            "p_encontrado",
            "q_encontrado",
            "Quebra_OK"
        ])

        wb.save(filename)

    wb = load_workbook(filename)
    ws = wb.active

    linha_existente = None
    for row in ws.iter_rows(min_row=2):
        qbt   = row[0].value
        mtd   = row[1].value
        modo  = row[2].value

        if qbt == qubits and mtd == metodo_quebra and modo == modo_execucao:
            linha_existente = row
            break

    if linha_existente:
        (
            linha_existente[0].value,
            linha_existente[1].value,
            linha_existente[2].value,
            linha_existente[3].value,
            linha_existente[4].value,
            linha_existente[5].value,
            linha_existente[6].value,
            linha_existente[7].value,
            linha_existente[8].value,
            linha_existente[9].value,
            linha_existente[10].value
        ) = (
            qubits,
            metodo_quebra,
            modo_execucao,
            dados["bias"],
            dados["t_rsa"],
            dados["t_quant"],
            dados["t_break"],
            dados["t_total"],
            dados["p"],
            dados["q"],
            dados["ok"]
        )
    else:
        ws.append([
            qubits,
            metodo_quebra,
            modo_execucao,
            dados["bias"],
            dados["t_rsa"],
            dados["t_quant"],
            dados["t_break"],
            dados["t_total"],
            dados["p"],
            dados["q"],
            dados["ok"]
        ])

    wb.save(filename)
    print("✔ Excel salvo/atualizado:", filename)



# =====================================================================
# === GERAÇÃO DE CHAVES RSA ===========================================
# =====================================================================

def generate_rsa_keypair(_bits):
    min_value = 1 << (_bits - 1)
    max_value = (1 << _bits) - 1
    
    p = randprime(min_value, max_value)
    q = randprime(min_value, max_value)
    
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    e = 65537
    if gcd(e, phi_n) != 1:
        e = randprime(3, 10**6)
        while gcd(e, phi_n) != 1:
            e = randprime(3, 10**6)

    d = mod_inverse(e, phi_n)

    return { "p": p, "q": q, "n": n, "phi_n": phi_n, "e": e, "d": d }


def calc_by_private_key(_p, _q, _e):
    n = _p * _q
    phi = (_p - 1) * (_q - 1)
    d = pow(_e, -1, phi)
    return d


# =====================================================================
# === SISTEMA QUÂNTICO ================================================
# =====================================================================

class SysParametersType(TypedDict):
    qubits_GPU: int
    qubits_CPU: int
    bits_RSA: int


def Sys_Parameters() -> SysParametersType:
    return {
        'qubits_GPU': 26,
        'qubits_CPU': 20,
        'bits_RSA': 50
    }


def Set_Bell_State(_qubits):
    qc = QuantumCircuit(_qubits)
    qc.h(0)
    qc.cx(0, 1)
    return qc


# ============================================================
# === GPU MAX PERFORMANCE ====================================
# ============================================================

def exec_Analisys_GPU(_qubits):
    qc = Set_Bell_State(_qubits)
    qc.measure_all()

    simulator = AerSimulator(
        method='statevector',
        device='GPU',
        max_parallel_threads=128,
        cuStateVec_enable=True,
        fusion_enable=True,
        fusion_max_qubit=6,
        precision='double'
    )

    job = simulator.run(qc, shots=4096)
    result = job.result()
    counts = result.get_counts()

    max_key = max(counts, key=counts.get)
    return int(max_key, 2) % 1000

def exec_Analisys_CPU(_qubits):
    qc = Set_Bell_State(_qubits)
    qc.measure_all()

    sampler = StatevectorSampler()
    job     = sampler.run([qc], shots=1024)
    result  = job.result()
    
    counts = result[0].data.meas.get_counts()
    max_key = max(counts, key=counts.get)
    return int(max_key, 2) % 1000  


# =====================================================================
# === EXECUÇÃO PRINCIPAL ==============================================
# =====================================================================

params = Sys_Parameters()

# TEMPO: geração RSA
t0 = time.time()
keys = generate_rsa_keypair(params['bits_RSA'])
t_rsa = time.time() - t0

print("\n==== CHAVES RSA GERADAS ====")
print("\nChave RSA Privada (n, d):\n", (keys['n'], keys['d']))
print("\nChave RSA Pública (n, e):\n", (keys['n'], keys['e']))

# TEMPO: análise quântica
t1 = time.time()

if(exec_mode == "CPU"):
    quantum_bias = exec_Analisys_CPU(params['qubits_CPU'])
else:
    quantum_bias = exec_Analisys_GPU(params['qubits_GPU'])

t_quantum = time.time() - t1

print(f"\n→ Resultado quântico (entanglement modulação): {quantum_bias}")

# TEMPO: quebra RSA
t2 = time.time()
Break_keys = breakCode.try_factor(
    keys['n'],
    BitsValues=params['bits_RSA'],
    quantum_seed=quantum_bias,
    break_mode=1
)
t_break = time.time() - t2

p_found, q_found = Break_keys
d_found = calc_by_private_key(p_found, q_found, 65537)


# =====================================================================
# === RESUMO FINAL =====================================================
# =====================================================================

print("\n\n==================== RESUMO FINAL ====================")
print(f"Qubits................: {params['qubits_GPU']}")
print(f"Bits RSA..............: {params['bits_RSA']}")
print(f"Bias Quântico.........: {quantum_bias}")
print(f"n......................: {keys['n']}")
print(f"e......................: {keys['e']}")
print(f"d (original)...........: {keys['d']}")
print(f"d (calculado)..........: {d_found}")
print(f"p encontrado............: {p_found}")
print(f"q encontrado............: {q_found}")

print("\n=== TEMPOS ===")
print(f"Gerar RSA.............: {t_rsa:.4f} s")
if(exec_mode == "CPU"):
    print(f"Análise Quântica (CPU): {t_quantum:.4f} s")
else:
    print(f"Análise Quântica (GPU): {t_quantum:.4f} s")
print(f"Tempo Total...........: {t_rsa + t_quantum + t_break:.4f} s")

print("\nQuebra bem-sucedida?...:",
      "SIM" if d_found == keys['d'] else "NÃO")
print("======================================================\n")


# =====================================================================
# === SALVAR NO EXCEL ================================================
# =====================================================================

modo_execucao = "GPU"
metodo_quebra = "trial_division"

save_or_update_excel(
    filename="Resultados_QBreak.xlsx",
    qubits=params['qubits_GPU'],
    metodo_quebra=break_mode,
    modo_execucao=exec_mode,
    dados={
        "bias": quantum_bias,
        "t_rsa": t_rsa,
        "t_quant": t_quantum,
        "t_break": t_break,
        "t_total": t_rsa + t_quantum + t_break,
        "p": p_found,
        "q": q_found,
        "ok": (d_found == keys['d'])
    }
)