listaProdutos = ["celular", "radio", "notebook"]
listaPrecos = [1500, 5000, 5500]

for produto in listaProdutos:
    print(produto)
print("")

# aqui demos um nome para os itens da nossa lista
# assim ele pirnta cada item da lista que é o vetor


# for normal
for i in range(2):
    print("Catarina", end = " ")
print("")

# for normal com i
for i in range(5):
    print(i, end = " ")
print("")

# for até 5 com ele incluso
for i in range(1, 6):
    print(i, end = " ")
print("")

# for int i = 0; i < 11; i+2
for i in range(0, 11, 2):
    print(i, end = " ")
print("")

# contagem regressiva
# for int i = 10; i > 0; i--
for i in range(10, 0, -1):
    print(i, end = " ")
print("")

# SOMANDO NÚMEROS
soma = 0
for i in range(1, 6):
    soma += i
print(soma)
print("")

# TABUADA
numero = int(input("Insira um número: "))
for i in range(1, 11):
    print(f"{numero} x {i} = {numero*i}")