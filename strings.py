texto = "Catarina"

print(texto)
print(f"Primeira letra: {texto[0]}")    # P
print(f"Última letra: {texto[-1]}")     # n

# tamanho
print(f"Sua palavra tem {len(texto)} letras")
print("")

# utilidades
texto.lower()               # tudo minúsculo
texto.upper()               # tudo maiúsculo
texto.strip()               # remove espaços das extremidades
texto.replace("a", "x")
texto.split()               # separa em palavras

nome = input("Escreva um nome: ").strip()
if nome.lower() == "catarina":
    print("Nome encontrado")
else:
    print("Nome errado")

# percorrendo uma string
palavra = "Catarina"
for letra in palavra:
    print(letra, end = " ")
print("")

# contando VOGAIS
palavra = input("Escreva uma palavra: ")
quantidade = 0
for letra in palavra.lower():
    if letra in "aeiou":
        quantidade += 1
# O in verifica se algo está dentro de outra coisa
print(f"Sua palavra tem {quantidade} vogais.")