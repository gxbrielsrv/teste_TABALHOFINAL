import pygame
import sys
from pytmx.util_pygame import load_pygame
from pygame.locals import QUIT, K_w, K_a, K_s, K_d
import math

pygame.init()

LARGURA = 800
ALTURA = 600
ZOOM = 3.5
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mapa com Quadrado")
tela_jogo = pygame.Surface((LARGURA // ZOOM, ALTURA // ZOOM))
clock = pygame.time.Clock()

# carrega o mapa do tiled
MapaOriginal = load_pygame("MapaOriginal.tmx")
TILE = 16

# cria as colisões
paredes = []
camada_colisao = MapaOriginal.get_layer_by_name("Colisao")
for obj in camada_colisao:
    paredes.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

# "boneco"
jogador = pygame.Rect(80, 125, 16, 16)
velocidade = 2

while True:
    clock.tick(60)
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()
    teclas = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if teclas[K_a]:
        dx -= 1
    if teclas[K_d]:
        dx += 1
    if teclas[K_w]:
        dy -= 1
    if teclas[K_s]:
        dy += 1


    # movimento na horizontal com colisao
    jogador.x += dx
    for parede in paredes:
        if jogador.colliderect(parede):
            if dx > 0:
                jogador.right = parede.left
            elif dx < 0:
                jogador.left = parede.right

    # movimento na vertical com colisao
    jogador.y += dy
    for parede in paredes:
        if jogador.colliderect(parede):
            if dy > 0:
                jogador.bottom = parede.top
            elif dy < 0:
                jogador.top = parede.bottom

    # mover a camera
    camera_x = jogador.centerx - (LARGURA // ZOOM) // 2
    camera_y = jogador.centery - (ALTURA // ZOOM) // 2
    tela_jogo.fill((0, 0, 0))

    # desenha o mapa no pygame
    for layer in MapaOriginal.visible_layers:
        if hasattr(layer, "data"):
            for x, y, gid in layer:
                tile = MapaOriginal.get_tile_image_by_gid(gid)
                if tile:
                    tela_jogo.blit(tile,(x * TILE - camera_x,y * TILE - camera_y))

    #"boneco"
    pygame.draw.rect(tela_jogo,(255, 0, 0),(jogador.x - camera_x,jogador.y - camera_y,jogador.width,jogador.height))

    #zoom na tela
    tela_zoom = pygame.transform.scale(tela_jogo,(LARGURA, ALTURA))

    tela.blit(tela_zoom, (0, 0))
    pygame.display.flip()