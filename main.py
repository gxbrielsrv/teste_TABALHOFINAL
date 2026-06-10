import pygame
import sys
from pytmx.util_pygame import load_pygame

pygame.init()

LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mapa Tiled")

clock = pygame.time.Clock()

mapa = load_pygame("mapa.tmx")

camera_x = 0
camera_y = 0
velocidade = 5

rodando = True

while rodando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_a]:
        camera_x += velocidade

    if teclas[pygame.K_d]:
        camera_x -= velocidade

    if teclas[pygame.K_w]:
        camera_y += velocidade

    if teclas[pygame.K_s]:
        camera_y -= velocidade

    tela.fill((0, 0, 0))

    for layer in mapa.visible_layers:
        if hasattr(layer, "data"):
            for x, y, gid in layer:
                tile = mapa.get_tile_image_by_gid(gid)

                if tile:
                    tela.blit(
                        tile,
                        (
                            x * mapa.tilewidth + camera_x,
                            y * mapa.tileheight + camera_y
                        )
                    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()