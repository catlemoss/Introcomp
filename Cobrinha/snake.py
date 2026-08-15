import pygame
import random

# inicialização do pygame
pygame.init()
pygame.display.set_caption("SNAKE: not alone")

# tamanho da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))

# controla a velocidade do jogo
relogio = pygame.time.Clock()

# cores RGB
preto = (0, 0, 0)
branco = (255, 255, 255)
amarelo = (255, 255, 0)
verde = (0, 255, 0)
vermelho = (255, 0, 0)
cinza = (100, 100, 100)
roxo = (160, 32, 240)

# parâmetros da cobrinha
tamanho_quadrado = 10

# velocidade inicial
velocidade_jogo = 15

# quantidade de obstáculos
quantidade_obstaculos = 9

# arquivo em que o recorde será guardado
arquivo_recorde = "recorde.txt"

# pontuacao para o shadow
pontos_4_shadow = 2

# lidando com o record
def carregar_recorde():
    try:
        with open(arquivo_recorde, "r") as arquivo:
            conteudo = arquivo.read().strip()

        if "," in conteudo:
            nome, pontos = conteudo.rsplit(",", 1)
            return nome, int(pontos)

        # caso o recorde.txt antigo tenha somente um número
        return "Ninguém", int(conteudo)

    except (FileNotFoundError, ValueError):
        return "---", 0

def salvar_recorde(nome, recorde):
    with open(arquivo_recorde, "w") as arquivo:
        arquivo.write(f"{nome},{recorde}")


# gera uma posiçao aleatoria alinhada com os quadrados
def gerar_posicao_aleatoria():
    pos_x = random.randrange(0, largura, tamanho_quadrado)
    pos_y = random.randrange(0, altura, tamanho_quadrado)

    return pos_x, pos_y


# gera a comida em uma posiçao livre
def gerar_comida(pixels, obstaculos):
    while True:
        comida_x, comida_y = gerar_posicao_aleatoria()

        posicao_comida = [comida_x, comida_y]

        # a comida nao pode aparecer na cobra nem nos obstaculos
        if posicao_comida not in pixels and posicao_comida not in obstaculos:
            return comida_x, comida_y


# cria os obstaculos do jogo
def gerar_obstaculos(quantidade, inicio_x, inicio_y):
    obstaculos = []

    while len(obstaculos) < quantidade:
        obstaculo_x, obstaculo_y = gerar_posicao_aleatoria()

        novo_obstaculo = [obstaculo_x, obstaculo_y]

        # impede obstaculos repetidos
        # e evita criar obstaculos muito perto da posição inicial
        longe_do_inicio = (
            abs(obstaculo_x - inicio_x) > 80
            or abs(obstaculo_y - inicio_y) > 80
        )

        if novo_obstaculo not in obstaculos and longe_do_inicio:
            obstaculos.append(novo_obstaculo)

    return obstaculos

def gerar_shadow(pixels, obstaculos):
    while True:
        shadow_x, shadow_y = gerar_posicao_aleatoria()

        posicao_shadow = [shadow_x, shadow_y]

        # não pode nascer na cobra nem em obstáculo
        if posicao_shadow in pixels or posicao_shadow in obstaculos:
            continue

        # cabeça da cobra
        cabeca_x, cabeca_y = pixels[-1]

        # evita o shadow nascer colado na cobra
        distancia = abs(shadow_x - cabeca_x) + abs(shadow_y - cabeca_y)

        if distancia >= 250:
            return shadow_x, shadow_y

# DESENHOS
def desenhar_comida(comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho_quadrado, tamanho_quadrado])

def desenhar_cobra(pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branco, [pixel[0], pixel[1], tamanho_quadrado, tamanho_quadrado])

def desenhar_obstaculos(obstaculos):
    for obstaculo in obstaculos:
        pygame.draw.rect(tela, cinza, [obstaculo[0], obstaculo[1], tamanho_quadrado, tamanho_quadrado])

