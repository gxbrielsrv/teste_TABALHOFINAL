import pygame, sys
from pygame.locals import QUIT
from pygame import *

init()

clock = time.Clock()

screen = display.set_mode((1200,700))

idle_down = image.load('Character_down_idle-Sheet6.png').convert_alpha()
idle_right = image.load('Character_side_idle-Sheet6.png').convert_alpha()
idle_left = image.load('Character_side-left_idle-Sheet6.png').convert_alpha()
idle_up = image.load('Character_up_idle-Sheet6.png').convert_alpha()

run_down = image.load('Character_down_run-Sheet6.png').convert_alpha()
run_right = image.load('Character_side_run-Sheet6.png').convert_alpha()
run_left = image.load('Character_side-left_run-Sheet6.png').convert_alpha()
run_up = image.load('Character_up_run-Sheet6.png').convert_alpha()

soco_down = image.load('Character_down_punch-Sheet4.png').convert_alpha()
soco_up = image.load('Character_up_punch-Sheet4.png').convert_alpha()
soco_left = image.load('Character_side-left_punch-Sheet4.png').convert_alpha()
soco_right = image.load('Character_side_punch-Sheet4.png').convert_alpha()

pegar_down = image.load('Character_down_Pick-up-Sheet3.png').convert_alpha()
pegar_up = image.load('Character_up_Pick-up-Sheet3.png').convert_alpha()
pegar_left = image.load('Character_side-left_Pick-up-Sheet3.png').convert_alpha()
pegar_right = image.load('Character_side_Pick-up-Sheet3.png').convert_alpha()

morte_right = image.load('Character_side_death3-Sheet6.png').convert_alpha()
morte_left = image.load('Character_side-left_death3-Sheet7.png').convert_alpha()

imagem_taco = image.load('bat.png').convert_alpha()
imagem_taco = transform.scale(imagem_taco, (30, 30)).convert_alpha()

#imagem de ataque do taco
taco_down_ataque = image.load('Bat_down_attack-Sheet4.png').convert_alpha()
taco_up_ataque = image.load('Bat_up_attack-Sheet4.png').convert_alpha()
taco_right_ataque = image.load('Bat_side_attack-Sheet4.png').convert_alpha()
taco_left_ataque = image.load('Bat_side-left_attack-Sheet4.png').convert_alpha()

#imagem do boneco away/correndo com taco
taco_down_idle = image.load('Bat_down_idle-and-run-Sheet6.png').convert_alpha()
taco_up_idle = image.load('Bat_up_idle-and-run-Sheet6.png').convert_alpha()
taco_right_idle = image.load('Bat_side_idle-and-run-Sheet6.png').convert_alpha()
taco_left_idle = image.load('Bat_side-left_idle-and-run-Sheet6.png').convert_alpha()

#inimigos
zumbipeq_down_idle = image.load('Zombie_Small_Down_Idle-Sheet6.png').convert_alpha()
zumbipeq_up_idle = image.load('Zombie_Small_Up_Idle-Sheet6.png').convert_alpha()
zumbipeq_left_idle = image.load('Zombie_Small_Side-left_Idle-Sheet6.png').convert_alpha()
zumbipeq_right_idle = image.load('Zombie_Small_Side_Idle-Sheet6.png').convert_alpha()

zumbipeq_down_walk = image.load('Zombie_Small_Down_walk-Sheet6.png').convert_alpha()
zumbipeq_up_walk = image.load('Zombie_Small_Up_Walk-Sheet6.png').convert_alpha()
zumbipeq_left_walk = image.load('Zombie_Small_Side-left_Walk-Sheet6.png').convert_alpha()
zumbipeq_right_walk = image.load('Zombie_Small_Side_Walk-Sheet6.png').convert_alpha()

zumbipeq_attack_down = image.load('Zombie_Small_Down_First-Attack-Sheet4.png').convert_alpha()
zumbipeq_attack_up = image.load('Zombie_Small_Up_First-Attack-Sheet4.png').convert_alpha()
zumbipeq_attack_left = image.load('Zombie_Small_Side-left_First-Attack-Sheet4.png').convert_alpha()
zumbipeq_attack_right = image.load('Zombie_Small_Side_First-Attack-Sheet4.png').convert_alpha()

zumbipeq_death_right = image.load('Zombie_Small_Side_Second-Death-Sheet7.png').convert_alpha()
zumbipeq_death_left = image.load('Zombie_Small_Side-left_Second-Death-Sheet7.png').convert_alpha()

