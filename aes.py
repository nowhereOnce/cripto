
# Constantes: S-box y Rcon (round constant)
Sbox = [
    # 0     1      2      3      4      5      6      7      8      9      A      B      C      D      E      F
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,  # 0
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,  # 1
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,  # 2
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,  # 3
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,  # 4
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,  # 5
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,  # 6
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,  # 7
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,  # 8
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,  # 9
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,  # A
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,  # B
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,  # C
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,  # D
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,  # E
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16   # F
]

Rcon = [
    0x00,
    0x01, 0x02, 0x04, 0x08,
    0x10, 0x20, 0x40, 0x80,
    0x1B, 0x36,
]


def bytes2matrix(text_bytes):
    """
    Convierte una secuencia de 16 bytes en una matriz 4x4 (estado) por columnas.
    """
    return [list(text_bytes[i:i+4]) for i in range(0, len(text_bytes), 4)]

def matrix2bytes(matrix):
    """
    Convierte una matriz 4x4 (estado) en una secuencia de 16 bytes.
    """
    return bytes(sum(matrix, []))

def xor_bytes(a, b):
    """
    Realiza un XOR entre dos secuencias de bytes.
    """
    return bytes(i ^ j for i, j in zip(a, b))

# La función xtime implementa la multiplicación por 2 (o, equivalentemente,
# por "x" en términos polinomiales) en GF(2⁸). Lo que hace es desplazar el byte un bit a la izquierda; 
# si el bit más significativo estaba activado, se realiza una reducción XOR con el polinomio irreducible 
#  (representado mediante 0x1B en este código) para mantener el resultado dentro del campo GF(2⁸).
def xtime(a):
    """
    Multiplica un byte por 2 en GF(2^8).
    """
    return ((a << 1) ^ 0x1B) & 0xFF if (a & 0x80) else (a << 1) & 0xFF

# mul_by_02 simplemente multiplica el número por 2 usando xtime.
def mul_by_02(num):
    return xtime(num)


# Función SubBytes: aplica la S-box a cada byte del estado.
def sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = Sbox[state[i][j]]
    return state

# Función ShiftRows: rota las filas de la matriz estado.
def shift_rows(state):
    new_state = [row[:] for row in state]
    # Segunda fila: rota 1 a la izquierda
    new_state[1] = state[1][1:] + state[1][:1]
    # Tercera fila: rota 2 a la izquierda
    new_state[2] = state[2][2:] + state[2][:2]
    # Cuarta fila: rota 3 a la izquierda
    new_state[3] = state[3][3:] + state[3][:3]
    return new_state

# Función MixColumns: mezcla cada columna del estado usando operaciones en GF(2^8)
def mix_single_column(a):
    # Para una sola columna (lista de 4 bytes)
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ mul_by_02(a[0] ^ a[1])
    a[1] ^= t ^ mul_by_02(a[1] ^ a[2])
    a[2] ^= t ^ mul_by_02(a[2] ^ a[3])
    a[3] ^= t ^ mul_by_02(a[3] ^ u)
    return a

def mix_columns(state):
    for i in range(4):
        column = [state[0][i], state[1][i], state[2][i], state[3][i]]
        column = mix_single_column(column)
        for j in range(4):
            state[j][i] = column[j]
    return state

# Función add_round_key: realiza XOR entre el estado y la subclave (round key)
def add_round_key(state, round_key):
    # Convertir la subclave (bytes) en matriz 4x4
    key_matrix = bytes2matrix(round_key)
    for i in range(4):
        for j in range(4):
            state[i][j] ^= key_matrix[i][j]
    return state

