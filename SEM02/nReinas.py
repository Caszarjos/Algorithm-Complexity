
def comprobar(reinas, cant, etapa):
    i = 0
    while i < etapa:
        if (reinas[i] == reinas[etapa]) or (abs(etapa-i) == abs(reinas[etapa]-reinas[i])):
            return False
        i = i + 1
    return True



def Nreinas(reinas, cant, etapa):
    if(etapa == cant):
        print("Reinas: ", reinas)
    else:
        reinas[etapa] = 0
        while(reinas[etapa] < cant):
            if (comprobar(reinas, cant, etapa)):
                Nreinas(reinas, cant, etapa + 1)
            reinas[etapa] = reinas[etapa] + 1


def main():
    etapa = 0
    cant = 5

    reinas = []
    for i in range(cant):
        reinas.append(-1)
    Nreinas(reinas,cant,etapa)

main()