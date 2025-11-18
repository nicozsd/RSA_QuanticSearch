import random, math, time
from math import sqrt, floor
from sympy import isprime, factorint


# ============================================================
#  TRIAL DIVISION (LINEAR)
# ============================================================
def trial_division(n):    
    if (n & 1) == 0:
        return (n//2, 2)

    a = floor(sqrt(n))
    
    if a * a == n:
        return (a, a)

    while True:    
        a += 1

        print(f"[*] testando divisor {a}")

        _b = a * a - n

        if _b < 0:
            continue

        b = int(sqrt(_b))
        if (b * b == _b):
            break

    return (a + b, a - b)


# ============================================================
#  RANDOMIZED TRIAL DIVISION
# ============================================================
def randomized_trial_division(n, _bits):
    if n % 2 == 0:
        return 2

    Tests = set()
    count = 0

    while True:
        count += 1
        i = random.randrange(10**(_bits-1), 10**_bits, 2)
        if i in Tests:
            continue  
        Tests.add(i)

        print(f"[*] Testando divisor aleatório |tentativa:{count}| - {i}")

        if n % i == 0:
            print(f"[+] Divisor encontrado: {i}")
            return i                


# ============================================================
#  POLLARD RHO (BÁSICO)
# ============================================================
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
        if d != n and d != 1:
            return d
    return None


# ============================================================
#  POLLARD P-1
# ============================================================
def pollard_p_minus_1(n, B=10000):    
    a = 2
    for q in range(2, B):
        print(f"\n[*] pollard p-1 testando primo {q}...")
        a = pow(a, q, n)
    g = math.gcd(a-1, n)
    if 1 < g < n:
        return g
    return None


# ============================================================
#  FERMAT OTIMIZADO
# ============================================================
def fermat_factor(n):
    if n % 2 == 0:
        return 2

    a = math.isqrt(n)
    if a*a == n:
        return a, a

    b2 = a*a - n
    step = 1

    while b2 < 0 or int(math.isqrt(b2))**2 != b2:
        a += step
        b2 = a*a - n
        step += 1
        if step > 100000000:
            return None

    b = int(math.isqrt(b2))
    return (a+b, a-b)


# ============================================================
#  BRENT POLLARD RHO (OTIMIZADO)
# ============================================================
def brent_pollard_rho(n):
    if n % 2 == 0:
        return 2

    y = random.randrange(1, n)
    c = random.randrange(1, n)
    m = random.randrange(1, n)

    g, r, q = 1, 1, 1

    while g == 1:
        x = y
        for _ in range(r):
            y = (y*y + c) % n

        k = 0
        while k < r and g == 1:
            ys = y
            for _ in range(min(m, r-k)):
                y = (y*y + c) % n
                q = q * abs(x-y) % n
            g = math.gcd(q, n)
            k += m
        
        r *= 2

    if g == n:
        while True:
            ys = (ys*ys + c) % n
            g = math.gcd(abs(x-ys), n)
            if g > 1:
                break

    return g


# ============================================================
#  DIXON FACTORIZATION
# ============================================================
def dixon_factor(n, tries=50000):
    B = 1000
    base = [p for p in range(2, B) if isprime(p)]

    for _ in range(tries):
        x = random.randint(2, n-2)
        r = (x*x) % n
        factors = factorint(r)

        if all(p in base for p in factors):
            y = 1
            for p, exp in factors.items():
                y *= pow(p, exp // 2)

            f = math.gcd(x - y, n)
            if 1 < f < n:
                return f
    return None


# ============================================================
#  MINI ECM — ELLIPTIC CURVE METHOD (Montgomery)
# ============================================================
def mini_ecm(n, curves=50, B1=1000):
    if n % 2 == 0:
        return 2

    def montgomery_step(a, x, z):
        return ((x*x - z*z)**2 % n, 4*x*z*(x*x + a*x*z + z*z) % n)

    for _ in range(curves):
        x = random.randint(2, n-1)
        z = 1
        a = random.randint(2, n-1)

        for p in range(2, B1):
            q = pow(p, int(math.log(n, p)))
            for _ in range(q):
                x, z = montgomery_step(a, x, z)
                g = math.gcd(z, n)
                if 1 < g < n:
                    return g

    return None


# ============================================================
#  MINI QUADRATIC SIEVE (wrapper do sympy)
# ============================================================
def mini_quadratic_sieve(n):
    try:
        factors = factorint(n)
        for f in factors:
            if 1 < f < n:
                return f
    except:
        pass
    return None


# ============================================================
#  NORMALIZADOR UNIVERSAL
# ============================================================
def normalize_factor(n, f):
    if isinstance(f, tuple):
        return f[0], f[1]
    return f, n // f


# ============================================================
#  ORQUESTRADOR PRINCIPAL
# ============================================================
def try_factor(n, quantum_seed=None, BitsValues=0, break_mode=1):    

    if quantum_seed is not None:
        print(f"Entropia quântica aplicada: seed = {quantum_seed}")
        random.seed(quantum_seed)
    else:
        random.seed(time.time())

    print(f"\n\n[*] tentando fatorar n ({n.bit_length()} bits)...")

    match break_mode:

        case 1:
            print("[*] Modo 1: Trial division.")
            f = trial_division(n)
            if f:
                f1, f2 = normalize_factor(n, f)
                print("[+] Trial division encontrou fatores:", f1, f2)
                return f1, f2
            return None

        case 2:
            print("[*] Modo 2: Randomized trial division.")
            f = randomized_trial_division(n, BitsValues)
            if f:
                f1, f2 = normalize_factor(n, f)
                print("[+] Randomized encontrou fatores:", f1, f2)
                return f1, f2
            return None

        case 3:
            print("[*] Modo 3: Pollard Rho.")
            f = pollard_rho(n)
            if f:
                f1, f2 = normalize_factor(n, f)
                print("[+] Pollard Rho encontrou fatores:", f1, f2)
                return f1, f2
            return None

        case 4:
            print("[*] Modo 4: Pollard P-1.")
            f = pollard_p_minus_1(n)
            if f:
                f1, f2 = normalize_factor(n, f)
                print("[+] Pollard P-1 encontrou fatores:", f1, f2)
                return f1, f2
            return None

        case 5:
            print("[*] Modo 5: Sequência Clássica Completa.")
            methods = [
                ("Trial division", trial_division),
                ("Randomized trial division", randomized_trial_division),
                ("Pollard Rho", pollard_rho),
                ("Pollard P-1", pollard_p_minus_1)
            ]
            for name, method in methods:
                print(f"\n[*] Tentando {name}...")
                f = method(n)
                if f:
                    f1, f2 = normalize_factor(n, f)
                    print(f"[+] {name} encontrou fatores:", f1, f2)
                    return f1, f2
            print("[-] Nenhum método encontrou fator.")
            return None

        case 6:
            print("[*] Modo 6: Fermat otimizado.")
            f = fermat_factor(n)
            if f:
                f1, f2 = normalize_factor(n, f)
                print("[+] Fermat encontrou fatores:", f1, f2)
                return f1, f2
            return None

        case 7:
            print("[*] Modo 7: Brent Pollard Rho.")
            f = brent_pollard_rho(n)
            if f:
                f1, f2 = normalize_factor(n, f)
                print("[+] Brent encontrou fatores:", f1, f2)
                return f1, f2
            return None

        case 8:
            print("[*] Modo 8: Dixon.")
            f = dixon_factor(n)
            if f:
                f1, f2 = normalize_factor(n, f)
                print("[+] Dixon encontrou fatores:", f1, f2)
                return f1, f2
            return None

        case 9:
            print("[*] Modo 9: ECM (mini).")
            f = mini_ecm(n)
            if f:
                f1, f2 = normalize_factor(n, f)
                print("[+] ECM encontrou fatores:", f1, f2)
                return f1, f2
            return None

        case 10:
            print("[*] Modo 10: Quadratic Sieve (mini).")
            f = mini_quadratic_sieve(n)
            if f:
                f1, f2 = normalize_factor(n, f)
                print("[+] Mini QS encontrou fatores:", f1, f2)
                return f1, f2
            return None

        case _:
            print("[-] Modo inválido.")
            return None