zumbigrande_down_idle = image.load('Zombie_Axe_Down_Idle-Sheet6.png').convert_alpha()
zumbigrande_up_idle = image.load('Zombie_Axe_Up_Idle-Sheet6.png').convert_alpha()
zumbigrande_left_idle = image.load('Zombie_Axe_Side-left_Idle-Sheet6.png').convert_alpha()
zumbigrande_right_idle = image.load('Zombie_Axe_Side_Idle-Sheet6.png').convert_alpha()

zumbigrande_down_walk = image.load('Zombie_Axe_Down_Walk-Sheet8.png').convert_alpha()
zumbigrande_up_walk = image.load('Zombie_Axe_Up_Walk-Sheet8.png').convert_alpha()
zumbigrande_left_walk = image.load('Zombie_Axe_Side-left_Walk-Sheet8.png').convert_alpha()
zumbigrande_right_walk = image.load('Zombie_Axe_Side_Walk-Sheet8.png').convert_alpha()

zumbigrande_attack_down = image.load('Zombie_Axe_Down_First-Attack-Sheet7.png').convert_alpha()
zumbigrande_attack_up = image.load('Zombie_Axe_Up_First-Attack-Sheet7.png').convert_alpha()
zumbigrande_attack_left = image.load('Zombie_Axe_Side-left_First-Attack-Sheet7.png').convert_alpha()
zumbigrande_attack_right = image.load('Zombie_Axe_Side_First-Attack-Sheet7.png').convert_alpha()

zumbigrande_death_right = image.load('Zombie_Axe_No-axe_Side_Second-Death-Sheet7.png').convert_alpha()
zumbigrande_death_left = image.load('Zombie_Axe_Side-left_Second-Death-Sheet7.png').convert_alpha()

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

morte_right_list = []
morte_left_list = []

#parte do taco

taco_down_ataque_list = []
taco_up_ataque_list = []
taco_right_ataque_list = []
taco_left_ataque_list = []

taco_down_idle_list = []
taco_up_idle_list = []
taco_right_idle_list = []
taco_left_idle_list = []

#parte zumbi

zumbipeq_down_idle_list = []
zumbipeq_up_idle_list = []
zumbipeq_left_idle_list = []
zumbipeq_right_idle_list = []

zumbipeq_down_walk_list = []
zumbipeq_up_walk_list = []
zumbipeq_left_walk_list = []
zumbipeq_right_walk_list = []

zumbipeq_attack_down_list = []
zumbipeq_attack_up_list = []
zumbipeq_attack_left_list = []
zumbipeq_attack_right_list = []

zumbipeq_death_right_list = []
zumbipeq_death_left_list = []

zumbigrande_down_idle_list = []
zumbigrande_up_idle_list = []
zumbigrande_left_idle_list = []
zumbigrande_right_idle_list = []

zumbigrande_down_walk_list = []
zumbigrande_up_walk_list = []
zumbigrande_left_walk_list = []
zumbigrande_right_walk_list = []

zumbigrande_attack_down_list = []
zumbigrande_attack_up_list = []
zumbigrande_attack_left_list = []
zumbigrande_attack_right_list = []

zumbigrande_death_right_list = []
zumbigrande_death_left_list = []

shot_vida = image.load('shot_1-Sheet3.png').convert_alpha()
shot_vida2 = image.load('shot_2-Sheet3.png').convert_alpha()

shotvida_list = []   # efeito de dano no JOGADOR
shotvida2_list = []  # efeito de dano no ZUMBI


