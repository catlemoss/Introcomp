# configurações iniciais
import pygame
import random

pygame.init()                                       # para ligar o pygame
pygame.display.set_caption("Jogo da Cobrinha")      # tela

largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))

# tempo do loop
relogio = pygame.time.Clock()

# cores RGB
preto = (0, 0, 0)
branca = (255, 255, 255)
amarelo = (255, 255, 0)
verde = (0, 255, 0)

# parametros da cobrinha
tamanho_quadrado = 10
velocidade_jogo = 15                 # quanto ela anda a cada clock

# gera quadrados aleatorios
def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado) / tamanho_quadrado) * tamanho_quadrado

    comida_y = round(random.randrange(0, altura - tamanho_quadrado) / tamanho_quadrado) * tamanho_quadrado

    return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("Helvetica", 25)
    texto = fonte.render(f"Pontos: {pontuacao}", True, amarelo) 
    # true = normal, false = texto em pixel
    tela.blit(texto, [2, 2])

def selecionar_deslocamento(tecla):
    if tecla == pygame.K_DOWN:
        velocidade_x = 0
        velocidade_y = tamanho_quadrado

    elif tecla == pygame.K_UP:
            velocidade_x = 0
            velocidade_y = -tamanho_quadrado

    elif tecla == pygame.K_RIGHT:
            velocidade_x = tamanho_quadrado
            velocidade_y = 0

    elif tecla == pygame.K_LEFT:
            velocidade_x = -tamanho_quadrado
            velocidade_y = 0
    
    return velocidade_x, velocidade_y

# criar um loop infinito
def rodar_jogo():
    fim_jogo = False

    # pos inicial 
    pos_x = largura / 2
    pos_y = altura / 2

    # quanto ela anda
    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1
    pixels = []

    comida_x, comida_y = gerar_comida()

    while not fim_jogo:
        tela.fill(preto)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_deslocamento(evento.key)

        # desenhar comida
        desenhar_comida(tamanho_quadrado, comida_x, comida_y)

        # atualizar pos cobra
        if pos_x < 0 or pos_x >= largura or pos_y < 0 or pos_y >= altura:
            fim_jogo = True
            
        pos_x += velocidade_x
        pos_y += velocidade_y

        # desenhar cobrinha
        pixels.append([pos_x, pos_y])           # pos atual da cabeça da cobra
        if len(pixels) > tamanho_cobra:
            del pixels[0]                       # acrescenta um pix e deleta o q saiu

        # cobra bateu nela mesma menos na cabeça
        for pixel in pixels[:-1]:                    
            if pixel == [pos_x, pos_y]:
                fim_jogo = True 

        desenhar_cobra(tamanho_quadrado, pixels)
        
        # desenhar pontos
        desenhar_pontuacao(tamanho_cobra-1)


        # atualização da tela
        pygame.display.update()

        # criar uma nova comida
        if pos_x == comida_x and pos_y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()


        relogio.tick(velocidade_jogo)
            

# desenhar os objs do jogo na tela
    # pontuação
    # cobrinha
    # comida

# criar lógica do end do jogo
    # cobra bateu na parede
    # cobra nela mesma

# pegar iterações do user
    # fechou o jogo
    # clicou na tela

rodar_jogo()