import numpy as np

def char_to_num(char):
    return ord(char) - ord('A')

def num_to_char(num):
    return chr((num % 26) + ord('A'))

def modinv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise Exception("No modular inverse found")

def hill_encrypt(plaintext, key_matrix):
    plaintext = plaintext.upper().replace(" ", "")
    if len(plaintext) % 2 != 0:
        plaintext += 'X'

    ciphertext = ''
    for i in range(0, len(plaintext), 2):
        pair = [char_to_num(plaintext[i]), char_to_num(plaintext[i + 1])]
        result = np.dot(key_matrix, pair) % 26
        ciphertext += ''.join(num_to_char(n) for n in result)
    return ciphertext

def hill_decrypt(ciphertext, key_matrix):
    det = int(np.round(np.linalg.det(key_matrix))) % 26
    det_inv = modinv(det, 26)

    matrix_inv = np.linalg.inv(key_matrix)
    adjugate = np.round(matrix_inv * det).astype(int) % 26
    key_matrix_inv = (det_inv * adjugate) % 26

    plaintext = ''
    for i in range(0, len(ciphertext), 2):
        pair = [char_to_num(ciphertext[i]), char_to_num(ciphertext[i + 1])]
        result = np.dot(key_matrix_inv, pair) % 26
        plaintext += ''.join(num_to_char(int(n)) for n in result)
    return plaintext

# --- MAIN PROGRAM ---
print("HILL CIPHER (2x2)")
message = input("Enter the message (letters only): ").upper()

print("Enter 4 numbers for the 2x2 key matrix (row-wise):")
key_input = input("Example:")
key_nums = list(map(int, key_input.strip().split()))
key_matrix = np.array(key_nums).reshape(2, 2)

try:
    cipher = hill_encrypt(message, key_matrix)
    print("Encrypted message:", cipher)

    show_decryption = input("Do you want to see the decrypted message? (yes/no): ").strip().lower()
    if show_decryption == "yes":
        original = hill_decrypt(cipher, key_matrix)
        print("Decrypted message:", original)

except Exception as e:
    print("Error:", e)
