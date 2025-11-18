# ============================================================
# batch_test_runner.py
# ============================================================

import time
import importlib
import traceback

# Importa seu arquivo principal (o nome pode ser alterado)
main = importlib.import_module("QuanticTest")  
# Se o nome do seu arquivo for diferente, troque "main" pelo certo.

def run_single_test(bits_rsa, qubits_cpu, qubits_gpu, break_mode, excel_file="Resultados_QBreak.xlsx"):
    """
    Executa UM teste completo usando o módulo principal.
    Usa exatamente as funções do seu script original.
    """

    print("\n===========================================")
    print(f"Rodando teste: {bits_rsa} bits | CPU {qubits_cpu} | GPU {qubits_gpu}")
    print("===========================================\n")

    try:
        # === Configuração dinâmica ===
        main.Sys_Parameters = lambda: {
            'qubits_GPU': qubits_gpu,
            'qubits_CPU': qubits_cpu,
            'bits_RSA': bits_rsa
        }

        # === Início ===
        t0 = time.time()

        # Geração RSA
        keys = main.generate_rsa_keypair(bits_rsa)
        t_rsa = time.time() - t0

        # Modo exec
        exec_mode = "GPU" if qubits_gpu > qubits_cpu else "CPU"

        # Análise quântica
        t1 = time.time()
        if exec_mode == "CPU":
            bias = main.exec_Analisys_CPU(qubits_cpu)
        else:
            bias = main.exec_Analisys_GPU(qubits_gpu)
        t_quant = time.time() - t1

        # Tentativa de quebra
        t2 = time.time()
        p_found, q_found = main.breakCode.try_factor(
            keys['n'],
            BitsValues=bits_rsa,
            quantum_seed=bias,
            break_mode=break_mode
        )
        t_break = time.time() - t2

        # Validando d
        d_found = main.calc_by_private_key(p_found, q_found, keys['e'])

        # Total
        t_total = t_rsa + t_quant + t_break

        # Salva no Excel
        main.save_or_update_excel(
            filename=excel_file,
            qubits=qubits_gpu,
            metodo_quebra=break_mode,
            modo_execucao=exec_mode,
            dados={
                "bias": bias,
                "t_rsa": t_rsa,
                "t_quant": t_quant,
                "t_break": t_break,
                "t_total": t_total,
                "p": p_found,
                "q": q_found,
                "ok": (d_found == keys['d'])
            }
        )

        return {
            "bits": bits_rsa,
            "qubits_cpu": qubits_cpu,
            "qubits_gpu": qubits_gpu,
            "break_mode": break_mode,
            "bias": bias,
            "rsa_ok": (d_found == keys['d']),
            "tempo_total": t_total
        }

    except Exception as e:
        print("❌ Erro no teste:")
        traceback.print_exc()
        return None


# =============================================================
# === BATERIA DE TESTES ========================================
# =============================================================

def run_batch():
    bits_test = [16, 20, 25, 30]   # Diferentes bit-sizes para validação
    cpu_qb    = [12, 16]           # variação CPU
    gpu_qb    = [22, 25]           # variação GPU
    break_modes = [1, 4, 3]        # MODOS

    total_tests = 0
    successes   = 0

    for bits in bits_test:
        for qc in cpu_qb:
            for qg in gpu_qb:
                for m in break_modes:

                    result = run_single_test(
                        bits_rsa=bits,
                        qubits_cpu=qc,
                        qubits_gpu=qg,
                        break_mode=m
                    )

                    total_tests += 1
                    if result and result["rsa_ok"]:
                        successes += 1

                    time.sleep(1)  

    print("\n\n==============================")
    print("BATERIA DE TESTES FINALIZADA")
    print("==============================")
    print(f"Total de testes: {total_tests}")
    print(f"Sucessos.......: {successes}")
    print(f"Falhas.........: {total_tests - successes}")
    print("==============================\n")


# Executa automaticamente se rodar o arquivo
if __name__ == "__main__":
    run_batch()
