import pygame
import sys
from pytmx.util_pygame import load_pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN, K_w, K_a, K_s, K_d, K_e, K_LSHIFT
import math

pygame.init()


LARGURA = 800
ALTURA = 600
ZOOM = 3.5

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo com Mapa e Personagem")

tela_jogo = pygame.Surface((LARGURA // ZOOM, ALTURA // ZOOM))
clock = pygame.time.Clock()

#mapa
MapaOriginal = load_pygame("MapaOriginal.tmx")
TILE = 16

#colisoes
paredes = []

camada_colisao = MapaOriginal.get_layer_by_name("Colisao")

for obj in camada_colisao:
    paredes.append(
        pygame.Rect(
            obj.x,
            obj.y,
            obj.width,
            obj.height
        )
    )


# Idle
idle_down = pygame.image.load('Character_down_idle-Sheet6.png')
idle_right = pygame.image.load('Character_side_idle-Sheet6.png')
idle_left = pygame.image.load('Character_side-left_idle-Sheet6.png')
idle_up = pygame.image.load('Character_up_idle-Sheet6.png')

# Correr
run_down = pygame.image.load('Character_down_run-Sheet6.png')
run_right = pygame.image.load('Character_side_run-Sheet6.png')
run_left = pygame.image.load('Character_side-left_run-Sheet6.png')
run_up = pygame.image.load('Character_up_run-Sheet6.png')

#Soco
soco_down = pygame.image.load('Character_down_punch-Sheet4.png')
soco_up = pygame.image.load('Character_up_punch-Sheet4.png')
soco_left = pygame.image.load('Character_side-left_punch-Sheet4.png')
soco_right = pygame.image.load('Character_side_punch-Sheet4.png')

#Pegar
pegar_down = pygame.image.load('Character_down_Pick-up-Sheet3.png')
pegar_up = pygame.image.load('Character_up_Pick-up-Sheet3.png')
pegar_left = pygame.image.load('Character_side-left_Pick-up-Sheet3.png')
pegar_right = pygame.image.load('Character_side_Pick-up-Sheet3.png')

#Animaçoes
idle_down_list = []
idle_up_list = []
idle_left_list = []
idle_right_list = []

run_down_list = []
run_up_list = []
run_left_list = []
run_right_list = []

soco_down_list = []
soco_up_list = []
soco_left_list = []
soco_right_list = []

pegar_down_list = []
pegar_up_list = []
pegar_left_list = []
pegar_right_list = []

#Idle e correr
for i in range(6):
    idle_down_list.append(pygame.transform.scale(idle_down.subsurface((i * 13, 0, 13, 16)), (16, 16)))
    run_down_list.append(pygame.transform.scale(run_down.subsurface((i * 13, 0, 13, 17)), (16, 16)))

    idle_up_list.append(pygame.transform.scale(idle_up.subsurface((i * 11, 0, 11, 16)), (16, 16)))
    run_up_list.append(pygame.transform.scale(run_up.subsurface((i * 13, 0, 13, 17)), (16, 16)))

    idle_left_list.append(pygame.transform.scale(idle_left.subsurface((i * 12, 0, 12, 16)), (16, 16)))
    run_left_list.append(pygame.transform.scale(run_left.subsurface((i * 14, 0, 14, 17)), (16, 16)))

    idle_right_list.append(pygame.transform.scale(idle_right.subsurface((i * 12, 0, 12, 16)), (16, 16)))
    run_right_list.append(pygame.transform.scale(run_right.subsurface((i * 14, 0, 14, 17)), (16, 16)))

#Soco
for i in range(4):
    soco_down_list.append(pygame.transform.scale(soco_down.subsurface((i * 12, 0, 12, 18)), (16, 16)))
    soco_up_list.append(pygame.transform.scale(soco_up.subsurface((i * 12, 0, 12, 17)), (16, 16)))
    soco_left_list.append(pygame.transform.scale(soco_left.subsurface((i * 20, 0, 20, 18)), (20, 20)))
    soco_right_list.append(pygame.transform.scale(soco_right.subsurface((i * 20, 0, 20, 18)), (20, 20)))

#Pegar
for i in range(3):
    pegar_down_list.append(pygame.transform.scale(pegar_down.subsurface((i * 12, 0, 12, 16)), (16, 16)))
    pegar_up_list.append(pygame.transform.scale(pegar_up.subsurface((i * 11, 0, 11, 15)), (16, 16)))
    pegar_left_list.append(pygame.transform.scale(pegar_left.subsurface((i * 11, 0, 11, 16)), (16, 16)))
    pegar_right_list.append(pygame.transform.scale(pegar_right.subsurface((i * 11, 0, 11, 16)), (16, 16)))

jogador = pygame.Rect(80, 125, 16, 16)  

# Estado de animação
animacao_atual = idle_right_list
ultima_direcao = "right"
frame = 0
anim_time = 0


atacar = False
pegar = False


velocidade = 1
velocidade_shift = 1.6


while True:
    dt = clock.tick(60)


    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

        # Ataque com clique do mouse
        if evento.type == MOUSEBUTTONDOWN and evento.button == 1:
            if not atacar and not pegar:
                atacar = True
                anim_time = 0
                frame = 0

                if ultima_direcao == 'down':
                    animacao_atual = soco_down_list
                elif ultima_direcao == 'up':
                    animacao_atual = soco_up_list
                elif ultima_direcao == 'left':
                    animacao_atual = soco_left_list
                elif ultima_direcao == 'right':
                    animacao_atual = soco_right_list

        # Pegar com tecla E
        if evento.type == KEYDOWN and evento.key == K_e:
            if not pegar and not atacar:
                pegar = True
                anim_time = 0
                frame = 0

                if ultima_direcao == 'down':
                    animacao_atual = pegar_down_list
                elif ultima_direcao == 'up':
                    animacao_atual = pegar_up_list
                elif ultima_direcao == 'left':
                    animacao_atual = pegar_left_list
                elif ultima_direcao == 'right':
                    animacao_atual = pegar_right_list


    teclas = pygame.key.get_pressed()

    if not atacar and not pegar:
        vel = velocidade_shift if teclas[K_LSHIFT] else velocidade
        mover = False

        # Movimento 
        dx = 0
        dy = 0

        if teclas[K_a]:
            dx -= 1
            animacao_atual = run_left_list
            ultima_direcao = 'left'
        if teclas[K_d]:
            dx += 1
            animacao_atual = run_right_list
            ultima_direcao = 'right'
        if teclas[K_w]:
            dy -= 1
            animacao_atual = run_up_list
            ultima_direcao = 'up'
        if teclas[K_s]:
            dy += 1
            animacao_atual = run_down_list
            ultima_direcao = 'down'
        if dx != 0 or dy != 0:

            tamanho = math.sqrt(dx * dx + dy * dy)

            dx /= tamanho
            dy /= tamanho

            dx *= vel
            dy *= vel

            mover = True

        # Aplicar movimento horizontal com colisão
        jogador.x += dx

        for parede in paredes:
            if jogador.colliderect(parede):
                if dx > 0:
                    jogador.right = parede.left
                elif dx < 0:
                    jogador.left = parede.right
       
        # Aplicar movimento vertical com colisão
        jogador.y += dy

        for parede in paredes:
            if jogador.colliderect(parede):
                if dy > 0:
                    jogador.bottom = parede.top
                elif dy < 0:
                    jogador.top = parede.bottom

        # Idle quando não está se movendo
        if not mover:
            if ultima_direcao == "down":
                animacao_atual = idle_down_list
            elif ultima_direcao == "up":
                animacao_atual = idle_up_list
            elif ultima_direcao == "left":
                animacao_atual = idle_left_list
            elif ultima_direcao == "right":
                animacao_atual = idle_right_list

  
    anim_time += dt

    if anim_time >= 96:
        frame += 1
        anim_time = 0

        if frame >= len(animacao_atual):
            frame = 0
            if atacar:
                atacar = False
            if pegar:
                pegar = False

                # Retorna para idle após pegar
                if ultima_direcao == 'down':
                    animacao_atual = idle_down_list
                elif ultima_direcao == 'up':
                    animacao_atual = idle_up_list
                elif ultima_direcao == 'left':
                    animacao_atual = idle_left_list
                elif ultima_direcao == 'right':
                    animacao_atual = idle_right_list

   
    camera_x = jogador.centerx - (LARGURA // ZOOM) // 2
    camera_y = jogador.centery - (ALTURA // ZOOM) // 2

    
    tela_jogo.fill((0, 0, 0))

    # Desenhar mapa
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

    # Desenhar personagem animado
    sprite = animacao_atual[frame]

    offset_x = (sprite.get_width() - jogador.width) // 2
    offset_y = sprite.get_height() - jogador.height

    tela_jogo.blit(
        sprite,
        (
            jogador.x - camera_x - offset_x,
            jogador.y - camera_y - offset_y
        )
    )

    
    tela_zoom = pygame.transform.scale(
        tela_jogo,
        (LARGURA, ALTURA)
    )

    tela.blit(tela_zoom, (0, 0))
    pygame.display.flip()