def desenhar_pontuacao(pontuacao, recorde, velocidade):
    fonte = pygame.font.SysFont("Consolas", 22)

    texto = fonte.render(f"Pontos: {pontuacao} | Recorde: {recorde} | Velocidade: {velocidade}", True, amarelo)

    tela.blit(texto, [5, 5])

# shadow snake
def desenhar_shadow(shadow_x, shadow_y):
    pygame.draw.rect(tela, roxo, [shadow_x, shadow_y, tamanho_quadrado, tamanho_quadrado])

def desenhar_olho_shadow(x, y, abertura, angulo):
    largura_olho = 100
    altura_maxima = 40

    altura_olho = max(1, int(altura_maxima * abertura))

    # cria uma superficie transparente para o desenho
    superficie_olho = pygame.Surface((largura_olho, altura_maxima), pygame.SRCALPHA)

    # olho roxo
    pygame.draw.ellipse(superficie_olho, roxo,
        [
            0,
            altura_maxima // 2 - altura_olho // 2,
            largura_olho,
            altura_olho
        ]
    )

    # pupila de gato
    if abertura > 0.3:
        altura_pupila = int(altura_olho * 0.8)

        pygame.draw.ellipse(superficie_olho, preto,
            [
                largura_olho // 2 - 5,
                altura_maxima // 2 - altura_pupila // 2,
                10,
                altura_pupila
            ]
        )

    # gira o olho
    olho_rotacionado = pygame.transform.rotate(superficie_olho, angulo)
    rect = olho_rotacionado.get_rect(center = (x, y))

    tela.blit(olho_rotacionado, rect)

