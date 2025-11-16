# rsa stuff

import math
from factordb.factordb import FactorDB

def gcd(a, b):
    # fast binary gcd
    if a == 0: return b
    if b == 0: return a
    
    # remove factors of 2
    shift = 0
    while ((a | b) & 1) == 0:
        a >>= 1
        b >>= 1
        shift += 1
    
    while (a & 1) == 0: a >>= 1
    
    while b != 0:
        while (b & 1) == 0: b >>= 1
        if a > b: a, b = b, a
        b -= a
    
    return a << shift

def extended_gcd(a, b):
    # extended gcd
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    # mod inverse
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % m + m) % m

def is_prime(n):
    # primality test
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def pollard_rho(n):
    # enhanced pollard rho with brent's algorithm
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3
    
    import random
    
    # try multiple polynomials and starting points
    for c in range(1, 20):
        for start in [2, 3, 5, 7, 11, 13]:
            x = start
            y = start
            d = 1
            
            # brent's cycle detection
            r = 1
            q = 1
            
            while d == 1:
                ys = y
                for _ in range(r):
                    y = (y * y + c) % n
                
                k = 0
                while k < r and d == 1:
                    for _ in range(min(100, r - k)):
                        y = (y * y + c) % n
                        q = (q * abs(x - y)) % n
                        k += 1
                    
                    d = gcd(q, n)
                    
                if d == 1:
                    x = y
                    r *= 2
                
                if d == n:
                    d = 1
                    while d == 1:
                        ys = (ys * ys + c) % n
                        d = gcd(abs(x - ys), n)
            
            if 1 < d < n:
                return d
    
    return None

def trial_division(n, limit=1000000):
    # optimized trial division with wheel
    factors = []
    
    # small primes
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    for p in small_primes:
        while n % p == 0:
            factors.append(p)
            n = n // p
        if n == 1: return factors
        if p > limit or p * p > n: break
    
    # wheel 2*3*5 = 30
    wheel = [4, 6, 10, 12, 16, 18, 22, 24]
    i = 49
    w = 0
    sqrt_n = int(math.sqrt(n)) + 1
    
    while i <= min(sqrt_n, limit):
        while n % i == 0:
            factors.append(i)
            n = n // i
        if n == 1: break
        i += wheel[w]
        w = (w + 1) % 8
    
    if n > 1:
        factors.append(n)
    
    return factors

def pollard_p_minus_1(n, bound=1000000):
    # pollard p-1 method
    a = 2
    for j in range(2, bound):
        a = pow(a, j, n)
        if j % 1000 == 0:  # check periodically
            d = gcd(a - 1, n)
            if 1 < d < n:
                return d
    
    d = gcd(a - 1, n)
    return d if 1 < d < n else None

def fermat_factorization(n, max_iter=100000):
    # fermat method for close primes
    a = int(math.sqrt(n)) + 1
    for _ in range(max_iter):
        b2 = a * a - n
        if b2 >= 0:
            b = int(math.sqrt(b2))
            if b * b == b2:
                p = a + b
                q = a - b
                if p > 1 and q > 1:
                    return min(p, q)
        a += 1
    return None

def factorDB_factorization(n):
    # use factorDB online database
    try:
        f = FactorDB(n)
        f.connect()
        
        # get factors from factorDB
        factors = f.get_factor_list()
        
        if factors and len(factors) >= 2:
            # filter out 1 and n itself, get proper factors
            proper_factors = [factor for factor in factors if factor != 1 and factor != n]
            if len(proper_factors) >= 2:
                return proper_factors[0], n // proper_factors[0]
            elif len(proper_factors) == 1:
                return proper_factors[0], n // proper_factors[0]
        
        return None, None
        
    except Exception as e:
        print(f"FactorDB error: {e}")
        return None, None