for i in range(6):

    idle_down_list.append(transform.scale(idle_down.subsurface((i * 13, 0, 13, 16)), (50, 70)))
    run_down_list.append(transform.scale(run_down.subsurface((i * 13, 0, 13, 17)),(50, 70)))
    taco_down_idle_list.append(transform.scale(taco_down_idle.subsurface((i * 17,0,17,11)),(50,70)))

    idle_up_list.append(transform.scale(idle_up.subsurface((i * 11, 0, 11, 16)),(50, 70)))
    run_up_list.append(transform.scale(run_up.subsurface((i * 13, 0, 13, 17)),(50, 70)))
    taco_up_idle_list.append(transform.scale(taco_up_idle.subsurface((i * 16,0,16,11)),(50,70)))

    idle_left_list.append(transform.scale(idle_left.subsurface((i * 12, 0, 12, 16)),(50, 70)))
    run_left_list.append(transform.scale(run_left.subsurface((i * 14, 0, 14, 17)),(50, 70)))
    taco_left_idle_list.append(transform.scale(taco_left_idle.subsurface((i * 16,0,16,13)),(50,70)))

    idle_right_list.append(transform.scale(idle_right.subsurface((i * 12, 0, 12, 16)),(50, 70)))
    run_right_list.append(transform.scale(run_right.subsurface((i * 14, 0, 14, 17)),(50, 70)))
    taco_right_idle_list.append(transform.scale(taco_right_idle.subsurface((i * 16,0,16,13)),(50,70)))

    zumbipeq_down_idle_list.append(transform.scale(zumbipeq_down_idle.subsurface((i * 13, 0, 13, 16)), (50, 70)))
    zumbipeq_up_idle_list.append(transform.scale(zumbipeq_up_idle.subsurface((i * 13, 0, 13, 15)), (50, 70)))
    zumbipeq_left_idle_list.append(transform.scale(zumbipeq_left_idle.subsurface((i * 11, 0, 11, 15)), (50, 70)))
    zumbipeq_right_idle_list.append(transform.scale(zumbipeq_right_idle.subsurface((i * 11, 0, 11, 15)), (50, 70)))

    zumbipeq_down_walk_list.append(transform.scale(zumbipeq_down_walk.subsurface((i * 12, 0, 12, 16)), (50, 70)))
    zumbipeq_up_walk_list.append(transform.scale(zumbipeq_up_walk.subsurface((i * 13, 0, 13, 16)), (50, 70)))
    zumbipeq_left_walk_list.append(transform.scale(zumbipeq_left_walk.subsurface((i * 13, 0, 13, 15)), (50, 70)))
    zumbipeq_right_walk_list.append(transform.scale(zumbipeq_right_walk.subsurface((i * 13, 0, 13, 15)), (50, 70)))

    zumbigrande_down_idle_list.append(transform.scale(zumbigrande_down_idle.subsurface((i * 13, 0, 13, 18)), (70, 70)))
    zumbigrande_up_idle_list.append(transform.scale(zumbigrande_up_idle.subsurface((i * 12, 0, 12, 23)), (70, 70)))
    zumbigrande_left_idle_list.append(transform.scale(zumbigrande_left_idle.subsurface((i * 22, 0, 22, 18)), (70, 70)))
    zumbigrande_right_idle_list.append(transform.scale(zumbigrande_right_idle.subsurface((i * 22, 0, 22, 18)), (70, 70)))


for i in range(4):

    soco_down_list.append(transform.scale(soco_down.subsurface((i * 12, 0, 12, 18)),(50, 70)))
    soco_up_list.append(transform.scale(soco_up.subsurface((i * 12, 0, 12, 17)),(50, 70)))
    soco_left_list.append(transform.scale(soco_left.subsurface((i * 20, 0, 20, 18)),(80, 70)))
    soco_right_list.append(transform.scale(soco_right.subsurface((i * 20, 0, 20, 18)),(80, 70)))

    taco_down_ataque_list.append(transform.scale(taco_down_ataque.subsurface((i *20,0,20,25)),(50,70)))
    taco_up_ataque_list.append(transform.scale(taco_up_ataque.subsurface((i * 20,0,20,25)),(50,70)))
    taco_right_ataque_list.append(transform.scale(taco_right_ataque.subsurface((i * 28,0,28,16)),(70,70)))
    taco_left_ataque_list.append(transform.scale(taco_left_ataque.subsurface((i * 28,0,28,16)),(70,70)))

    zumbipeq_attack_down_list.append(transform.scale(zumbipeq_attack_down.subsurface((i * 13, 0, 13, 16)), (50, 70)))
    zumbipeq_attack_up_list.append(transform.scale(zumbipeq_attack_up.subsurface((i * 14, 0, 14, 15)), (50, 70)))
    zumbipeq_attack_left_list.append(transform.scale(zumbipeq_attack_left.subsurface((i * 11, 0, 11, 14)), (50, 70)))
    zumbipeq_attack_right_list.append(transform.scale(zumbipeq_attack_right.subsurface((i * 11, 0, 11, 14)), (50, 70)))


