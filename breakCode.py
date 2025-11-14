import random, math, time
from tracemalloc import start
from sympy import isprime, factorint

# ---------- Trial division Linear ----------
def trial_division(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    if n % 5 == 0:
        return 5

    i = 10**50 + 1  
    wheel = [4, 2, 4, 2, 4, 6, 2, 6]

    wi = 0
    while i * i <= n:
        print(f"[*] testando divisor {i}")
        if n % i == 0:
            return i
        i += wheel[wi]
        wi = (wi + 1) % len(wheel)
    return None

# ---------- Trial division Aleatorio ----------
def randomized_trial_division(n):
    if n % 2 == 0:
        return 2

    Tests = set()

    count = 0;

    while True:
        count += 1
        i = random.randrange(10**99, 10**100, 2)
        if i in Tests:
            continue  
        Tests.add(i)

        print(f"[*] Testando divisor aleatório |tentativa:{count}| - {i}")

        if n % i == 0:
            print(f"[+] Divisor encontrado: {i}")
            return i                

# ---------- Pollard's Rho ----------
def pollard_rho(n, max_iters=100000):
    if n % 2 == 0:
        return 2
    if isprime(n):
        return n
    for attempt in range(5):
        print(f"\n[*] pollard rho tentativa {attempt+1}...")
        x = random.randrange(2, n-1)
        y = x
        c = random.randrange(1, n-1)
        d = 1
        iters = 0
        while d == 1 and iters < max_iters:
            x = (x*x + c) % n
            y = (y*y + c) % n
            y = (y*y + c) % n
            d = math.gcd(abs(x-y), n)
            iters += 1
        if d == n or d == 1:
            continue
        return d
    return None

# ---------- Pollard p-1 ----------
def pollard_p_minus_1(n, B=10000):    
    a = 2
    for q in range(2, B):
        print(f"\n[*] pollard p-1 testando primo {q}...")
        a = pow(a, q, n)
    g = math.gcd(a-1, n)
    if 1 < g < n:
        return g
    return None

# ---------- Orquestrador ----------
def try_factor(n, timeout_seconds=60, quantum_seed=None, break_mode=1):    
    if quantum_seed is not None:
        print(f"[🧠] Entropia quântica aplicada: seed = {quantum_seed}")
        random.seed(quantum_seed)
    else:
        random.seed(time.time())

    #start = time.time()

    print(f"\n\n[*] tentando fatorar n ({n.bit_length()} bits)...")

    match break_mode:
        case 1:
            print("[*] Modo 1: Tentando apenas trial division.")
            f = trial_division(n)
            if f:
                print("[+] trial division encontrou fator:", f)
                return f, n//f    
            else:
                print("[-] trial division não encontrou fatores.")
                return None
        case 2:
            print("[*] Modo 2: Tentando apenas randomized trial division.")
            f = randomized_trial_division(n)
            if f:
                print("[+] randomized trial division encontrou fator:", f)
                return f, n//f    
            else:
                print("[-] randomized trial division não encontrou fatores.")
                return None
        case 3:
            print("[*] Modo 3: Tentando apenas pollard rho.")
            f = pollard_rho(n, max_iters=500000)
            if f:
                print("[+] pollard rho encontrou fator:", f)
                return f, n//f    
            else:
                print("[-] pollard rho não encontrou fatores.")
                return None
        case 4:
            print("[*] Modo 4: Tentando apenas pollard p-1.")
            f = pollard_p_minus_1(n, B=5000)
            if f:
                print("[+] pollard p-1 encontrou fator:", f)
                return f, n//f    
            else:
                print("[-] pollard p-1 não encontrou fatores.")
                return None
        case 5: 
            print("[*] Modo 5: Tentando todos os métodos clássicos.")
            methods = [
                ("trial division", trial_division),
                ("randomized trial division", randomized_trial_division),
                ("pollard rho", pollard_rho),
                ("pollard p-1", pollard_p_minus_1)
            ]
            for name, method in methods:
                print(f"\n[*] Tentando {name}...")
                f = method(n)
                if f:
                    print(f"[+] {name} encontrou fator:", f)
                    return f, n//f    
                else:
                    print(f"[-] {name} não encontrou fatores.")
        case _:
            return None

    print("[-] não foi possível encontrar fator dentro do timeout.")
    return None
