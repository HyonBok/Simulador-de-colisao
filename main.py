import random
import pygame
import math
from pygame.locals import *
from sys import exit

# Variáveis iniciais e inicialização da tela.
pygame.init()
largura = 1000
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Simulador')
# Lista que será usada mais adiante.
particulas = []
quantidadeDeParticulas = 100
# Define a fonte de todos os textos.
font = pygame.font.Font('freesansbold.ttf', 24)
energiaCinetica = 0


# Define as propriedades e colisão das partículas.
class Particula:
    def __init__(self, v, pos, raio, cor):
        self.v = v
        self.raio = raio
        self.pos = pos
        self.cor = cor
        # Massa = raio²
        self.massa = math.pow(raio, 2)

    # Colisão definida entre 2 partículas.
    def colisao(self, colisor):
        # Massa total.
        mt = self.massa + colisor.massa

        # Velocidade das partículas.
        v1 = pygame.Vector2(self.v.x, self.v.y)
        v2 = pygame.Vector2(colisor.v.x, colisor.v.y)

        # Parte principal, usa a função de projeção ortogonal para conseguir as componentes de velocidade da direção p.
        v1px, v1py = projecao(v1.x, v1.y, self.pos.x - colisor.pos.x, self.pos.y - colisor.pos.y)
        v2px, v2py = projecao(v2.x, v2.y, self.pos.x - colisor.pos.x, self.pos.y - colisor.pos.y)

        # Aqui, as projeções sao adicionados conforme a própria velocidade da partícula e sua massa.
        self.v.x += (v2px - v1px) * 2 * colisor.massa / mt
        self.v.y += (v2py - v1py) * 2 * colisor.massa / mt
        colisor.v.x += (v1px - v2px) * 2 * self.massa / mt
        colisor.v.y += (v1py - v2py) * 2 * self.massa / mt


# Função de projeção.
def projecao(vx, vy, ux, uy):
    # vetor u = vetor de direção p
    # proj(b)a = <a,b> / |b²| * b
    # proj(b)a = ʎ * bx, ʎ * by
    p = ((vx * ux) + (vy * uy)) / ((ux * ux) + (uy * uy))
    return p * ux, p * uy


# Apenas mostra energia cinética do sistema.
def textos(ec):
    ec = font.render("Ec: " + str(round(ec, 2)), True, (255, 255, 255))
    tela.blit(ec, (10, 10))


# Testa se há colisão naquele espaço.
def colidindo(pos1, pos2, raio1, raio2):
    distancia = math.hypot(pos1.x - pos2.x, pos1.y - pos2.y)
    if distancia < raio1 + raio2:
        return True
    return False


# A função CriarParticula pode criar indefinidamente até o momento que a tela estiver 'cheia'.
def criar_particula():
    cor = random.uniform(80, 220)
    raio = random.uniform(20, 60)
    pos = pygame.Vector2(0, 0)
    # Apenas compara se não há outras partículas no mesmo espaço.
    # t é apenas uma variável de confirmação, caso não haja mais espaço.
    flag = False
    t = 0
    while not flag:
        flag = True
        pos = pygame.Vector2(random.uniform(raio, largura - raio), random.uniform(raio, altura - raio))
        for p in range(0, len(particulas)):
            if colidindo(pos, particulas[p].pos, raio, particulas[p].raio):
                flag = False
                break
        t += 1
        if t > 10:
            return None
    v = pygame.Vector2(random.uniform(-0.4, 0.4), random.uniform(-0.4, 0.4))
    part = Particula(v, pos, raio, (cor, cor, cor))
    return part


# Criação das partículas.
for x in range(0, quantidadeDeParticulas):
    particula = criar_particula()
    if particula:
        particulas.append(particula)


# Execução do programa.
while True:
    # Preenche a tela de preto.
    tela.fill((10, 10, 10))

    # Atualiza a partir de eventos.
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # Atualiza energia cinética para recontar.
    energiaCinetica = 0
    # Tamanho da lista de partículas.
    k = len(particulas)
    for i in range(0, k):
        # Movimentação pela velocidade.
        particulas[i].pos += particulas[i].v
        # Confere se as partículas estão colidindo com as paredes invertendo suas velocidades.
        # Além disso, verifica se a velocidade condiz com a colisão, para não trava-las na parede.
        if ((particulas[i].pos.x > largura - particulas[i].raio and particulas[i].v.x > 0) or
                (particulas[i].pos.x < particulas[i].raio and particulas[i].v.x < 0)):
            particulas[i].v.x *= -1
        if ((particulas[i].pos.y > altura - particulas[i].raio and particulas[i].v.y > 0) or
                (particulas[i].pos.y < particulas[i].raio and particulas[i].v.y < 0)):
            particulas[i].v.y *= -1
        # Percorre a lista O(n²/2), pois a verificação so precisa ser feita pelo par de partículas.
        j = i + 1
        for j in range(j, k):
            if colidindo(particulas[i].pos, particulas[j].pos, particulas[i].raio, particulas[j].raio):
                particulas[i].colisao(particulas[j])
        # Desenha os objetos e incrementa a energia cinética.
        pygame.draw.circle(tela, particulas[i].cor, (particulas[i].pos.x, particulas[i].pos.y), particulas[i].raio)
        energiaCinetica += particulas[i].massa * (particulas[i].v.x * particulas[i].v.x +
                                                  particulas[i].v.y * particulas[i].v.y)

    textos(energiaCinetica)
    # Deixa a tela atualizando
    pygame.display.update()