for i in range(3):

    pegar_down_list.append(transform.scale(pegar_down.subsurface((i * 12, 0, 12, 16 )), (50, 70)))
    pegar_up_list.append(transform.scale(pegar_up.subsurface((i * 11, 0, 11, 15)), (50,70)))
    pegar_left_list.append(transform.scale(pegar_left.subsurface((i * 11, 0, 11, 16)), (50,70)))
    pegar_right_list.append(transform.scale(pegar_right.subsurface((i * 11, 0, 11, 16)), (50,70)))
    shotvida_list.append(transform.scale(shot_vida.subsurface((i * 7, 0, 7, 6)), (30, 60)))
    shotvida2_list.append(transform.scale(shot_vida2.subsurface((i * 6, 0, 6, 6)), (30, 60)))

for i in range(7):
    morte_left_list.append(transform.scale(morte_left.subsurface((i * 21,0,21,16)), (70,70)))
    morte_right_list.append(transform.scale(morte_right.subsurface((i * 21,0,21,16)), (70,70)))
    zumbipeq_death_right_list.append(transform.scale(zumbipeq_death_right.subsurface((i * 16,0,16,16)), (50,70)))
    zumbipeq_death_left_list.append(transform.scale(zumbipeq_death_left.subsurface((i * 16,0,16,16)), (50,70)))

    zumbigrande_attack_down_list.append(transform.scale(zumbigrande_attack_down.subsurface((i * 15, 0, 15, 21)), (70, 70)))
    zumbigrande_attack_up_list.append(transform.scale(zumbigrande_attack_up.subsurface((i * 13, 0, 13, 25)), (70, 70)))
    zumbigrande_attack_left_list.append(transform.scale(zumbigrande_attack_left.subsurface((i * 25, 0, 25, 19)), (70, 70)))
    zumbigrande_attack_right_list.append(transform.scale(zumbigrande_attack_right.subsurface((i * 25, 0, 25, 19)), (70, 70)))

    zumbigrande_death_right_list.append(transform.scale(zumbigrande_death_right.subsurface((i * 22, 0, 22, 19)), (70, 70)))
    zumbigrande_death_left_list.append(transform.scale(zumbigrande_death_left.subsurface((i * 27, 0, 27, 20)), (70, 70)))

for i in range(8):
    zumbigrande_down_walk_list.append(transform.scale(zumbigrande_down_walk.subsurface((i * 12, 0, 12, 20)), (70, 70)))
    zumbigrande_up_walk_list.append(transform.scale(zumbigrande_up_walk.subsurface((i * 12, 0, 12, 23)), (70, 70)))
    zumbigrande_left_walk_list.append(transform.scale(zumbigrande_left_walk.subsurface((i * 21, 0, 21, 19)), (70, 70)))
    zumbigrande_right_walk_list.append(transform.scale(zumbigrande_right_walk.subsurface((i * 21, 0, 21, 19)), (70, 70)))

animacao_atual = idle_right_list
animacao_taco = None
ultima_direcao = "right"

frame_taco = 0
frame = 0
anim_time = 0 

atacar = False
pegar = False
morrer = False
morto = False

taco_no_chao = True
tem_taco = False

pos_x = 700
pos_y = 200
taco_x = 500
taco_y = 300

#zumbi

zumbi_x = 950
zumbi_y = 500
zumbi_direcao = "down"
zumbi_animacao_atual = zumbipeq_down_idle_list
zumbi_frame = 0
zumbi_anim_time = 0
zumbi_velocidade = 1.3
zumbi_alcance_deteccao = 250
zumbi_distancia_minima = 45

# --- vida do jogador ---
vida_maxima = 10
vida_atual = vida_maxima

dano_cooldown = 0
dano_cooldown_max = 1000 

#vida do zumbi pequeno

zumbi_vida_maxima = 3
zumbi_vida_atual = zumbi_vida_maxima
zumbi_vivo = True

zumbi_dano_cooldown = 0
zumbi_dano_cooldown_max = 500  

zumbi_flash_timer = 0
zumbi_flash_intervalo = 80
zumbi_mostrar_vermelho = False

golpe_aplicado = False  
alcance_ataque = 70

dano_zumbi_pequeno = 1   # dano que o zumbi pequeno tira do jogador

# zumbi grande

zumbigrande_x = 300
zumbigrande_y = 500
zumbigrande_direcao = "down"
zumbigrande_animacao_atual = zumbigrande_down_idle_list
zumbigrande_frame = 0
zumbigrande_anim_time = 0
zumbigrande_velocidade = 0.9
zumbigrande_alcance_deteccao = 280
zumbigrande_distancia_minima = 55

