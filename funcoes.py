# com retorno
def soma(a, b):
    resultado = a + b
    return resultado

valor = soma(10, 20)
print(valor)

# sem retorno
def cumprimentar(nome):
    print("Olá,", nome)

cumprimentar("Catarina")

def maior(a, b):
    return max(a, b)

numeros = input("Digite dois números: ")
partes = numeros.split()

a = int(partes[0])
b = int(partes[1])

biggest = maior(a, b)

print(f"O maior número é: {biggest}.")

