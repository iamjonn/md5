import struct
import math

# Função de rotação para a esquerda (circular)
def rotaciona_esquerda(x, c):
    return ((x << c) & 0xFFFFFFFF) | (x >> (32 - c))

# Função de preenchimento (padding)
def adiciona_padding(mensagem):
    comprimento_original = len(mensagem) * 8
    mensagem += b'\x80'  # Adiciona o bit 1
    while len(mensagem) % 64 != 56:
        mensagem += b'\x00'  # Preenche com 0s
    mensagem += struct.pack('<Q', comprimento_original)  # Adiciona o comprimento
    return mensagem

# Função de inicialização dos valores MD5
def inicializa_valores():
    return [
        0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476
    ]

# Funções de operação para MD5
def funcao_f(x, y, z):
    return (x & y) | (~x & z)

def funcao_g(x, y, z):
    return (x & z) | (y & ~z)

def funcao_h(x, y, z):
    return x ^ y ^ z

def funcao_i(x, y, z):
    return y ^ (x | ~z)

# Função para gerar as constantes K
def gera_constantes_k():
    return [
        int((2**32) * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)
    ]

# Função para processar cada bloco de 512 bits
def processa_bloco(bloco, h):
    a, b, c, d = h
    k = gera_constantes_k()  # Constantes K
    s = [
        [7, 12, 17, 22], [5, 9, 14, 20], [4, 11, 16, 23], [6, 10, 15, 21]
    ]
    # Dividindo o bloco em palavras de 32 bits
    m = [struct.unpack('<I', bloco[i:i+4])[0] for i in range(0, 64, 4)]

    for i in range(64):
        if 0 <= i <= 15:
            f = funcao_f(b, c, d)
            g = i
            rot = s[0][i % 4]
        elif 16 <= i <= 31:
            f = funcao_g(b, c, d)
            g = (5 * i + 1) % 16
            rot = s[1][i % 4]
        elif 32 <= i <= 47:
            f = funcao_h(b, c, d)
            g = (3 * i + 5) % 16
            rot = s[2][i % 4]
        elif 48 <= i <= 63:
            f = funcao_i(b, c, d)
            g = (7 * i) % 16
            rot = s[3][i % 4]
#01101010 01101111 01101110 
        temp = d
        d = c
        c = b
        b = (b + rotaciona_esquerda((a + f + k[i] + m[g]) & 0xFFFFFFFF, rot)) & 0xFFFFFFFF
        a = temp

    return [
        (h[0] + a) & 0xFFFFFFFF,
        (h[1] + b) & 0xFFFFFFFF,
        (h[2] + c) & 0xFFFFFFFF,
        (h[3] + d) & 0xFFFFFFFF
    ]

# Função principal para calcular o hash MD5
def md5(mensagem):
    mensagem = adiciona_padding(mensagem)
    h = inicializa_valores()

    # Processa os blocos de 512 bits
    for i in range(0, len(mensagem), 64):
        bloco = mensagem[i:i+64]
        h = processa_bloco(bloco, h)

    # Concatena o resultado final
    return ''.join(f'{x:08x}' for x in h)

# Função para comparar com hashlib (verificação de integridade)
def verificar_com_hashlib(mensagem):
    import hashlib
    hash_md5_lib = hashlib.md5(mensagem).hexdigest()
    hash_md5_manual = md5(mensagem)
    return hash_md5_lib == hash_md5_manual

# Testes de exemplo
if __name__ == "__main__":
    exemplo1 = b"Ola Mundo!"
    exemplo2 = b"Ola Mundo?"

    print("Hash MD5 de 'Ola Mundo!':", md5(exemplo1))
    print("Hash MD5 de 'Ola Mundo?':", md5(exemplo2))

    print("\nVerificando integridade com hashlib:")
    print("Hashes iguais? (exemplo1)", verificar_com_hashlib(exemplo1))
    print("Hashes iguais? (exemplo2)", verificar_com_hashlib(exemplo2))

    # Teste de modificação de um único byte
    print("\nAlterando um único byte e verificando a diferença nos hashes:")
    print("Hash de 'Ola Mundo!':", md5(exemplo1))
    print("Hash de 'Ola Mundo?':", md5(exemplo2))


