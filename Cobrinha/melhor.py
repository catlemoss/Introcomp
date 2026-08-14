# configurações iniciais
import pygame
import random

pygame.init()
pygame.display.set_caption("Jogo da Cobrinha")

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

# parâmetros da cobrinha
tamanho_quadrado = 10

# velocidade inicial
velocidade_jogo = 15

# quantidade de obstáculos
quantidade_obstaculos = 6

# arquivo em que o recorde será guardado
arquivo_recorde = "recorde.txt"


# tenta carregar o recorde salvo
def carregar_recorde():
    try:
        with open(arquivo_recorde, "r") as arquivo:
            return int(arquivo.read())

    except (FileNotFoundError, ValueError):
        return 0

# salva o novo recorde
def salvar_recorde(recorde):
    with open(arquivo_recorde, "w") as arquivo:
        arquivo.write(str(recorde))


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


def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho, tamanho])


def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branco, [pixel[0], pixel[1], tamanho, tamanho])


def desenhar_obstaculos(tamanho, obstaculos):
    for obstaculo in obstaculos:
        pygame.draw.rect(tela, cinza, [obstaculo[0], obstaculo[1], tamanho, tamanho])


def desenhar_pontuacao(pontuacao, recorde, velocidade):
    fonte = pygame.font.SysFont("Helvetica", 22)

    texto = fonte.render(f"Pontos: {pontuacao} | Recorde: {recorde} | Velocidade: {velocidade}", True, amarelo)

    tela.blit(texto, [5, 5])


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


# exibe a tela de fim de jogo
def mostrar_game_over(pontuacao, recorde):
    fonte_titulo = pygame.font.SysFont("Helvetica", 55)
    fonte_texto = pygame.font.SysFont("Helvetica", 28)

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

    recorde = carregar_recorde()
    jogar_novamente = True

    # reiniciar o jogo
    while jogar_novamente:
        fim_jogo = False

        # posição inicial da cobra
        pos_x = largura // 2
        pos_y = altura // 2

        # a cobra começa parada
        velocidade_x = 0
        velocidade_y = 0

        # velocidade atual da partida
        velocidade_atual = velocidade_jogo

        tamanho_cobra = 1

        # começa com a cabeça da cobra
        pixels = [[pos_x, pos_y]]

        obstaculos = gerar_obstaculos(quantidade_obstaculos, pos_x, pos_y)

        comida_x, comida_y = gerar_comida(pixels, obstaculos)

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

            # verifica se bateu nela msm
            for pixel in pixels[:-1]:
                if pixel == [pos_x, pos_y]:
                    fim_jogo = True

            if fim_jogo:
                continue

            # verifica se bateu em algum obstaculo
            if [pos_x, pos_y] in obstaculos:
                fim_jogo = True
                continue

            # comeu a comida
            if pos_x == comida_x and pos_y == comida_y:
                tamanho_cobra += 1

                pontuacao = tamanho_cobra - 1

                # aumenta 1 ponto de velocidade a cada 2 comidas
                velocidade_atual = velocidade_jogo + pontuacao // 2

                # impede que o jogo fique rapido demais kkk
                velocidade_atual = min(velocidade_atual, 30)

                # atualiza e salva o recorde
                if pontuacao > recorde:
                    recorde = pontuacao
                    salvar_recorde(recorde)

                comida_x, comida_y = gerar_comida(pixels, obstaculos)

            # limpa a tela
            tela.fill(preto)

            # desenha os objetos
            desenhar_comida(tamanho_quadrado, comida_x, comida_y)

            desenhar_obstaculos(tamanho_quadrado, obstaculos)

            desenhar_cobra(tamanho_quadrado, pixels)

            desenhar_pontuacao(tamanho_cobra - 1, recorde, velocidade_atual)

            # atualiza a tela
            pygame.display.update()

            # controla a velocidade
            relogio.tick(velocidade_atual)

        pontuacao_final = tamanho_cobra - 1

        jogar_novamente = mostrar_game_over(pontuacao_final, recorde)

    pygame.quit()


rodar_jogo()