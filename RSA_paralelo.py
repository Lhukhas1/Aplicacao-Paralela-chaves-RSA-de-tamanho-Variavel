from mpi4py import MPI
from Cryptodome.Util import number
import os
import sys

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
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    quantProcessos = comm.Get_size()
    
    if rank == 0:
        inicio = MPI.Wtime()
        print(f"RSA -> Paralelo: {NUMERO_DE_CHAVES} chaves com {TAMANHO_BITS} bits\n")
        print(f"Quantidade de Processos: {quantProcessos}\n")
        sys.stdout.flush()
    
    # Quantas chaves cada processo vai gerar
    quantChavesProcesso = NUMERO_DE_CHAVES // quantProcessos
    chavesSobraram = NUMERO_DE_CHAVES % quantProcessos
    
    # Os primeiros processos pegam as que sobraram
    if rank < chavesSobraram:
        num_chaves = quantChavesProcesso + 1
        offset = rank * num_chaves
    else:
        num_chaves = quantChavesProcesso
        offset = chavesSobraram * (quantChavesProcesso + 1) + \
                 (rank - chavesSobraram) * quantChavesProcesso
    
    # Cada processo gera suas chaves
    chavesGeradas = []
    for i in range(num_chaves):
        n, e, d = gerarChaveRSA(TAMANHO_BITS)
        chavesGeradas.append((n, e, d))
        print(f"Processo {rank}: chave {offset + i + 1}/{NUMERO_DE_CHAVES} gerada")
        sys.stdout.flush()
    
    # Coletando todas as chaves no processo raiz
    todasChaves = comm.gather(chavesGeradas, root=0)
    
    # Remove arquivo anterior
    if rank == 0:
        if os.path.exists("Chaves_RSA_paralelo.txt"):
            os.remove("Chaves_RSA_paralelo.txt")
        
        with open("Chaves_RSA_paralelo.txt", 'w', encoding='utf-8') as arquivo:
            chaveNum = 1
            for rank_id, chaves in enumerate(todasChaves):
                for n, e, d in chaves:
                    arquivo.write(f"Chave {chaveNum} (N, E, D):\n")
                    arquivo.write(f"N:({n})\nE:({e})\nD:({d})\n\n")
                    chaveNum += 1
        
        fim = MPI.Wtime()
        tempoTotal = fim - inicio
        print(f"Todas as {NUMERO_DE_CHAVES} chaves geradas em {tempoTotal:.3f} segundos.")

if __name__ == "__main__":
    main()