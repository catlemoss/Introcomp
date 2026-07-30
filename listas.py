# Lista é semelhante a um vetor, mas pode crescer facilmente.

numeros = [10, 20, 30, 40]

# positions
print(numeros[0])   # 10
print(numeros[1])   # 20
print(numeros[2])   # 30
print(numeros[-1])  # 40, último elemento

# tamanho
print(f"Qnt num na lista: {len(numeros)}")

# add num na lista
numeros.append(50)

# remov num da 
numeros.remove(20)

# percorre valores
for numero in numeros:
    print(numero, end = " ")
print("")

# percorre os índices
for i in range(len(numeros)):
    print(f"Posição: {i}, Num: {numeros[i]}")


# CRIANDO UMA LISTA PELA ENTRADA PADRÃO

numeros = list(map(int, input("Insira seus números: ").split()))

print(numeros)          # printa a lista
print(numeros[3])       # numero na posição tal
print(sum(numeros))     # soma dos numeros na lista
print(max(numeros))     # maior numero
print(min(numeros))     # menor numero

'''
len(numeros)  # quantidade
sum(numeros)  # soma
max(numeros)  # maior
min(numeros)  # menor
'''