# rsa stuff

import math

def gcd(a, b):
    # gcd
    while b:
        a, b = b, a % b
    return a

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
    # pollard rho
    if n % 2 == 0:
        return 2
    
    x = 2
    y = 2
    d = 1
    
    def f(x):
        return (x * x + 1) % n
    
    while d == 1:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
    
    return d if d != n else None

def trial_division(n, limit=1000000):
    # trial division
    factors = []
    
    # check 2
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    
    # check odd
    for i in range(3, min(int(math.sqrt(n)) + 1, limit), 2):
        while n % i == 0:
            factors.append(i)
            n = n // i
    
    if n > 1:
        factors.append(n)
    
    return factors

def factor_n(n):
    # factor n
    print(f"Factoring N = {n}")
    
    # First try trial division for small factors
    factors = trial_division(n, 100000)
    
    if len(factors) >= 2:
        return factors[0], n // factors[0]
    
    # try pollard rho
    print("Trying Pollard Rho...")
    factor = pollard_rho(n)
    
    if factor and factor != n:
        return factor, n // factor
    
    # failed
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
        
        # decrypt
        plaintext = pow(c, d, n)
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