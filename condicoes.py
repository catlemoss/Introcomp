# uma condição:
idade = int(input("Idade: "))

if idade >= 18:
    print("Maior de idade")
else:
    print("Menor de idade")

# mais condições:
nota = float(input("Nota: "))

if nota >= 7:
    print("Aprovado")
elif nota >= 5:
    print("Final")
else:
    print("Reprovado")

'''
and   # &&
or    # ||
not   # !
'''

idade = int(input("Qual sua idade: "))
tem_ingresso = True

if idade >= 18 and tem_ingresso:
    print("Pode entrar")