# Expansión de la clave (Key Expansion)
def key_expansion(key):
    """
    A partir de la clave original (16 bytes) genera una lista de 44 palabras 
    (4 bytes cada una) que se reagrupan en 11 subclaves de 16 bytes cada una.
    """
    Nb = 4       # Número de columnas (estado = 4)
    Nk = 4       # Clave de 128 bits = 4 palabras
    Nr = 10      # Número de rondas para AES-128

    key_columns = bytes2matrix(key)  # Obtiene una matriz 4x4, se interpreta por columnas
    key_schedule = []

    # Forma inicial de las primeras Nk palabras
    for i in range(Nk):
        word = [key_columns[0][i], key_columns[1][i], key_columns[2][i], key_columns[3][i]]
        key_schedule.append(word)

    for i in range(Nk, Nb*(Nr+1)):
        temp = key_schedule[i-1][:]
        if i % Nk == 0:
            # RotWord: rota una palabra (primer byte pasa a ser el último)
            temp = temp[1:] + temp[:1]
            # SubWord: sustituye cada byte mediante la S-box
            temp = [Sbox[b] for b in temp]
            # XOR con Rcon
            temp[0] ^= Rcon[i // Nk]
        # XOR con la palabra Nk posiciones atrás
        word = [a ^ b for a, b in zip(key_schedule[i-Nk], temp)]
        key_schedule.append(word)
    # Convertir la lista de palabras en una lista de subclaves de 16 bytes cada una
    round_keys = []
    for i in range(0, len(key_schedule), 4):
        round_key = []
        for j in range(4):
            round_key.extend(key_schedule[i+j])
        round_keys.append(bytes(round_key))
    return round_keys

# Función que encripta un bloque de 16 bytes
def encrypt_block(plaintext, key):
    """
    plaintext: bytes de 16 bytes.
    key: bytes de 16 bytes.
    """
    assert len(plaintext) == 16
    assert len(key) == 16

    round_keys = key_expansion(key)
    
    state = bytes2matrix(plaintext)

    # Ronda inicial: se añade la subclave inicial
    state = add_round_key(state, round_keys[0])

    # 9 rondas intermedias
    for rnd in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[rnd])
    
    # Ronda final (sin MixColumns)
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[10])
    
    return matrix2bytes(state)

## FUNCIONES PARA DECRYPT

# Tabla inversa de S-box para descifrado
invSbox = [
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
]

# Función para multiplicar en GF(2^8)
def gf_mul(a, b):
    p = 0
    for i in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a = (a << 1) & 0xFF
        if hi_bit_set:
            a ^= 0x1B
        b >>= 1
    return p

# Función inv_sub_bytes: aplica la Inverse S-box a cada byte del estado.
def inv_sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = invSbox[state[i][j]]
    return state

# Función inv_shift_rows: rota las filas en sentido inverso.
def inv_shift_rows(state):
    new_state = [row[:] for row in state]
    new_state[1] = state[1][-1:] + state[1][:-1]  # Rota la segunda fila a la derecha
    new_state[2] = state[2][-2:] + state[2][:-2]  # Rota la tercera fila a la derecha
    new_state[3] = state[3][-3:] + state[3][:-3]  # Rota la cuarta fila a la derecha
    return new_state

# Función inv_mix_columns: aplica la transformación inversa de MixColumns.
def inv_mix_columns(state):
    for i in range(4):
        col = [state[j][i] for j in range(4)]
        state[0][i] = gf_mul(col[0], 0x0e) ^ gf_mul(col[1], 0x0b) ^ gf_mul(col[2], 0x0d) ^ gf_mul(col[3], 0x09)
        state[1][i] = gf_mul(col[0], 0x09) ^ gf_mul(col[1], 0x0e) ^ gf_mul(col[2], 0x0b) ^ gf_mul(col[3], 0x0d)
        state[2][i] = gf_mul(col[0], 0x0d) ^ gf_mul(col[1], 0x09) ^ gf_mul(col[2], 0x0e) ^ gf_mul(col[3], 0x0b)
        state[3][i] = gf_mul(col[0], 0x0b) ^ gf_mul(col[1], 0x0d) ^ gf_mul(col[2], 0x09) ^ gf_mul(col[3], 0x0e)
    return state

# Función decrypt_block: descifra un bloque de 16 bytes.
def decrypt_block(ciphertext, key):
    """
    ciphertext: bytes de 16 bytes.
    key: bytes de 16 bytes.
    """
    assert len(ciphertext) == 16
    assert len(key) == 16

    round_keys = key_expansion(key)
    state = bytes2matrix(ciphertext)

    # Ronda inicial: se añade la última subclave
    state = add_round_key(state, round_keys[10])

    # 9 rondas intermedias
    for rnd in range(9, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, round_keys[rnd])
        state = inv_mix_columns(state)

    # Ronda final (sin inv_mix_columns)
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, round_keys[0])
    
    return matrix2bytes(state)

# Ejemplo de uso:
if __name__ == "__main__":
    # Texto plano (16 bytes) y clave de 16 bytes
    plaintext = b'\x32\x43\xf6\xa8\x88\x5a\x30\x8d\x31\x31\x98\xa2\xe0\x37\x07\x34'
    key = b'\x2b\x7e\x15\x16\x28\xae\xd2\xa6\xab\xf7\x15\x88\x09\xcf\x4f\x3c'
    
    ciphertext = encrypt_block(plaintext, key)
    
    decypted_text = decrypt_block(ciphertext, key)
    
    print("PROYECTO FINAL CRIPTOGRAFÍA\n")
    print("Texto original:", plaintext.hex())
    print("Texto cifrado:", ciphertext.hex())
    print("Texto descifrado:", decypted_text.hex())