def factor_n(n):
    # enhanced factorization with factorDB
    import time
    start_time = time.time()
    print(f"Factoring N = {n}")
    print(f"N has {n.bit_length()} bits")
    
    # method 1: factorDB (try online database first)
    print("Trying FactorDB...")
    factor, cofactor = factorDB_factorization(n)
    if factor and cofactor:
        elapsed = time.time() - start_time
        print(f"FactorDB succeeded in {elapsed:.3f}s")
        return factor, cofactor
    
    # method 2: trial division
    print("Trying trial division...")
    factors = trial_division(n, 1000000)
    if len(factors) >= 2:
        elapsed = time.time() - start_time
        print(f"Trial division succeeded in {elapsed:.3f}s")
        return factors[0], n // factors[0]
    
    # method 3: fermat (for close primes)
    print("Trying Fermat...")
    factor = fermat_factorization(n)
    if factor:
        elapsed = time.time() - start_time
        print(f"Fermat succeeded in {elapsed:.3f}s")
        return factor, n // factor
    
    # method 4: pollard p-1
    print("Trying Pollard P-1...")
    factor = pollard_p_minus_1(n)
    if factor:
        elapsed = time.time() - start_time
        print(f"Pollard P-1 succeeded in {elapsed:.3f}s")
        return factor, n // factor
    
    # method 5: enhanced pollard rho
    print("Trying Enhanced Pollard Rho...")
    factor = pollard_rho(n)
    if factor:
        elapsed = time.time() - start_time
        print(f"Pollard Rho succeeded in {elapsed:.3f}s")
        return factor, n // factor
    
    # failed
    elapsed = time.time() - start_time
    print(f"All methods failed after {elapsed:.3f}s")
    raise ValueError("Can't factor N")

def rsa_decrypt(c, n, e):
    # decrypt rsa
    print("RSA Decrypt")
    print(f"C: {c}")
    print(f"N: {n}")
    print(f"e: {e}")
    print()
    
    try:
        # factor n
        p, q = factor_n(n)
        
        print(f"Factored!")
        print(f"p = {p}")
        print(f"q = {q}")
        print(f"Check: {p * q == n}")
        print()
        
        # calc phi
        phi_n = (p - 1) * (q - 1)
        print(f"phi = {phi_n}")
        
        # calc d
        d = mod_inverse(e, phi_n)
        print(f"d = {d}")
        print()
        
        # decrypt with timing
        import time
        print("Decrypting...")
        start_time = time.time()
        plaintext = pow(c, d, n)  # python's pow is already optimized
        decrypt_time = time.time() - start_time
        print(f"Decryption took {decrypt_time:.3f}s")
        print(f"Number: {plaintext}")
        
        # to text
        try:
            # to bytes
            message_bytes = plaintext.to_bytes((plaintext.bit_length() + 7) // 8, 'big')
            message_text = message_bytes.decode('utf-8', errors='ignore')
            print(f"Text: '{message_text}'")
        except:
            print("Can't convert to text")
        
        return plaintext, d
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def main():
    # params
    C = 62324783949134119159408816513334912534343517300880137691662780895409992760262021
    N = 1280678415822214057864524798453297819181910621573945477544758171055968245116423923
    e = 65537
    
    # decrypt
    plaintext, private_key = rsa_decrypt(C, N, e)
    
    if plaintext is not None:
        print("\nSuccess!")
        print(f"Message: {plaintext}")
        
        # analysis
        print(f"\nAnalysis:")
        print(f"Bit length: {plaintext.bit_length()}")
        print(f"Hex representation: 0x{plaintext:x}")
        
        # encodings
        try:
            # big endian
            byte_length = (plaintext.bit_length() + 7) // 8
            as_bytes = plaintext.to_bytes(byte_length, 'big')
            print(f"Bytes (BE): {as_bytes}")
            print(f"UTF-8: {as_bytes.decode('utf-8', errors='replace')}")
        except:
            pass
            
        try:
            # little endian
            as_bytes_le = plaintext.to_bytes(byte_length, 'little')
            print(f"Bytes (LE): {as_bytes_le}")
            print(f"UTF-8 (LE): {as_bytes_le.decode('utf-8', errors='replace')}")
        except:
            pass
    else:
        print("\nFailed. N too big.")

if __name__ == "__main__":
    main()