def desenhar_olhos_shadow(abertura):
    desenhar_olho_shadow(largura // 2 - 100, altura // 2, abertura, -15)
    desenhar_olho_shadow(largura // 2 + 100, altura // 2, abertura, 15)


# seleciona a direção da cobra
def selecionar_deslocamento(tecla, velocidade_x, velocidade_y):

    if tecla == pygame.K_DOWN and velocidade_y == 0:
        velocidade_x = 0
        velocidade_y = tamanho_quadrado

    elif tecla == pygame.K_UP and velocidade_y == 0:
        velocidade_x = 0
        velocidade_y = -tamanho_quadrado

    elif tecla == pygame.K_RIGHT and velocidade_x == 0:
        velocidade_x = tamanho_quadrado
        velocidade_y = 0

    elif tecla == pygame.K_LEFT and velocidade_x == 0:
        velocidade_x = -tamanho_quadrado
        velocidade_y = 0

    return velocidade_x, velocidade_y

def mover_shadow(shadow_x, shadow_y, cobra_x, cobra_y):

    # Se distancia_x > 0 = cobra a direita
    # Se < 0: cobra a esquerda

    distancia_x = cobra_x - shadow_x
    distancia_y = cobra_y - shadow_y

    # distância maior = shadow snake anda
    if abs(distancia_x) > abs(distancia_y):
        if distancia_x > 0:
            shadow_x += tamanho_quadrado

        elif distancia_x < 0:
            shadow_x -= tamanho_quadrado

    else:
        if distancia_y > 0:
            shadow_y += tamanho_quadrado

        elif distancia_y < 0:
            shadow_y -= tamanho_quadrado

    return shadow_x, shadow_y


# exibe a tela de fim de jogo
def mostrar_game_over(pontuacao, recorde):
    fonte_titulo = pygame.font.SysFont("Consolas", 55)
    fonte_texto = pygame.font.SysFont("Consolas", 28)

    while True:
        tela.fill(preto)

        # prints
        titulo = fonte_titulo.render("GAME OVER", True, vermelho)
        texto_pontos = fonte_texto.render(f"Pontuação: {pontuacao}", True, branco)
        texto_recorde = fonte_texto.render(f"Recorde: {recorde}", True, amarelo)
        texto_reiniciar = fonte_texto.render("Pressione R para jogar novamente", True, branco)
        texto_sair = fonte_texto.render("Pressione Q ou ESC para sair", True, branco)

        # positions
        tela.blit(titulo, [largura / 2 - titulo.get_width() / 2, 150])
        tela.blit(texto_pontos, [largura / 2 - texto_pontos.get_width() / 2, 240])
        tela.blit(texto_recorde, [largura / 2 - texto_recorde.get_width() / 2, 280])
        tela.blit(texto_reiniciar, [largura / 2 - texto_reiniciar.get_width() / 2, 350])
        tela.blit(texto_sair, [largura / 2 - texto_sair.get_width() / 2, 390])

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True

                if evento.key == pygame.K_q or evento.key == pygame.K_ESCAPE:
                    return False

        relogio.tick(15)

# main mais ou menos
def rodar_jogo():

    nome_jogador = pedir_nome()
    nome_recorde, recorde = carregar_recorde()
    jogar_novamente = True

    # reiniciar o jogo
    while jogar_novamente:
        fim_jogo = False

        # cobra no meio
        pos_x = largura // 2
        pos_y = altura // 2

        # cobra começa parada
        velocidade_x = 0
        velocidade_y = 0

        # velocidade atual da partida
        velocidade_atual = velocidade_jogo

        tamanho_cobra = 1

        # começa com a cabeça da cobra
        pixels = [[pos_x, pos_y]]

        obstaculos = gerar_obstaculos(quantidade_obstaculos, pos_x, pos_y)
        comida_x, comida_y = gerar_comida(pixels, obstaculos)

        # shadow ainda não existe
        shadow_ativo = False
        shadow_x = 0
        shadow_y = 0
        velocidade_shadow = 0

        while not fim_jogo:

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return

                if evento.type == pygame.KEYDOWN:
                    velocidade_x, velocidade_y = selecionar_deslocamento(evento.key, velocidade_x, velocidade_y)

            # atualiza a posição da cabeça
            pos_x += velocidade_x
            pos_y += velocidade_y

            # bateu na parede
            if (pos_x < 0 or pos_x >= largura or pos_y < 0 or pos_y >= altura):
                fim_jogo = True
                continue

            # adiciona a nova posição da cabeça
            pixels.append([pos_x, pos_y])

            # remove a posição mais antiga
            if len(pixels) > tamanho_cobra:
                del pixels[0]

            # verifica se bateu nela menos a cabeça
            for pixel in pixels[:-1]:
                if pixel == [pos_x, pos_y]:
                    fim_jogo = True

            # verifica se bateu em algum obstaculo
            if [pos_x, pos_y] in obstaculos:
                fim_jogo = True
                continue

            if fim_jogo:
                continue

            # comeu a comida
            if pos_x == comida_x and pos_y == comida_y:
                tamanho_cobra += 1

                pontuacao = tamanho_cobra - 1

                # aumenta 1 ponto de velocidade a cada 3 comidas
                velocidade_atual = velocidade_jogo + pontuacao // 3

                # impede que o jogo fique rapido demais kkk
                velocidade_atual = min(velocidade_atual, 30)

                # atualiza e salva o recorde
                if pontuacao > recorde:
                    recorde = pontuacao
                    nome_recorde = nome_jogador
                    salvar_recorde(nome_recorde, recorde)

                comida_x, comida_y = gerar_comida(pixels, obstaculos)


            # introducao do shadow quando tiver n pnts
            pontuacao = tamanho_cobra - 1

            if pontuacao >= pontos_4_shadow and not shadow_ativo:
                mostrar_shadow_snake(nome_jogador)

                shadow_x, shadow_y = gerar_shadow(pixels, obstaculos)
                shadow_ativo = True

            if shadow_ativo:
                velocidade_shadow += 1

                # velocidade do shadow ++ a cada 7 pnts
                movimentos = (pontuacao - pontos_4_shadow) // 7
                intervalo_shadow = max(1, 4 - movimentos)

                if velocidade_shadow >= intervalo_shadow:
                    shadow_x, shadow_y = mover_shadow(shadow_x, shadow_y, pos_x, pos_y)

                    velocidade_shadow = 0

                # shadow pegou a cobra
                if [shadow_x, shadow_y] in pixels:
                    fim_jogo = True
                    continue

            # limpa a tela
            tela.fill(preto)

            # desenha os objetos
            desenhar_comida(comida_x, comida_y)
            desenhar_obstaculos(obstaculos)

            if shadow_ativo:
                desenhar_shadow(shadow_x, shadow_y)

            desenhar_cobra(pixels)
            desenhar_pontuacao(tamanho_cobra - 1, recorde, velocidade_atual)

            # atualiza a tela
            pygame.display.update()

            # controla a velocidade
            relogio.tick(velocidade_atual)

        pontuacao_final = tamanho_cobra - 1
        jogar_novamente = mostrar_game_over(pontuacao_final, recorde)

    pygame.quit()


def pedir_nome():

    nome = ""

    fonte_titulo = pygame.font.SysFont("Consolas", 45)
    fonte_texto = pygame.font.SysFont("Consolas", 28)

    while True:

        tela.fill(preto)

        titulo = fonte_titulo.render("SNAKE: not alone", True, amarelo)
        instrucao = fonte_texto.render("Digite seu nome:", True, branco)
        nome_na_tela = fonte_texto.render(nome, True, branco)
        continuar = fonte_texto.render("Pressione ENTER para jogar", True, cinza)

        tela.blit(titulo, [largura / 2 - titulo.get_width() / 2, 150])
        tela.blit(instrucao, [largura / 2 - instrucao.get_width() / 2, 240])

        # caixa onde aparece o nome
        caixa = pygame.Rect(largura / 2 - 150, 290, 300, 45)
        pygame.draw.rect(tela, branco, caixa, 2)
        tela.blit(nome_na_tela, [caixa.x + 10, caixa.y + 7])
        tela.blit(continuar, [largura / 2 - continuar.get_width() / 2, 370])

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None

            if evento.type == pygame.KEYDOWN:

                # apagar
                if evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]

                # começar jogo
                elif evento.key == pygame.K_RETURN:
                    if nome.strip() != "":
                        return nome.strip()
                    
                # digitar
                else:
                    if len(nome) < 15:
                        nome += evento.unicode
                        # qualquer caractere digitado

        relogio.tick(30)

# cutscene do shadow snake kkkk
def mostrar_shadow_snake(nome_jogador):

    fonte_grande = pygame.font.SysFont("Impact", 42, bold = True)
    fonte_media = pygame.font.SysFont("Consolas", 28)
    fonte_shadow = pygame.font.SysFont("Impact", 45)

    # retorna o tempo
    inicio = pygame.time.get_ticks()
    duracao_total = 11000

    while True:
        tempo = pygame.time.get_ticks() - inicio

        if tempo >= duracao_total:
            return True

        tela.fill(preto)

        # mensagem inicial
        if tempo < 2000:
            texto = fonte_grande.render("VOCÊ NÃO ESTÁ MAIS SOZINHO...", True, vermelho)
            tela.blit(texto, [largura // 2 - texto.get_width() // 2, altura // 2 - 30])

        # tela completamente preta
        elif tempo < 2700:
            pass

        # olhos se abrindo
        elif tempo < 5200:
            # número entre 0 e 1
            progresso = (tempo - 2700) / 2500
            abertura = progresso **2                # aumento de velocidade pot2
            desenhar_olhos_shadow(abertura)

        # olhos abertos
        elif tempo < 6200:
            desenhar_olhos_shadow(1)

        elif tempo < 8400:
            desenhar_olhos_shadow(1)
            texto_nome = fonte_media.render(f"Cuidado, {nome_jogador}.", True, branco)

            tela.blit(texto_nome, [largura // 2 - texto_nome.get_width() // 2, altura - 150])

        else:
            desenhar_olhos_shadow(1)
            texto_nome = fonte_media.render(f"Cuidado, {nome_jogador}.", True, branco)
            texto_shadow = fonte_shadow.render("SHADOW SNAKE ESTÁ ATRÁS DE VOCÊ", True, vermelho)

            tela.blit(texto_nome, [largura // 2 - texto_nome.get_width() // 2, altura - 150])
            tela.blit(texto_shadow, [largura // 2 - texto_shadow.get_width() // 2, altura - 100])

        pygame.display.update()
        relogio.tick(60) # animação suave dos olhos do shadow

rodar_jogo()