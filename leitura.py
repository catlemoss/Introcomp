# LENDO UMA INFO

# Em Python, input() sempre devolve uma string.
nome = input("Digite seu nome: ")
print(f"Olá, {nome}.")

# Para ler um inteiro:
idade = int(input("Digite sua idade: "))
print(f"{nome} tem {idade} anos.")

# Para ler um número decimal:
altura = float(input("Digite sua altura em cm: "))
print(f"{nome} tem {idade} anos e tem {altura} cm de altura.")

print("") # acho q isso é o nosso \n né

# LENDO DOIS NUMEROS NA MSM LINHA

entrada = input("Digite dois números: ")    # "10 20"
partes = entrada.split()                    # ["10", "20"]

a = int(partes[0])
b = int(partes[1])

print(f"A soma dos números é: {a+b}.")