zumbigrande_vida_maxima = 5
zumbigrande_vida_atual = zumbigrande_vida_maxima
zumbigrande_vivo = True

zumbigrande_dano_cooldown = 0
zumbigrande_dano_cooldown_max = 700   # >= duracao da animacao de ataque (7 frames x 96ms)

zumbigrande_flash_timer = 0
zumbigrande_flash_intervalo = 80
zumbigrande_mostrar_vermelho = False

golpe_aplicado_grande = False

dano_zumbi_grande = 2   # dano que o zumbi grande tira do jogador

zumbigrande_atacando = False   # True enquanto toca a animacao de ataque

efeitos_dano = []
efeito_dano_intervalo = 96


def criar_efeito_dano(x, y, lista_frames):
    efeitos_dano.append({
        "x": x,
        "y": y,
        "frames": lista_frames,
        "frame_atual": 0,
        "anim_time": 0
    })


def obter_sprite_vermelha(sprite, alpha=140):
    vermelha = sprite.copy()
    overlay = Surface(sprite.get_size(), SRCALPHA)
    overlay.fill((255, 60, 60, 255))
    vermelha.blit(overlay, (0, 0), special_flags=BLEND_RGBA_MULT)
    vermelha.set_alpha(alpha)
    return vermelha

flash_timer = 0
flash_intervalo = 100
mostrar_vermelho = False


velocidade = 2
velocidade_shift = 4

