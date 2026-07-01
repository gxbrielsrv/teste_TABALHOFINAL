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


for i in range(4):

    soco_down_list.append(transform.scale(soco_down.subsurface((i * 12, 0, 12, 18)),(50, 70)))
    soco_up_list.append(transform.scale(soco_up.subsurface((i * 12, 0, 12, 17)),(50, 70)))
    soco_left_list.append(transform.scale(soco_left.subsurface((i * 20, 0, 20, 18)),(80, 70)))
    soco_right_list.append(transform.scale(soco_right.subsurface((i * 20, 0, 20, 18)),(80, 70)))

    taco_down_ataque_list.append(transform.scale(taco_down_ataque.subsurface((i *20,0,20,25)),(50,70)))
    taco_up_ataque_list.append(transform.scale(taco_up_ataque.subsurface((i * 20,0,20,25)),(50,70)))
    taco_right_ataque_list.append(transform.scale(taco_right_ataque.subsurface((i * 28,0,28,16)),(70,70)))
    taco_left_ataque_list.append(transform.scale(taco_left_ataque.subsurface((i * 28,0,28,16)),(70,70)))


for i in range(3):

    pegar_down_list.append(transform.scale(pegar_down.subsurface((i * 12, 0, 12, 16 )), (50, 70)))
    pegar_up_list.append(transform.scale(pegar_up.subsurface((i * 11, 0, 11, 15)), (50,70)))
    pegar_left_list.append(transform.scale(pegar_left.subsurface((i * 11, 0, 11, 16)), (50,70)))
    pegar_right_list.append(transform.scale(pegar_right.subsurface((i * 11, 0, 11, 16)), (50,70)))

for i in range(7):
    morte_left_list.append(transform.scale(morte_left.subsurface((i * 21,0,21,16)), (70,70)))
    morte_right_list.append(transform.scale(morte_right.subsurface((i * 21,0,21,16)), (70,70)))

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

    if distancia < zumbi_alcance_deteccao and distancia > zumbi_distancia_minima:
        zumbi_moveu = True

        dx /= distancia
        dy /= distancia

        zumbi_x += dx * zumbi_velocidade
        zumbi_y += dy * zumbi_velocidade

    
        if abs(dx) > abs(dy):
            zumbi_direcao = "right" if dx > 0 else "left"
        else:
            zumbi_direcao = "down" if dy > 0 else "up"

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

    zumbi_anim_time += dt
    if zumbi_anim_time >= 96:
        zumbi_anim_time = 0
        zumbi_frame += 1
        if zumbi_frame >= len(zumbi_animacao_atual):
            zumbi_frame = 0
        

    screen.fill((73, 77, 74))

    screen.blit(zumbi_animacao_atual[zumbi_frame], (zumbi_x, zumbi_y))

    draw_x = pos_x
    draw_y = pos_y

    if atacar:
        if ultima_direcao == "left":
            draw_x -= 30
        # elif ultima_direcao == "right":
        #     draw_x += 10 

    screen.blit(animacao_atual[frame], (draw_x, draw_y))

    if tem_taco and animacao_taco:
        screen.blit(animacao_taco[frame], (draw_x, draw_y))
    
    if taco_no_chao:
        screen.blit(imagem_taco, (taco_x, taco_y))

    display.update()