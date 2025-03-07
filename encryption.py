import base64
import os
import struct
from Crypto.Cipher import DES, AES
from Crypto.Util import Counter

def xor_encrypt_decrypt(data, key):
    key = key.encode() if isinstance(key, str) else key
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def rc4_encrypt_decrypt(data, key):
    key = key.encode() if isinstance(key, str) else key
    S = list(range(256))
    j = 0
    out = bytearray()
    
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    i = j = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(char ^ S[(S[i] + S[j]) % 256])
    
    return bytes(out)

def pad(data, block_size):
    padding_len = block_size - len(data) % block_size
    return data + bytes([padding_len] * padding_len)

def unpad(data):
    return data[:-data[-1]]

def encrypt_file(filename, key, algorithm, mode='ECB'):
    with open(filename, 'rb') as f:
        data = f.read()
    
    if algorithm == 'xor':
        encrypted_data = xor_encrypt_decrypt(data, key)
    elif algorithm == 'rc4':
        encrypted_data = rc4_encrypt_decrypt(data, key)
    else:
        block_size = 8 if algorithm == 'des' else 16
        key = key.ljust(block_size, b'\0')[:block_size]
        
        if mode == 'ECB':
            cipher = DES.new(key, DES.MODE_ECB) if algorithm == 'des' else AES.new(key, AES.MODE_ECB)
            encrypted_data = cipher.encrypt(pad(data, block_size))
        elif mode == 'CBC':
            iv = os.urandom(block_size)
            cipher = DES.new(key, DES.MODE_CBC, iv) if algorithm == 'des' else AES.new(key, AES.MODE_CBC, iv)
            encrypted_data = iv + cipher.encrypt(pad(data, block_size))
        elif mode == 'CTR':
            nonce = os.urandom(8)
            ctr = Counter.new(64, prefix=nonce)
            cipher = DES.new(key, DES.MODE_CTR, counter=ctr) if algorithm == 'des' else AES.new(key, AES.MODE_CTR, counter=ctr)
            encrypted_data = nonce + cipher.encrypt(data)
    
    output_filename = filename + ".enc"
    with open(output_filename, 'wb') as f:
        f.write(encrypted_data)
    
    return output_filename

def encrypt_text(text, key, algorithm, mode='ECB'):
    if algorithm == 'xor':
        return xor_encrypt_decrypt(text, key)
    elif algorithm == 'rc4':
        return rc4_encrypt_decrypt(text, key)
    else:
        block_size = 8 if algorithm == 'des' else 16
        key = key.ljust(block_size, b'\0')[:block_size]
        
        if mode == 'ECB':
            cipher = DES.new(key, DES.MODE_ECB) if algorithm == 'des' else AES.new(key, AES.MODE_ECB)
            return cipher.encrypt(pad(text, block_size))
        # Add CBC and CTR modes similarly
    return text

def decrypt_text(cipher_text, key, algorithm, mode='ECB'):
    if algorithm == 'xor':
        return xor_encrypt_decrypt(cipher_text, key)
    elif algorithm == 'rc4':
        return rc4_encrypt_decrypt(cipher_text, key)
    else:
        block_size = 8 if algorithm == 'des' else 16
        key = key.ljust(block_size, b'\0')[:block_size]
        
        if mode == 'ECB':
            cipher = DES.new(key, DES.MODE_ECB) if algorithm == 'des' else AES.new(key, AES.MODE_ECB)
            return unpad(cipher.decrypt(cipher_text))
        # Add CBC and CTR modes similarly
    return cipher_text


def decrypt_file(filename, key, algorithm, mode='ECB'):
    with open(filename, 'rb') as f:
        data = f.read()
    
    if algorithm == 'xor':
        decrypted_data = xor_encrypt_decrypt(data, key)
    elif algorithm == 'rc4':
        decrypted_data = rc4_encrypt_decrypt(data, key)
    else:
        block_size = 8 if algorithm == 'des' else 16
        key = key.ljust(block_size, b'\0')[:block_size]
        
        if mode == 'ECB':
            cipher = DES.new(key, DES.MODE_ECB) if algorithm == 'des' else AES.new(key, AES.MODE_ECB)
            decrypted_data = unpad(cipher.decrypt(data))
        elif mode == 'CBC':
            iv = data[:block_size]
            cipher = DES.new(key, DES.MODE_CBC, iv) if algorithm == 'des' else AES.new(key, AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(data[block_size:]))
        elif mode == 'CTR':
            nonce = data[:8]
            ctr = Counter.new(64, prefix=nonce)
            cipher = DES.new(key, DES.MODE_CTR, counter=ctr) if algorithm == 'des' else AES.new(key, AES.MODE_CTR, counter=ctr)
            decrypted_data = cipher.decrypt(data[8:])
    
    output_filename = filename.replace(".enc", ".dec")
    with open(output_filename, 'wb') as f:
        f.write(decrypted_data)
    
    return output_filename