while True:

    dt = clock.tick(60)

    for ev in event.get():
        if ev.type == QUIT:
            quit()
            sys.exit()

        if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
            if not atacar and not morto and not morrer:

                atacar = True
                anim_time = 0 
                frame = 0 
                golpe_aplicado = False
                golpe_aplicado_grande = False
            
                if ultima_direcao == 'down':
                    animacao_atual = soco_down_list
                    animacao_taco = taco_down_ataque_list if tem_taco else None
                
                elif ultima_direcao == 'up':
                    animacao_atual = soco_up_list
                    animacao_taco = taco_up_ataque_list if tem_taco else None

                elif ultima_direcao == 'left':
                    animacao_atual = soco_left_list
                    animacao_taco = taco_left_ataque_list if tem_taco else None

                elif ultima_direcao == 'right':
                    animacao_atual = soco_right_list    
                    animacao_taco = taco_right_ataque_list if tem_taco else None  
            
        if ev.type == KEYDOWN and ev.key == K_e:
            if not pegar and not morto and not morrer:

                if perto_do_taco and taco_no_chao:
                    pegar = True
                    taco_no_chao = False
                    tem_taco = True

                    anim_time = 0
                    frame = 0

                    if ultima_direcao == "down":
                        animacao_atual = pegar_down_list
                    elif ultima_direcao == "up":
                        animacao_atual = pegar_up_list
                    elif ultima_direcao == "left":
                        animacao_atual = pegar_left_list
                    elif ultima_direcao == "right":
                        animacao_atual = pegar_right_list

        if ev.type == KEYDOWN and ev.key == K_l:
            if not morrer and not morto:
                morrer = True
                frame = 0 
                anim_time = 0
                animacao_taco = None

                if ultima_direcao == 'right':
                    animacao_atual = morte_right_list
                elif ultima_direcao == 'left':
                    animacao_atual = morte_left_list
    

    keys = key.get_pressed()
    perto_do_taco = False
    if abs(pos_x - taco_x) < 40 and abs(pos_y - taco_y) < 40:
        perto_do_taco = True

    mover = False
    if not atacar and not pegar and not morrer and not morto:
        vel = velocidade_shift if keys[K_LSHIFT] else velocidade

        if keys[K_w]:
            animacao_atual = run_up_list
            if tem_taco:
                animacao_taco = taco_up_idle_list
            ultima_direcao = 'up'
            mover = True
            pos_y -= vel
        
        if keys[K_a]:
            animacao_atual = run_left_list
            if tem_taco:
                animacao_taco = taco_left_idle_list
            ultima_direcao = 'left'
            mover = True
            pos_x -= vel

        if keys[K_s]:
            animacao_atual = run_down_list
            if tem_taco:
                animacao_taco = taco_down_idle_list 
            ultima_direcao = 'down'
            mover = True
            pos_y += vel

        if keys[K_d]:
            animacao_atual = run_right_list
            if tem_taco:
                animacao_taco = taco_right_idle_list
            ultima_direcao = 'right'
            mover = True
            pos_x += vel

        if not mover:

            if ultima_direcao == "down":
                animacao_atual = idle_down_list
                if tem_taco:
                    animacao_taco = taco_down_idle_list

            elif ultima_direcao == "up":
                animacao_atual = idle_up_list
                if tem_taco:
                    animacao_taco = taco_up_idle_list

            elif ultima_direcao == "left":
                animacao_atual = idle_left_list
                if tem_taco:
                    animacao_taco = taco_left_idle_list

            elif ultima_direcao == "right":
                animacao_atual = idle_right_list
                if tem_taco:
                    animacao_taco = taco_right_idle_list

    anim_time += dt

    if anim_time >= 96:
        anim_time = 0
        
        if morrer:
            if frame < len(animacao_atual) - 1:
                frame += 1
            else:
                morrer = False
                morto = True
                frame = len(animacao_atual) - 1
        else:
            if not morto:
                frame += 1

            if frame >= len(animacao_atual):
                frame = 0

                if atacar:
                    atacar = False

                    if ultima_direcao == 'down':
                        animacao_atual = idle_down_list
                    elif ultima_direcao == 'up':
                        animacao_atual = idle_up_list
                    elif ultima_direcao == 'left':
                        animacao_atual = idle_left_list
                    elif ultima_direcao == 'right':
                        animacao_atual = idle_right_list

                if pegar:
                    pegar = False

                    if ultima_direcao == 'down':
                        animacao_atual = idle_down_list
                    elif ultima_direcao == 'up':
                        animacao_atual = idle_up_list
                    elif ultima_direcao == 'left':
                        animacao_atual = idle_left_list
                    elif ultima_direcao == 'right':
                        animacao_atual = idle_right_list
    

    dx = pos_x - zumbi_x
    dy = pos_y - zumbi_y
    distancia = (dx**2 + dy**2) ** 0.5

    zumbi_moveu = False
    zumbi_animacao_anterior = zumbi_animacao_atual

    if zumbi_vivo and distancia < zumbi_alcance_deteccao and distancia > zumbi_distancia_minima:
        zumbi_moveu = True

        dx_norm = dx / distancia
        dy_norm = dy / distancia

        zumbi_x += dx_norm * zumbi_velocidade
        zumbi_y += dy_norm * zumbi_velocidade

        nova_direcao = zumbi_direcao
        if abs(dx) > abs(dy) * 1.5:
            nova_direcao = "right" if dx > 0 else "left"
        elif abs(dy) > abs(dx) * 1.5:
            nova_direcao = "down" if dy > 0 else "up"

        if nova_direcao != zumbi_direcao:
            zumbi_direcao = nova_direcao
            zumbi_frame = 0
            zumbi_anim_time = 0

        if zumbi_direcao == "down":
            zumbi_animacao_atual = zumbipeq_down_walk_list
        elif zumbi_direcao == "up":
            zumbi_animacao_atual = zumbipeq_up_walk_list
        elif zumbi_direcao == "left":
            zumbi_animacao_atual = zumbipeq_left_walk_list
        elif zumbi_direcao == "right":
            zumbi_animacao_atual = zumbipeq_right_walk_list

    else:
        if zumbi_direcao == "down":
            zumbi_animacao_atual = zumbipeq_down_idle_list
        elif zumbi_direcao == "up":
            zumbi_animacao_atual = zumbipeq_up_idle_list
        elif zumbi_direcao == "left":
            zumbi_animacao_atual = zumbipeq_left_idle_list
        elif zumbi_direcao == "right":
            zumbi_animacao_atual = zumbipeq_right_idle_list

    # trava de seguranca: se a lista de animacao mudou (idle <-> walk) e o
    # frame atual nao existe na nova lista, evita o IndexError / crash
    if zumbi_animacao_atual is not zumbi_animacao_anterior and zumbi_frame >= len(zumbi_animacao_atual):
        zumbi_frame = 0
        zumbi_anim_time = 0

    zumbi_anim_time += dt
    if zumbi_anim_time >= 96:
        zumbi_anim_time = 0
        zumbi_frame += 1
        if zumbi_frame >= len(zumbi_animacao_atual):
            zumbi_frame = 0

    if zumbi_dano_cooldown > 0:
        zumbi_dano_cooldown -= dt

        zumbi_flash_timer += dt
        if zumbi_flash_timer >= zumbi_flash_intervalo:
            zumbi_flash_timer = 0
            zumbi_mostrar_vermelho = not zumbi_mostrar_vermelho
    else:
        zumbi_mostrar_vermelho = False
        zumbi_flash_timer = 0

    if (atacar and not golpe_aplicado and zumbi_vivo
            and distancia <= alcance_ataque and zumbi_dano_cooldown <= 0):
        golpe_aplicado = True
        zumbi_vida_atual -= 1
        zumbi_dano_cooldown = zumbi_dano_cooldown_max
        criar_efeito_dano(zumbi_x, zumbi_y - 20, shotvida2_list)

        if zumbi_vida_atual <= 0:
            zumbi_vivo = False

    if dano_cooldown > 0:
        dano_cooldown -= dt

        flash_timer += dt
        if flash_timer >= flash_intervalo:
            flash_timer = 0
            mostrar_vermelho = not mostrar_vermelho
    else:
        mostrar_vermelho = False
        flash_timer = 0

    if (zumbi_vivo and distancia <= zumbi_distancia_minima + 5
            and dano_cooldown <= 0 and vida_atual > 0 and not morto):
        vida_atual -= dano_zumbi_pequeno
        dano_cooldown = dano_cooldown_max
        criar_efeito_dano(pos_x, pos_y - 20, shotvida_list)

        if vida_atual <= 0 and not morrer and not morto:
            morrer = True
            frame = 0
            anim_time = 0
            animacao_taco = None

            if ultima_direcao == 'right':
                animacao_atual = morte_right_list
            elif ultima_direcao == 'left':
                animacao_atual = morte_left_list

    dx_g = pos_x - zumbigrande_x
    dy_g = pos_y - zumbigrande_y
    distancia_grande = (dx_g**2 + dy_g**2) ** 0.5

    zumbigrande_animacao_anterior = zumbigrande_animacao_atual

    if zumbigrande_atacando:
        # enquanto ataca, a animacao de ataque nao pode ser sobrescrita
        # pela logica de andar/parado
        pass

    elif zumbigrande_vivo and distancia_grande < zumbigrande_alcance_deteccao and distancia_grande > zumbigrande_distancia_minima:

        dx_norm_g = dx_g / distancia_grande
        dy_norm_g = dy_g / distancia_grande

        zumbigrande_x += dx_norm_g * zumbigrande_velocidade
        zumbigrande_y += dy_norm_g * zumbigrande_velocidade

        nova_direcao_g = zumbigrande_direcao
        if abs(dx_g) > abs(dy_g) * 1.5:
            nova_direcao_g = "right" if dx_g > 0 else "left"
        elif abs(dy_g) > abs(dx_g) * 1.5:
            nova_direcao_g = "down" if dy_g > 0 else "up"

        if nova_direcao_g != zumbigrande_direcao:
            zumbigrande_direcao = nova_direcao_g
            zumbigrande_frame = 0
            zumbigrande_anim_time = 0

        if zumbigrande_direcao == "down":
            zumbigrande_animacao_atual = zumbigrande_down_walk_list
        elif zumbigrande_direcao == "up":
            zumbigrande_animacao_atual = zumbigrande_up_walk_list
        elif zumbigrande_direcao == "left":
            zumbigrande_animacao_atual = zumbigrande_left_walk_list
        elif zumbigrande_direcao == "right":
            zumbigrande_animacao_atual = zumbigrande_right_walk_list

    else:
        if zumbigrande_direcao == "down":
            zumbigrande_animacao_atual = zumbigrande_down_idle_list
        elif zumbigrande_direcao == "up":
            zumbigrande_animacao_atual = zumbigrande_up_idle_list
        elif zumbigrande_direcao == "left":
            zumbigrande_animacao_atual = zumbigrande_left_idle_list
        elif zumbigrande_direcao == "right":
            zumbigrande_animacao_atual = zumbigrande_right_idle_list

    # trava de seguranca: mesma logica do zumbi pequeno, mas aqui era
    # OBRIGATORIA porque walk (8 frames) e idle (6 frames) tem tamanhos
    # diferentes no zumbi grande -- era isso que crashava o jogo
    if zumbigrande_animacao_atual is not zumbigrande_animacao_anterior and zumbigrande_frame >= len(zumbigrande_animacao_atual):
        zumbigrande_frame = 0
        zumbigrande_anim_time = 0

    zumbigrande_anim_time += dt
    if zumbigrande_anim_time >= 96:
        zumbigrande_anim_time = 0
        zumbigrande_frame += 1
        if zumbigrande_frame >= len(zumbigrande_animacao_atual):
            zumbigrande_frame = 0
            if zumbigrande_atacando:
                zumbigrande_atacando = False   # animacao de ataque terminou, volta ao normal

    if zumbigrande_dano_cooldown > 0:
        zumbigrande_dano_cooldown -= dt
        zumbigrande_flash_timer += dt
        if zumbigrande_flash_timer >= zumbigrande_flash_intervalo:
            zumbigrande_flash_timer = 0
            zumbigrande_mostrar_vermelho = not zumbigrande_mostrar_vermelho
    else:
        zumbigrande_mostrar_vermelho = False
        zumbigrande_flash_timer = 0

    if (atacar and not golpe_aplicado_grande and zumbigrande_vivo
            and distancia_grande <= alcance_ataque and zumbigrande_dano_cooldown <= 0):
        golpe_aplicado_grande = True
        zumbigrande_vida_atual -= 1
        zumbigrande_dano_cooldown = zumbigrande_dano_cooldown_max
        criar_efeito_dano(zumbigrande_x, zumbigrande_y - 20, shotvida2_list)

        if zumbigrande_vida_atual <= 0:
            zumbigrande_vivo = False

    if (zumbigrande_vivo and distancia_grande <= zumbigrande_distancia_minima + 5
            and dano_cooldown <= 0 and vida_atual > 0 and not morto):
        vida_atual -= dano_zumbi_grande
        dano_cooldown = dano_cooldown_max
        criar_efeito_dano(pos_x, pos_y - 20, shotvida_list)

        # dispara a animacao de ataque do zumbi grande
        zumbigrande_atacando = True
        zumbigrande_frame = 0
        zumbigrande_anim_time = 0

        if zumbigrande_direcao == "down":
            zumbigrande_animacao_atual = zumbigrande_attack_down_list
        elif zumbigrande_direcao == "up":
            zumbigrande_animacao_atual = zumbigrande_attack_up_list
        elif zumbigrande_direcao == "left":
            zumbigrande_animacao_atual = zumbigrande_attack_left_list
        elif zumbigrande_direcao == "right":
            zumbigrande_animacao_atual = zumbigrande_attack_right_list

        if vida_atual <= 0 and not morrer and not morto:
            morrer = True
            frame = 0
            anim_time = 0
            animacao_taco = None

            if ultima_direcao == 'right':
                animacao_atual = morte_right_list
            elif ultima_direcao == 'left':
                animacao_atual = morte_left_list

    for efeito in efeitos_dano[:]:
        efeito["anim_time"] += dt
        if efeito["anim_time"] >= efeito_dano_intervalo:
            efeito["anim_time"] = 0
            efeito["frame_atual"] += 1

            if efeito["frame_atual"] >= len(efeito["frames"]):
                efeitos_dano.remove(efeito)

    screen.fill((73, 77, 74))

    if zumbi_vivo:
        if zumbi_mostrar_vermelho:
            screen.blit(obter_sprite_vermelha(zumbi_animacao_atual[zumbi_frame]), (zumbi_x, zumbi_y))
        else:
            screen.blit(zumbi_animacao_atual[zumbi_frame], (zumbi_x, zumbi_y))
    if zumbigrande_vivo:
        if zumbigrande_mostrar_vermelho:
            screen.blit(obter_sprite_vermelha(zumbigrande_animacao_atual[zumbigrande_frame]), (zumbigrande_x, zumbigrande_y))
        else:
            screen.blit(zumbigrande_animacao_atual[zumbigrande_frame], (zumbigrande_x, zumbigrande_y))

    draw_x = pos_x
    draw_y = pos_y

    if atacar:
        if ultima_direcao == "left":
            draw_x -= 30
        # elif ultima_direcao == "right":
        #    draw_x += 10 

    if mostrar_vermelho:
        screen.blit(obter_sprite_vermelha(animacao_atual[frame]), (draw_x, draw_y))
    else:
        screen.blit(animacao_atual[frame], (draw_x, draw_y))

    if tem_taco and animacao_taco:
        screen.blit(animacao_taco[frame], (draw_x, draw_y))
    
    if taco_no_chao:
        screen.blit(imagem_taco, (taco_x, taco_y))

    for efeito in efeitos_dano:
        screen.blit(efeito["frames"][efeito["frame_atual"]], (efeito["x"], efeito["y"]))

    display.update()
