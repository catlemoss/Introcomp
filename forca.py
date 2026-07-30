from palavraForca import palavra

letras_user = []
chances = 4
ganhou = False

while True:
    # criar nossa logica
    print(f"Você tem {chances} chances.")

    for letra in palavra:
        if letra.lower() in letras_user:
            print(letra, end = " ") 
        else:
            print("_", end = " ")

    print("")
    tentativa = input("Escolha uma letra para adivinhar: ")
    letras_user.append(tentativa.lower())
    if tentativa.lower() not in palavra.lower():
        chances -= 1

    ganhou = True
    for letra in palavra:
        if letra.lower() not in letras_user:
            ganhou = False

    if chances == 0 or ganhou:
        break


if ganhou:
    print("Parabéns, você ganhou o jogo!")
    print("A palavra era:", palavra)
else:
    print("Você perdeu... A palavra era:", palavra)