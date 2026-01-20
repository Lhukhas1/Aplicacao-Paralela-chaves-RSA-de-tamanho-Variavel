from Cryptodome.Util import number
import os

NUMERO_DE_CHAVES = 10
TAMANHO_BITS = 4096  

def gerarChaveRSA(tamanho_bits):
    # 1:  Dois numeros primos gigantes, p e q
    p = number.getPrime(tamanho_bits // 2)
    q = number.getPrime(tamanho_bits // 2)
    
    # p e q precisa ser diferentes
    while p == q:
        q = number.getPrime(tamanho_bits // 2)
    
    # 2:  n = p * q
    n = p * q
    
    # Calcular phi = (p - 1)(q - 1)
    phi = (p - 1) * (q - 1)
    
    # 3: Expoente publico e
    e = 65537
    
    # Calcular inversa modular (d = e^(-1) mod phi)
    d = pow(e, -1, phi)
    
    return (n, e, d)


def main():
    print(f"RSA -> Sequencial: {NUMERO_DE_CHAVES} com {TAMANHO_BITS} bits\n")
    
    # Remove arquivo anterior
    if os.path.exists("Chaves_RSA_sequencial.txt"):
        os.remove("Chaves_RSA_sequencial.txt")
    

    with open("Chaves_RSA_sequencial.txt", 'w', encoding='utf-8') as arquivo:
        for i in range(0, NUMERO_DE_CHAVES):
    
            n, e, d = gerarChaveRSA(TAMANHO_BITS)
            print(f"Chave {i + 1} gerada.")
            arquivo.write(f"Chave {i + 1} (N, E, D):\n")
            arquivo.write(f"N:({n})\nE:({e})\nD:({d})\n\n")

        
    print(f"\nTodas as {NUMERO_DE_CHAVES} geradas e salvas.")

if __name__ == "__main__":
    main()