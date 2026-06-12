import pygame
import sys
from pytmx.util_pygame import load_pygame

pygame.init()

LARGURA = 800
ALTURA = 600

ZOOM = 2

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("MapaOriginal")

tela_jogo = pygame.Surface((LARGURA // ZOOM, ALTURA // ZOOM))

clock = pygame.time.Clock()

MapaOriginal = load_pygame("MapaOriginal.tmx")

TILE = 16

paredes = []

camada_colisao = MapaOriginal.get_layer_by_name("Colisao")
print(MapaOriginal.tilewidth)
print(MapaOriginal.tileheight)
for x, y, gid in camada_colisao:
    if gid:
        parede = pygame.Rect(
            x * TILE,
            y * TILE,
            TILE,
            TILE
        )
        paredes.append(parede)

jogador = pygame.Rect(80, 125, 12, 12)

velocidade = 3

while True:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if teclas[pygame.K_a]:
        dx = -velocidade

    if teclas[pygame.K_d]:
        dx = velocidade

    if teclas[pygame.K_w]:
        dy = -velocidade

    if teclas[pygame.K_s]:
        dy = velocidade

    jogador.x += dx

    for parede in paredes:

        if jogador.colliderect(parede):

            if dx > 0:
                jogador.right = parede.left

            if dx < 0:
                jogador.left = parede.right

    jogador.y += dy

    for parede in paredes:

        if jogador.colliderect(parede):

            if dy > 0:
                jogador.bottom = parede.top

            if dy < 0:
                jogador.top = parede.bottom

    camera_x = jogador.centerx - (LARGURA // ZOOM) // 2
    camera_y = jogador.centery - (ALTURA // ZOOM) // 2

    tela_jogo.fill((0, 0, 0))

    for layer in MapaOriginal.visible_layers:

        if hasattr(layer, "data"):

            for x, y, gid in layer:

                tile = MapaOriginal.get_tile_image_by_gid(gid)

                if tile:

                    tela_jogo.blit(
                        tile,
                        (
                            x * TILE - camera_x,
                            y * TILE - camera_y
                        )
                    )

    pygame.draw.rect(
        tela_jogo,
        (255, 0, 0),
        (
            jogador.x - camera_x,
            jogador.y - camera_y,
            jogador.width,
            jogador.height
        )
    )

    tela_zoom = pygame.transform.scale(
        tela_jogo,
        (LARGURA, ALTURA)
    )

    tela.blit(tela_zoom, (0, 0))

    pygame.display.flip()
    clock.tick(60)

