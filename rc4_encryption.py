# rc4 stuff

def rc4_ksa(key):
    # ksa
    # key to bytes
    if isinstance(key, str):
        key = key.encode('utf-8')
    
    # init s-box
    S = list(range(256))
    j = 0
    
    # do stuff
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        # swap
        S[i], S[j] = S[j], S[i]
    
    return S

def rc4_prga(S, plaintext):
    # prga
    # text to bytes
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')
    
    i = j = 0
    ciphertext = []
    
    for byte in plaintext:
        # update
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        
        # swap
        S[i], S[j] = S[j], S[i]
        
        # keystream
        keystream_byte = S[(S[i] + S[j]) % 256]
        
        # xor
        cipher_byte = byte ^ keystream_byte
        ciphertext.append(cipher_byte)
    
    return bytes(ciphertext)

def rc4_encrypt_decrypt(key, text):
    # encrypt/decrypt
    S = rc4_ksa(key)
    result = rc4_prga(S, text)
    return result

def main():
    # name
    name = "Umer Baig"
    
    # key
    key = "mySecretKey123"
    
    print("RC4")
    print(f"Name: {name}")
    print(f"Key: {key}")
    
    # encrypt
    encrypted = rc4_encrypt_decrypt(key, name)
    
    print("Encrypted:")
    print(f"Hex: {encrypted.hex()}")
    print(f"Bytes: {list(encrypted)}")
    
    # decrypt
    decrypted = rc4_encrypt_decrypt(key, encrypted)
    decrypted_text = decrypted.decode('utf-8')
    
    print("Decrypted:")
    print(f"Result: {decrypted_text}")
    print(f"Match: {decrypted_text == name}")
    
    # ascii
    print("ASCII:")
    print(f"Original: {[ord(c) for c in name]}")
    print(f"Encrypted: {list(encrypted)}")

if __name__ == "__main__":
    main()