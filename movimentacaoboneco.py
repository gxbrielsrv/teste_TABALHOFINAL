import pygame, sys
from pygame.locals import QUIT
from pygame import *

init()

clock = time.Clock()

screen = display.set_mode((1200,700))

idle_down = image.load('Character_down_idle-Sheet6.png')
idle_right = image.load('Character_side_idle-Sheet6.png')
idle_left = image.load('Character_side-left_idle-Sheet6.png')
idle_up = image.load('Character_up_idle-Sheet6.png')

run_down = image.load('Character_down_run-Sheet6.png')
run_right = image.load('Character_side_run-Sheet6.png')
run_left = image.load('Character_side-left_run-Sheet6.png')
run_up = image.load('Character_up_run-Sheet6.png')

soco_down = image.load('Character_down_punch-Sheet4.png')
soco_up = image.load('Character_up_punch-Sheet4.png')
soco_left = image.load('Character_side-left_punch-Sheet4.png')
soco_right = image.load('Character_side_punch-Sheet4.png')

pegar_down = image.load('Character_down_Pick-up-Sheet3.png')
pegar_up = image.load('Character_up_Pick-up-Sheet3.png')
pegar_left = image.load('Character_side-left_Pick-up-Sheet3.png')
pegar_right = image.load('Character_side_Pick-up-Sheet3.png')

morte_right = image.load('Character_side_death3-Sheet6.png')
morte_left = image.load('Character_side-left_death3-Sheet7.png')

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

for i in range(6):

    idle_down_list.append(transform.scale(idle_down.subsurface((i * 13, 0, 13, 16)), (50, 70)))
    run_down_list.append(transform.scale(run_down.subsurface((i * 13, 0, 13, 17)),(50, 70)))

    idle_up_list.append(transform.scale(idle_up.subsurface((i * 11, 0, 11, 16)),(50, 70)))
    run_up_list.append(transform.scale(run_up.subsurface((i * 13, 0, 13, 17)),(50, 70)))

    idle_left_list.append(transform.scale(idle_left.subsurface((i * 12, 0, 12, 16)),(50, 70)))
    run_left_list.append(transform.scale(run_left.subsurface((i * 14, 0, 14, 17)),(50, 70)))

    idle_right_list.append(transform.scale(idle_right.subsurface((i * 12, 0, 12, 16)),(50, 70)))
    run_right_list.append(transform.scale(run_right.subsurface((i * 14, 0, 14, 17)),(50, 70)))

    morte_right_list.append(transform.scale(morte_right.subsurface((i * 24,0,24,16)), (50,70)))

for i in range(4):

    soco_down_list.append(transform.scale(soco_down.subsurface((i * 12, 0, 12, 18)),(50, 70)))
    soco_up_list.append(transform.scale(soco_up.subsurface((i * 12, 0, 12, 17)),(50, 70)))
    soco_left_list.append(transform.scale(soco_left.subsurface((i * 20, 0, 20, 18)),(80, 70)))
    soco_right_list.append(transform.scale(soco_right.subsurface((i * 20, 0, 20, 18)),(80, 70)))

for i in range(3):

    pegar_down_list.append(transform.scale(pegar_down.subsurface((i * 12, 0, 12, 16 )), (50, 70)))
    pegar_up_list.append(transform.scale(pegar_up.subsurface((i * 11, 0, 11, 15)), (50,70)))
    pegar_left_list.append(transform.scale(pegar_left.subsurface((i * 11, 0, 11, 16)), (50,70)))
    pegar_right_list.append(transform.scale(pegar_right.subsurface((i * 11, 0, 11, 16)), (50,70)))

for i in range(7):
    morte_left_list.append(transform.scale(morte_left.subsurface((i * 24,0,24,16)), (50,70)))
    
animacao_atual = idle_right_list
ultima_direcao = "right"

frame = 0
anim_time = 0 

atacar = False
pegar = False

pos_x = 700
pos_y = 200

velocidade = 2
velocidade_shift = 4

while True:

    dt = clock.tick(60)

    for ev in event.get():
        if ev.type == QUIT:
            quit()
            sys.exit()

        if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
            if not atacar:

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
            
        if ev.type == KEYDOWN and ev.key == K_e:
            if not pegar:
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
    

    keys = key.get_pressed()

    mover = False
    if not atacar and not pegar:
        vel = velocidade_shift if keys[K_LSHIFT] else velocidade

        if keys[K_w]:
            animacao_atual = run_up_list
            ultima_direcao = 'up'
            mover = True
            pos_y -= vel
        
        if keys[K_a]:
            animacao_atual = run_left_list
            ultima_direcao = 'left'
            mover = True
            pos_x -= vel

        if keys[K_s]:
            animacao_atual = run_down_list
            ultima_direcao = 'down'
            mover = True
            pos_y += vel

        if keys[K_d]:
            animacao_atual = run_right_list
            ultima_direcao = 'right'
            mover = True
            pos_x += vel

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

                if ultima_direcao == 'down':
                    animacao_atual = idle_down_list

                elif ultima_direcao == 'up':
                    animacao_atual = idle_up_list

                elif ultima_direcao == 'left':
                    animacao_atual = idle_left_list

                elif ultima_direcao == 'right':
                    animacao_atual = idle_right_list

            frame = 0

    screen.fill((73, 77, 74))

    draw_x = pos_x
    draw_y = pos_y

    if atacar:
        if ultima_direcao == "left":
            draw_x -= 30
        # elif ultima_direcao == "right":
        #     draw_x += 10 

    screen.blit(animacao_atual[frame], (draw_x, draw_y))


    display.update()