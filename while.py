contador = 1

while contador <= 5:
    print(contador, end = " ")
    contador += 1
print("")
# nao tem contador++ em python T^T

# Lendo numeros até aparecer o 0:
numero = int(input("Escreva um número: "))

while numero != 0:
    print("Você digitou:", numero)
    numero = int(input("Escreva um número: "))

    if numero == 0:
        print("Saindo...")