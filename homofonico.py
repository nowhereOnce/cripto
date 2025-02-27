import random

tabla_homofonica = {
    'a': ['000010', '000101', '000001'],
    'b': ['000111', '000000'],
    'c': ['001100', '010111'],
    'd': ['001001'],
    'e': ['001010', '011010'],
    'f': ['000011', '001101', '011110'],
    'g': ['000110', '010010'],
    'h': ['001000'],
    'i': ['001111'],
    'j': ['011011'],
    'k': ['010011'],
    'l': ['000100', '010100'],
    'm': ['010001', '011101'],
    'n': ['100000', '101000'],
    'o': ['001110'],
    'p': ['011001'],
    'q': ['100001'],
    'r': ['100010'],
    's': ['010000', '011000'],
    't': ['100011'],
    'u': ['001011', '010110'],
    'v': ['100100'],
    'w': ['011100'],
    'x': ['100101'],
    'y': ['100111'],
    'z': ['010101'],
    ' ': ['011111']
}

def cifrar(mensaje):
    mensaje = mensaje.lower()
    mensaje_cifrado = ''
    for letra in mensaje:
        if letra in tabla_homofonica:
            random_index = random.randint(0, len(tabla_homofonica[letra]) - 1)
            cifrado = tabla_homofonica[letra][random_index]
            mensaje_cifrado += cifrado
    return mensaje_cifrado

def ordenar(mensaje_cifrado):
    ordenado = []
    bits = ''
    conta = 0
    for bit in mensaje_cifrado:
        if conta == 6:
            ordenado.append(bits)
            bits = ''
            bits += bit
            conta = 1
        else:
            bits += bit
            conta += 1
    ordenado.append(bits)
    return ordenado
        

def descifrar(mensaje_cifrado):
    grupos = ordenar(mensaje_cifrado)
    mensaje_descifrado = ''
    for grupo in grupos:
        # Busca en la tabla la letra cuyo código (dentro de su lista) coincida con el grupo actual
        for letra, codigos in tabla_homofonica.items():
            if grupo in codigos:
                mensaje_descifrado += letra
                break
    return mensaje_descifrado

# # Impresión de la tabla homofónica (es necesario instalar la librería tabulate)
# # pip install tabulate
# from tabulate import tabulate
# # Convertir el diccionario en una lista de listas para tabulate
# tabla = [[letra, ", ".join(valores)] for letra, valores in tabla_homofonica.items()]
# # Encabezados de la tabla
# encabezados = ["Letra", "Valores Binarios"]
# # Imprimir la tabla
# print(tabulate(tabla, headers=encabezados, tablefmt="grid"))

mensaje = 'este es un mensaje secreto'

print("Mensaje original: ", mensaje)
mensaje_cifrado = cifrar(mensaje)
print("Mensaje cifrado: ", mensaje_cifrado)
mensaje_descifrado = descifrar(mensaje_cifrado)
print("Mensaje descifrado: ", mensaje_descifrado)


    