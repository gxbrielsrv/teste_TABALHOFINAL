import pygame
import sys
import os
from pytmx.util_pygame import load_pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN, K_w, K_a, K_s, K_d, K_e, K_l, K_LSHIFT, K_ESCAPE
import math

pygame.init()

LARGURA = 800
ALTURA = 600
ZOOM = 3.5

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Into the Epidemic")

tela_jogo = pygame.Surface((LARGURA // ZOOM, ALTURA // ZOOM))
clock = pygame.time.Clock()

# Mapa
NOME_MAPA = "MapaOriginal.tmx"
MapaOriginal = load_pygame(NOME_MAPA)
TILE = 16

ARQUIVO_SAVE = "save.txt"

# Final do jogo
imagem_final = pygame.image.load("final_casa.png")
imagem_final = pygame.transform.scale(imagem_final, (LARGURA, ALTURA))
area_final = pygame.Rect(1095, 190, 24, 24)

# Efeitos sonoros
som_porta = pygame.mixer.Sound("porta.wav")
som_porta2 = pygame.mixer.Sound("som_porta2.wav")
som_porta2.set_volume(0.1)
som_taco = pygame.mixer.Sound('somtaco.wav')
som_taco.set_volume(0.2)
som_vida = pygame.mixer.Sound('somvida.wav')
som_vida.set_volume(0.2)
som_soco = pygame.mixer.Sound('somsoco.wav')
som_soco.set_volume(0.2)


# Sistema de portas
area_teleporte = pygame.Rect(48, 210, 18, 18) 
destino_x = 48  
destino_y = 190

area_teleporte2 = pygame.Rect(200, 115, 12, 12) 
destino_x2 = 215 
destino_y2= 115

area_teleporte3 = pygame.Rect(265, 195, 12, 12) 
destino_x3 = 280  
destino_y3= 195

area_teleporte4 = pygame.Rect(564, 240, 8, 8) 
destino_x4 = 562  
destino_y4= 265

area_teleporte5 = pygame.Rect(564, 255, 8, 8) 
destino_x5 = 562
destino_y5= 225

area_teleporte6 = pygame.Rect(530, 270, 8, 8) 
destino_x6 = 495
destino_y6= 275

area_teleporte7 = pygame.Rect(510, 270, 8, 8) 
destino_x7 = 530
destino_y7= 270

# Funçoes
def tela_game_over():
    botao_sair = pygame.Rect(0, 0, 360, 65)
    botao_sair.center = (LARGURA // 2, ALTURA // 2 + 50)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == QUIT:
                salvar_jogo()
                pygame.quit()
                sys.exit()

            if evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                if botao_sair.collidepoint(evento.pos):
                    return "sair"

        tela.fill((10, 10, 15))

        texto_fim = fonte_titulo_maior.render("FIM DE JOGO", True, COR_TITULO_VERMELHO)
        sombra_fim = fonte_titulo_maior.render("FIM DE JOGO", True, COR_SOMBRA)
        rect_fim = texto_fim.get_rect(center=(LARGURA // 2, ALTURA // 2 - 100))

        tela.blit(sombra_fim, (rect_fim.x + 5, rect_fim.y + 5))
        tela.blit(texto_fim, rect_fim)

        desenhar_botao_menu(tela, botao_sair, "SAIR", mouse_pos)

        pygame.display.flip()
        clock.tick(60)

def mostrar_final():
    botao_sair = pygame.Rect(0, 0, 360, 65)
    botao_sair.center = (LARGURA // 2, ALTURA - 100) 

    tela.fill((0, 0, 0))
    pygame.display.flip()
    
    pygame.time.wait(500) 

    canal = som_porta.play()

    while canal.get_busy():

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        tela.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(60)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                if botao_sair.collidepoint(evento.pos):
                    return "menu" 

        tela.blit(imagem_final, (0, 0))
        
        desenhar_botao_menu(tela, botao_sair, "MENU INICIAL", mouse_pos)
        
        pygame.display.flip()
        clock.tick(60)

def desenhar_hud_jogador(superficie, vida):
    for i in range(8):

        cor = (200, 0, 0) if i < vida else (50, 50, 50)
        pygame.draw.rect(superficie, cor, (10 + (i * 25), 10, 20, 20))
        pygame.draw.rect(superficie, (255, 255, 255), (10 + (i * 25), 10, 20, 20), 2)

def desenhar_hud_zumbi(superficie, zumbi, camera_x, camera_y):
    for i in range(5):
        cor = (0, 200, 0) if i < zumbi["vida"] else (50, 50, 50)

        x = zumbi["rect"].x - camera_x + (i * 4)
        y = zumbi["rect"].y - camera_y - 8
        pygame.draw.rect(superficie, cor, (x, y, 3, 3))



def salvar_jogo():
    try:
        with open(ARQUIVO_SAVE, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"mapa={NOME_MAPA}\n")
            arquivo.write(f"pos_x={jogador.x}\n")
            arquivo.write(f"pos_y={jogador.y}\n")
            arquivo.write(f"direcao={ultima_direcao}\n")
            arquivo.write(f"tem_taco={tem_taco}\n")
            arquivo.write(f"taco_no_chao={taco_no_chao}\n")
            arquivo.write(f"taco_x={taco_rect.x}\n")
            arquivo.write(f"taco_y={taco_rect.y}\n")
            arquivo.write(f"morto={morto}\n")
            arquivo.write(f"vida_jogador={vida_jogador}\n")
            arquivo.write(f"zumbis_mortos={zumbis_mortos}\n")
            for i, zumbi in enumerate(lista_zumbis):
                arquivo.write(f"zumbi_{i}_vivo={zumbi['vivo']}\n")
                arquivo.write(f"zumbi_{i}_morto={zumbi['morto']}\n")
    except Exception as erro:
        print(f"[SAVE] Nao foi possivel salvar o jogo: {erro}")

def carregar_jogo():
    dados_save = {}
    if os.path.exists(ARQUIVO_SAVE):
        try:
            with open(ARQUIVO_SAVE, "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    linha = linha.strip()
                    if not linha or "=" not in linha:
                        continue
                    chave, valor = linha.split("=", 1)
                    dados_save[chave] = valor
        except Exception as erro:
            print(f"[SAVE] Nao foi possivel ler o save: {erro}")
    return dados_save

# Colisoes
paredes = []
camada_colisao = MapaOriginal.get_layer_by_name("Colisao")
for obj in camada_colisao:
    paredes.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

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

# Soco
soco_down = pygame.image.load('Character_down_punch-Sheet4.png')
soco_up = pygame.image.load('Character_up_punch-Sheet4.png')
soco_left = pygame.image.load('Character_side-left_punch-Sheet4.png')
soco_right = pygame.image.load('Character_side_punch-Sheet4.png')

# Pegar
pegar_down = pygame.image.load('Character_down_Pick-up-Sheet3.png')
pegar_up = pygame.image.load('Character_up_Pick-up-Sheet3.png')
pegar_left = pygame.image.load('Character_side-left_Pick-up-Sheet3.png')
pegar_right = pygame.image.load('Character_side_Pick-up-Sheet3.png')

# Morrer
morte_right = pygame.image.load('Character_side_death3-Sheet6.png')
morte_left = pygame.image.load('Character_side-left_death3-Sheet7.png')

# Taco
imagem_taco = pygame.image.load('bat.png')
imagem_taco = pygame.transform.scale(imagem_taco, (16, 16))

taco_down_ataque = pygame.image.load('Bat_down_attack-Sheet4.png')
taco_up_ataque = pygame.image.load('Bat_up_attack-Sheet4.png')
taco_right_ataque = pygame.image.load('Bat_side_attack-Sheet4.png')
taco_left_ataque = pygame.image.load('Bat_side-left_attack-Sheet4.png')

taco_down_idle = pygame.image.load('Bat_down_idle-and-run-Sheet6.png')
taco_up_idle = pygame.image.load('Bat_up_idle-and-run-Sheet6.png')
taco_right_idle = pygame.image.load('Bat_side_idle-and-run-Sheet6.png')
taco_left_idle = pygame.image.load('Bat_side-left_idle-and-run-Sheet6.png')

# Animaçoes Jogador
idle_down_list = []; idle_up_list = []; idle_left_list = []; idle_right_list = []
run_down_list = []; run_up_list = []; run_left_list = []; run_right_list = []
soco_down_list = []; soco_up_list = []; soco_left_list = []; soco_right_list = []
pegar_down_list = []; pegar_up_list = []; pegar_left_list = []; pegar_right_list = []
morte_right_list = []; morte_left_list = []
taco_down_ataque_list = []; taco_up_ataque_list = []; taco_left_ataque_list = []; taco_right_ataque_list = []
taco_down_idle_list = []; taco_up_idle_list = []; taco_left_idle_list = []; taco_right_idle_list = []

# Idle e correr
for i in range(6):
    idle_down_list.append(pygame.transform.scale(idle_down.subsurface((i * 13, 0, 13, 16)), (16, 16)))
    run_down_list.append(pygame.transform.scale(run_down.subsurface((i * 13, 0, 13, 17)), (16, 16)))
    idle_up_list.append(pygame.transform.scale(idle_up.subsurface((i * 11, 0, 11, 16)), (16, 16)))
    run_up_list.append(pygame.transform.scale(run_up.subsurface((i * 13, 0, 13, 17)), (16, 16)))
    idle_left_list.append(pygame.transform.scale(idle_left.subsurface((i * 12, 0, 12, 16)), (16, 16)))
    run_left_list.append(pygame.transform.scale(run_left.subsurface((i * 14, 0, 14, 17)), (16, 16)))
    idle_right_list.append(pygame.transform.scale(idle_right.subsurface((i * 12, 0, 12, 16)), (16, 16)))
    run_right_list.append(pygame.transform.scale(run_right.subsurface((i * 14, 0, 14, 17)), (16, 16)))
    taco_down_idle_list.append(pygame.transform.scale(taco_down_idle.subsurface((i * 17, 0, 17, 11)), (16, 16)))
    taco_up_idle_list.append(pygame.transform.scale(taco_up_idle.subsurface((i * 16, 0, 16, 11)), (16, 16)))
    taco_left_idle_list.append(pygame.transform.scale(taco_left_idle.subsurface((i * 16, 0, 16, 13)), (16, 16)))
    taco_right_idle_list.append(pygame.transform.scale(taco_right_idle.subsurface((i * 16, 0, 16, 13)), (16, 16)))

# Soco
for i in range(4):
    soco_down_list.append(pygame.transform.scale(soco_down.subsurface((i * 12, 0, 12, 18)), (16, 16)))
    soco_up_list.append(pygame.transform.scale(soco_up.subsurface((i * 12, 0, 12, 17)), (16, 16)))
    soco_left_list.append(pygame.transform.scale(soco_left.subsurface((i * 20, 0, 20, 18)), (20, 20)))
    soco_right_list.append(pygame.transform.scale(soco_right.subsurface((i * 20, 0, 20, 18)), (20, 20)))
    taco_down_ataque_list.append(pygame.transform.scale(taco_down_ataque.subsurface((i * 20, 0, 20, 25)), (16, 16)))
    taco_up_ataque_list.append(pygame.transform.scale(taco_up_ataque.subsurface((i * 20, 0, 20, 25)), (16, 16)))
    taco_left_ataque_list.append(pygame.transform.scale(taco_left_ataque.subsurface((i * 28, 0, 28, 16)), (20, 20)))
    taco_right_ataque_list.append(pygame.transform.scale(taco_right_ataque.subsurface((i * 28, 0, 28, 16)), (20, 20)))

# Pegar
for i in range(3):
    pegar_down_list.append(pygame.transform.scale(pegar_down.subsurface((i * 12, 0, 12, 16)), (16, 16)))
    pegar_up_list.append(pygame.transform.scale(pegar_up.subsurface((i * 11, 0, 11, 15)), (16, 16)))
    pegar_left_list.append(pygame.transform.scale(pegar_left.subsurface((i * 11, 0, 11, 16)), (16, 16)))
    pegar_right_list.append(pygame.transform.scale(pegar_right.subsurface((i * 11, 0, 11, 16)), (16, 16)))

# Morte
for i in range(7):
    morte_left_list.append(pygame.transform.scale(morte_left.subsurface((i * 21, 0, 21, 16)), (20, 20)))
    morte_right_list.append(pygame.transform.scale(morte_right.subsurface((i * 21, 0, 21, 16)), (20, 20)))

try:
    zumbipeq_down_idle = pygame.image.load('Zombie_Small_Down_Idle-Sheet6.png')
    zumbipeq_up_idle = pygame.image.load('Zombie_Small_Up_Idle-Sheet6.png')
    zumbipeq_left_idle = pygame.image.load('Zombie_Small_Side-left_Idle-Sheet6.png')
    zumbipeq_right_idle = pygame.image.load('Zombie_Small_Side_Idle-Sheet6.png')

    zumbipeq_down_walk = pygame.image.load('Zombie_Small_Down_walk-Sheet6.png')
    zumbipeq_up_walk = pygame.image.load('Zombie_Small_Up_Walk-Sheet6.png')
    zumbipeq_left_walk = pygame.image.load('Zombie_Small_Side-left_Walk-Sheet6.png')
    zumbipeq_right_walk = pygame.image.load('Zombie_Small_Side_Walk-Sheet6.png')

    zumbipeq_attack_down = pygame.image.load('Zombie_Small_Down_First-Attack-Sheet4.png')
    zumbipeq_attack_up = pygame.image.load('Zombie_Small_Up_First-Attack-Sheet4.png')
    zumbipeq_attack_left = pygame.image.load('Zombie_Small_Side-left_First-Attack-Sheet4.png')
    zumbipeq_attack_right = pygame.image.load('Zombie_Small_Side_First-Attack-Sheet4.png')

    zumbipeq_death_right = pygame.image.load('Zombie_Small_Side_Second-Death-Sheet7.png')
    zumbipeq_death_left = pygame.image.load('Zombie_Small_Side-left_Second-Death-Sheet7.png')

    zumbipeq_down_idle_list = []; zumbipeq_up_idle_list = []; zumbipeq_left_idle_list = []; zumbipeq_right_idle_list = []
    zumbipeq_down_walk_list = []; zumbipeq_up_walk_list = []; zumbipeq_left_walk_list = []; zumbipeq_right_walk_list = []
    zumbipeq_attack_down_list = []; zumbipeq_attack_up_list = []; zumbipeq_attack_left_list = []; zumbipeq_attack_right_list = []
    zumbipeq_death_right_list = []; zumbipeq_death_left_list = []

    for i in range(6):
        zumbipeq_down_idle_list.append(pygame.transform.scale(zumbipeq_down_idle.subsurface((i * 13, 0, 13, 16)), (16, 16)))
        zumbipeq_up_idle_list.append(pygame.transform.scale(zumbipeq_up_idle.subsurface((i * 13, 0, 13, 15)), (16, 16)))
        zumbipeq_left_idle_list.append(pygame.transform.scale(zumbipeq_left_idle.subsurface((i * 11, 0, 11, 15)), (16, 16)))
        zumbipeq_right_idle_list.append(pygame.transform.scale(zumbipeq_right_idle.subsurface((i * 11, 0, 11, 15)), (16, 16)))

        zumbipeq_down_walk_list.append(pygame.transform.scale(zumbipeq_down_walk.subsurface((i * 12, 0, 12, 16)), (16, 16)))
        zumbipeq_up_walk_list.append(pygame.transform.scale(zumbipeq_up_walk.subsurface((i * 13, 0, 13, 16)), (16, 16)))
        zumbipeq_left_walk_list.append(pygame.transform.scale(zumbipeq_left_walk.subsurface((i * 13, 0, 13, 15)), (16, 16)))
        zumbipeq_right_walk_list.append(pygame.transform.scale(zumbipeq_right_walk.subsurface((i * 13, 0, 13, 15)), (16, 16)))

    for i in range(4):
        zumbipeq_attack_down_list.append(pygame.transform.scale(zumbipeq_attack_down.subsurface((i * 13, 0, 13, 16)), (16, 16)))
        zumbipeq_attack_up_list.append(pygame.transform.scale(zumbipeq_attack_up.subsurface((i * 14, 0, 14, 15)), (16, 16)))
        zumbipeq_attack_left_list.append(pygame.transform.scale(zumbipeq_attack_left.subsurface((i * 11, 0, 11, 14)), (16, 16)))
        zumbipeq_attack_right_list.append(pygame.transform.scale(zumbipeq_attack_right.subsurface((i * 11, 0, 11, 14)), (16, 16)))

    for i in range(7):
        zumbipeq_death_right_list.append(pygame.transform.scale(zumbipeq_death_right.subsurface((i * 16, 0, 16, 16)), (16, 16)))
        zumbipeq_death_left_list.append(pygame.transform.scale(zumbipeq_death_left.subsurface((i * 16, 0, 16, 16)), (16, 16)))

except Exception as e:
    print(f"Aviso: Nao foi possivel carregar alguma imagem de zumbi ({e}). Usando superficies coloridas.")
    zumbipeq_down_idle_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbipeq_up_idle_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbipeq_left_idle_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbipeq_right_idle_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbipeq_down_walk_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbipeq_up_walk_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbipeq_left_walk_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbipeq_right_walk_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbipeq_attack_down_list = [pygame.Surface((16,16)) for _ in range(4)]
    zumbipeq_attack_up_list = [pygame.Surface((16,16)) for _ in range(4)]
    zumbipeq_attack_left_list = [pygame.Surface((16,16)) for _ in range(4)]
    zumbipeq_attack_right_list = [pygame.Surface((16,16)) for _ in range(4)]
    zumbipeq_death_right_list = [pygame.Surface((16,16)) for _ in range(7)]
    zumbipeq_death_left_list = [pygame.Surface((16,16)) for _ in range(7)]

    for lista in [zumbipeq_down_idle_list, zumbipeq_up_idle_list, zumbipeq_left_idle_list, zumbipeq_right_idle_list,
                  zumbipeq_down_walk_list, zumbipeq_up_walk_list, zumbipeq_left_walk_list, zumbipeq_right_walk_list]:
        for s in lista: s.fill((20, 150, 20))

    for lista in [zumbipeq_attack_down_list, zumbipeq_attack_up_list, zumbipeq_attack_left_list, zumbipeq_attack_right_list]:
        for s in lista: s.fill((200, 120, 20))

    for lista in [zumbipeq_death_right_list, zumbipeq_death_left_list]:
        for s in lista: s.fill((80, 20, 20))

try:
    zumbiaxe_down_idle = pygame.image.load('Zombie_Axe_Down_Idle-Sheet6.png')
    zumbiaxe_up_idle = pygame.image.load('Zombie_Axe_Up_Idle-Sheet6.png')
    zumbiaxe_left_idle = pygame.image.load('Zombie_Axe_Side-left_Idle-Sheet6.png')
    zumbiaxe_right_idle = pygame.image.load('Zombie_Axe_Side_Idle-Sheet6.png')

    zumbiaxe_down_walk = pygame.image.load('Zombie_Axe_Down_walk-Sheet8.png')
    zumbiaxe_up_walk = pygame.image.load('Zombie_Axe_Up_Walk-Sheet8.png')
    zumbiaxe_left_walk = pygame.image.load('Zombie_Axe_Side-left_Walk-Sheet8.png')
    zumbiaxe_right_walk = pygame.image.load('Zombie_Axe_Side_Walk-Sheet8.png')

    zumbiaxe_attack_down = pygame.image.load('Zombie_Axe_Down_First-Attack-Sheet7.png')
    zumbiaxe_attack_up = pygame.image.load('Zombie_Axe_Up_First-Attack-Sheet7.png')
    zumbiaxe_attack_left = pygame.image.load('Zombie_Axe_Side-left_First-Attack-Sheet7.png')
    zumbiaxe_attack_right = pygame.image.load('Zombie_Axe_Side_First-Attack-Sheet7.png')

    zumbiaxe_death_right = pygame.image.load('Zombie_Axe_No-axe_Side_Second-Death-Sheet7.png')
    zumbiaxe_death_left = pygame.image.load('Zombie_Axe_Side-left_Second-Death-Sheet7.png')

    zumbiaxe_down_idle_list = []; zumbiaxe_up_idle_list = []; zumbiaxe_left_idle_list = []; zumbiaxe_right_idle_list = []
    zumbiaxe_down_walk_list = []; zumbiaxe_up_walk_list = []; zumbiaxe_left_walk_list = []; zumbiaxe_right_walk_list = []
    zumbiaxe_attack_down_list = []; zumbiaxe_attack_up_list = []; zumbiaxe_attack_left_list = []; zumbiaxe_attack_right_list = []
    zumbiaxe_death_right_list = []; zumbiaxe_death_left_list = []

    for i in range(6):
        zumbiaxe_down_idle_list.append(pygame.transform.scale(zumbiaxe_down_idle.subsurface((i * 13, 0 , 13, 18)), (16, 16)))
        zumbiaxe_up_idle_list.append(pygame.transform.scale(zumbiaxe_up_idle.subsurface((i * 12, 0, 12, 23)), (16, 16)))
        zumbiaxe_left_idle_list.append(pygame.transform.scale(zumbiaxe_left_idle.subsurface((i * 22, 0, 22, 18)), (16, 16)))
        zumbiaxe_right_idle_list.append(pygame.transform.scale(zumbiaxe_right_idle.subsurface((i * 22, 0, 22, 18)), (16, 16)))

    for i in range(8):
        zumbiaxe_down_walk_list.append(pygame.transform.scale(zumbiaxe_down_walk.subsurface((i * 12, 0, 12, 20)), (16, 16)))
        zumbiaxe_up_walk_list.append(pygame.transform.scale(zumbiaxe_up_walk.subsurface((i * 12, 0, 12, 23)), (16, 16)))
        zumbiaxe_left_walk_list.append(pygame.transform.scale(zumbiaxe_left_walk.subsurface((i * 21, 0, 21, 19)), (16, 16)))
        zumbiaxe_right_walk_list.append(pygame.transform.scale(zumbiaxe_right_walk.subsurface((i * 21, 0, 21, 19)), (16, 16)))

    for i in range(7):
        zumbiaxe_attack_down_list.append(pygame.transform.scale(zumbiaxe_attack_down.subsurface((i * 15, 0, 15, 21)), (16, 16)))
        zumbiaxe_attack_up_list.append(pygame.transform.scale(zumbiaxe_attack_up.subsurface((i * 13, 0, 13, 25)), (16, 16)))
        zumbiaxe_attack_left_list.append(pygame.transform.scale(zumbiaxe_attack_left.subsurface((i * 25, 0, 25, 19)), (16, 16)))
        zumbiaxe_attack_right_list.append(pygame.transform.scale(zumbiaxe_attack_right.subsurface((i * 25, 0, 25, 19)), (16, 16)))

    for i in range(7):
        zumbiaxe_death_right_list.append(pygame.transform.scale(zumbiaxe_death_right.subsurface((i * 22, 0, 22, 19)), (16, 16)))
        zumbiaxe_death_left_list.append(pygame.transform.scale(zumbiaxe_death_left.subsurface((i * 27, 0, 27, 20)), (16, 16)))

except Exception as e:
    print(f"Aviso: Nao foi possivel carregar alguma imagem de zumbi machado ({e}). Usando superficies coloridas.")
    zumbiaxe_down_idle_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbiaxe_up_idle_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbiaxe_left_idle_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbiaxe_right_idle_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbiaxe_down_walk_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbiaxe_up_walk_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbiaxe_left_walk_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbiaxe_right_walk_list = [pygame.Surface((16,16)) for _ in range(6)]
    zumbiaxe_attack_down_list = [pygame.Surface((16,16)) for _ in range(4)]
    zumbiaxe_attack_up_list = [pygame.Surface((16,16)) for _ in range(4)]
    zumbiaxe_attack_left_list = [pygame.Surface((16,16)) for _ in range(4)]
    zumbiaxe_attack_right_list = [pygame.Surface((16,16)) for _ in range(4)]
    zumbiaxe_death_right_list = [pygame.Surface((16,16)) for _ in range(7)]
    zumbiaxe_death_left_list = [pygame.Surface((16,16)) for _ in range(7)]

    for lista in [zumbiaxe_down_idle_list, zumbiaxe_up_idle_list, zumbiaxe_left_idle_list, zumbiaxe_right_idle_list,
                  zumbiaxe_down_walk_list, zumbiaxe_up_walk_list, zumbiaxe_left_walk_list, zumbiaxe_right_walk_list]:
        for s in lista: s.fill((20, 150, 20))

    for lista in [zumbiaxe_attack_down_list, zumbiaxe_attack_up_list, zumbiaxe_attack_left_list, zumbiaxe_attack_right_list]:
        for s in lista: s.fill((200, 120, 20))

    for lista in [zumbiaxe_death_right_list, zumbiaxe_death_left_list]:
        for s in lista: s.fill((80, 20, 20))

ANIMACOES_ZUMBI = {
    "peq": {
        "idle": {"down": zumbipeq_down_idle_list, "up": zumbipeq_up_idle_list,
                 "left": zumbipeq_left_idle_list, "right": zumbipeq_right_idle_list},
        "walk": {"down": zumbipeq_down_walk_list, "up": zumbipeq_up_walk_list,
                 "left": zumbipeq_left_walk_list, "right": zumbipeq_right_walk_list},
        "attack": {"down": zumbipeq_attack_down_list, "up": zumbipeq_attack_up_list,
                   "left": zumbipeq_attack_left_list, "right": zumbipeq_attack_right_list},
        "death": {"left": zumbipeq_death_left_list, "right": zumbipeq_death_right_list},
    },
    "axe": {
        "idle": {"down": zumbiaxe_down_idle_list, "up": zumbiaxe_up_idle_list,
                 "left": zumbiaxe_left_idle_list, "right": zumbiaxe_right_idle_list},
        "walk": {"down": zumbiaxe_down_walk_list, "up": zumbiaxe_up_walk_list,
                 "left": zumbiaxe_left_walk_list, "right": zumbiaxe_right_walk_list},
        "attack": {"down": zumbiaxe_attack_down_list, "up": zumbiaxe_attack_up_list,
                   "left": zumbiaxe_attack_left_list, "right": zumbiaxe_attack_right_list},
        "death": {"left": zumbiaxe_death_left_list, "right": zumbiaxe_death_right_list},
    },
}

def obter_sprite_vermelha(sprite, alpha=140):
    vermelha = sprite.copy()
    overlay = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
    overlay.fill((255, 60, 60, 255))
    vermelha.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    vermelha.set_alpha(alpha)
    return vermelha

# Fontes 
pygame.font.init()
try:
    fonte_titulo_menor = pygame.font.SysFont("courier", 45, bold=True)
    fonte_titulo_maior = pygame.font.SysFont("courier", 85, bold=True)
    fonte_botao_menu = pygame.font.SysFont("courier", 24, bold=True)
except:
    fonte_titulo_menor = pygame.font.Font(None, 45)
    fonte_titulo_maior = pygame.font.Font(None, 85)
    fonte_botao_menu = pygame.font.Font(None, 24)

# Paleta de Cores baseada na imagem
COR_TITULO_BRANCO = (200, 200, 190)
COR_TITULO_VERDE = (140, 180, 100)
COR_TITULO_VERMELHO = (190, 40, 40)
COR_BOTAO_BG = (50, 75, 100)
COR_BOTAO_HOVER = (65, 95, 120)
COR_BOTAO_BORDA = (20, 20, 25)
COR_BOTAO_DETALHE = (180, 80, 80) 
COR_CAVEIRA = (200, 60, 150)
COR_BOTAO_DESABILITADO = (40, 50, 60)
COR_SOMBRA = (10, 10, 15)

def desenhar_caveira_pixelada(superficie, x, y, cor):
    pygame.draw.rect(superficie, cor, (x - 8, y - 8, 16, 12))
    pygame.draw.rect(superficie, cor, (x - 5, y + 4, 10, 5))
    pygame.draw.rect(superficie, COR_SOMBRA, (x - 6, y - 3, 4, 4))
    pygame.draw.rect(superficie, COR_SOMBRA, (x + 2, y - 3, 4, 4))
    pygame.draw.rect(superficie, COR_SOMBRA, (x - 1, y + 1, 2, 3))
    pygame.draw.line(superficie, COR_SOMBRA, (x - 2, y + 5), (x - 2, y + 8), 1)
    pygame.draw.line(superficie, COR_SOMBRA, (x + 1, y + 5), (x + 1, y + 8), 1)

def desenhar_botao_menu(superficie, rect, texto, mouse_pos, habilitado=True):
    hover = rect.collidepoint(mouse_pos) if habilitado else False
    bg_color = COR_BOTAO_HOVER if hover else COR_BOTAO_BG
    if not habilitado:
        bg_color = COR_BOTAO_DESABILITADO
    cor_texto = (255, 255, 255) if habilitado else (120, 120, 120)
    sombra_rect = rect.copy()
    sombra_rect.y += 4
    pygame.draw.rect(superficie, COR_SOMBRA, sombra_rect)

    pygame.draw.rect(superficie, bg_color, rect)
    
    pygame.draw.rect(superficie, COR_BOTAO_BORDA, rect, width=4)
    pygame.draw.rect(superficie, (100, 130, 160) if habilitado else (70, 80, 90), rect.inflate(-8, -8), width=2)

    largura_bracadeira, altura_bracadeira = 16, 40
    rect_esq = pygame.Rect(rect.left - 8, rect.centery - altura_bracadeira // 2, largura_bracadeira, altura_bracadeira)
    pygame.draw.rect(superficie, COR_BOTAO_DETALHE if habilitado else (100, 60, 60), rect_esq)
    pygame.draw.rect(superficie, COR_BOTAO_BORDA, rect_esq, width=3)
    rect_dir = pygame.Rect(rect.right - 8, rect.centery - altura_bracadeira // 2, largura_bracadeira, altura_bracadeira)
    pygame.draw.rect(superficie, COR_BOTAO_DETALHE if habilitado else (100, 60, 60), rect_dir)
    pygame.draw.rect(superficie, COR_BOTAO_BORDA, rect_dir, width=3)

    desenhar_caveira_pixelada(superficie, rect.left + 35, rect.centery,'#FFFFFF')
    desenhar_caveira_pixelada(superficie, rect.right - 35, rect.centery,'#FFFFFF')

    texto_sombra = fonte_botao_menu.render(texto, True, COR_SOMBRA)
    texto_render = fonte_botao_menu.render(texto, True, cor_texto)
    texto_rect = texto_render.get_rect(center=rect.center)
    
    superficie.blit(texto_sombra, (texto_rect.x + 2, texto_rect.y + 2))
    superficie.blit(texto_render, texto_rect)

def renderizar_fundo_sombrio(superficie):
    for layer in MapaOriginal.visible_layers:
        if hasattr(layer, "data"):
            for x, y, gid in layer:
                tile = MapaOriginal.get_tile_image_by_gid(gid)
                if tile:
                    tile_zoom = pygame.transform.scale(tile, (int(16 * ZOOM), int(16 * ZOOM)))
                    superficie.blit(tile_zoom, (x * int(16 * ZOOM), y * int(16 * ZOOM)))
    
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((10, 20, 25, 210))
    superficie.blit(overlay, (0, 0))

def desenhar_titulo_jogo(superficie):
    centro_x = LARGURA // 2
    texto_into = fonte_titulo_menor.render("INTO THE", True, COR_TITULO_BRANCO)
    sombra_into = fonte_titulo_menor.render("INTO THE", True, COR_SOMBRA)
    rect_into = texto_into.get_rect(center=(centro_x, 120))
    superficie.blit(sombra_into, (rect_into.x + 4, rect_into.y + 4))
    superficie.blit(texto_into, rect_into)

    texto_epi = fonte_titulo_maior.render("EPI", True, COR_TITULO_VERDE)
    sombra_epi = fonte_titulo_maior.render("EPI", True, COR_SOMBRA)
    texto_d = fonte_titulo_maior.render("D", True, COR_TITULO_VERMELHO)
    sombra_d = fonte_titulo_maior.render("D", True, COR_SOMBRA)
    texto_emic = fonte_titulo_maior.render("EMIC", True, COR_TITULO_VERDE)
    sombra_emic = fonte_titulo_maior.render("EMIC", True, COR_SOMBRA)

    largura_total = texto_epi.get_width() + texto_d.get_width() + texto_emic.get_width()
    inicio_x = centro_x - (largura_total // 2)
    y_epidemic = 170

    superficie.blit(sombra_epi, (inicio_x + 5, y_epidemic + 5))
    superficie.blit(texto_epi, (inicio_x, y_epidemic))
    inicio_x += texto_epi.get_width()
    
    superficie.blit(sombra_d, (inicio_x + 5, y_epidemic + 5))
    superficie.blit(texto_d, (inicio_x, y_epidemic))
    inicio_x += texto_d.get_width()

    superficie.blit(sombra_emic, (inicio_x + 5, y_epidemic + 5))
    superficie.blit(texto_emic, (inicio_x, y_epidemic))


def tela_menu_principal():
    existe_save = os.path.exists(ARQUIVO_SAVE)

    botao_novo_jogo = pygame.Rect(0, 0, 360, 65)
    botao_continuar = pygame.Rect(0, 0, 360, 65)

    botao_novo_jogo.center = (LARGURA // 2, ALTURA // 2 + 50)
    botao_continuar.center = (LARGURA // 2, ALTURA // 2 + 135)

    fonte_mensagem_menu = pygame.font.SysFont("courier", 20, bold=True)
    mensagem_aviso = ""
    mensagem_aviso_ate = 0

    while True:
        mouse_pos = pygame.mouse.get_pos()
        agora = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                if botao_novo_jogo.collidepoint(evento.pos):
                    return "novo"
                if botao_continuar.collidepoint(evento.pos):
                    if existe_save:
                        return "continuar"
                    else:
                        mensagem_aviso = "NENHUM SAVE ENCONTRADO!"
                        mensagem_aviso_ate = agora + 2000

        renderizar_fundo_sombrio(tela)
        desenhar_titulo_jogo(tela)
        desenhar_botao_menu(tela, botao_novo_jogo, "NOVO JOGO", mouse_pos)
        desenhar_botao_menu(tela, botao_continuar, "CONTINUAR JOGO", mouse_pos, habilitado=existe_save)

        if mensagem_aviso and agora < mensagem_aviso_ate:
            texto_aviso = fonte_mensagem_menu.render(mensagem_aviso, True, (255, 100, 100))
            texto_aviso_rect = texto_aviso.get_rect(center=(LARGURA // 2, botao_continuar.bottom + 30))
            tela.blit(texto_aviso, texto_aviso_rect)

        pygame.display.flip()
        clock.tick(60)

def tela_pausa():
    fundo_pausa = tela.copy()
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((10, 20, 25, 200))

    botao_continuar_pausa = pygame.Rect(0, 0, 360, 65)
    botao_sair_pausa = pygame.Rect(0, 0, 360, 65)
    botao_continuar_pausa.center = (LARGURA // 2, ALTURA // 2 - 20)
    botao_sair_pausa.center = (LARGURA // 2, ALTURA // 2 + 70)

    titulo_pausa = fonte_titulo_maior.render("PAUSADO", True, COR_TITULO_BRANCO)
    sombra_pausa = fonte_titulo_maior.render("PAUSADO", True, COR_SOMBRA)
    titulo_pausa_rect = titulo_pausa.get_rect(center=(LARGURA // 2, ALTURA // 2 - 140))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == QUIT:
                salvar_jogo()
                pygame.quit()
                sys.exit()

            if evento.type == KEYDOWN and evento.key == K_ESCAPE:
                return "continuar"

            if evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                if botao_continuar_pausa.collidepoint(evento.pos):
                    return "continuar"
                if botao_sair_pausa.collidepoint(evento.pos):
                    return "sair"

        tela.blit(fundo_pausa, (0, 0))
        tela.blit(overlay, (0, 0))
        
        tela.blit(sombra_pausa, (titulo_pausa_rect.x + 5, titulo_pausa_rect.y + 5))
        tela.blit(titulo_pausa, titulo_pausa_rect)

        desenhar_botao_menu(tela, botao_continuar_pausa, "CONTINUAR", mouse_pos)
        desenhar_botao_menu(tela, botao_sair_pausa, "SAIR E SALVAR", mouse_pos)

        pygame.display.flip()
        clock.tick(60)

while True:
    opcao_menu = tela_menu_principal()

    velocidade = 1
    velocidade_shift = 1.6
    mensagem_cama_ativa = True

    if opcao_menu == "continuar" :
        mensagem_cama_ativa = False

    try:
        fonte_mensagem_cama = pygame.font.SysFont("courier", 28, bold=True)
    except:
        fonte_mensagem_cama = pygame.font.Font(None, 28)
  
    jogador = pygame.Rect(95, 280, 14, 14)
    taco_rect = pygame.Rect(450, 270, 16, 16)
    taco_no_chao = True
    tem_taco = False
    perto_do_taco = False

    # Status do Jogador
    vida_jogador = 8
    zumbis_mortos = 0
    dano_cooldown_jogador = 0
    dano_cooldown_max = 1000
    mostrar_vermelho_jogador = False
    flash_timer_jogador = 0
    alcance_ataque_jogador = 25

    # Estado de animação
    animacao_atual = idle_right_list
    ultima_direcao = "right"
    frame = 0
    anim_time = 0

    atacar = False
    pegar = False
    morto = False
    morrer = False

    def criar_zumbi(x, y, velocidade, alcance_deteccao, tipo="peq", dano=1, vida=5):
        return {
            "rect": pygame.Rect(x, y, 16, 16),
            "tipo": tipo,
            "velocidade": velocidade,
            "dano": dano,
            "alcance_deteccao": alcance_deteccao,
            "direcao": "down",
            "movendo": False,
            "frame": 0,
            "anim_time": 0,
            "vivo": True,
            "vida": vida,
            "dano_cooldown": 0,
            "flash_timer": 0,
            "mostrar_vermelho": False,
            "atacando": False,
            "ataque_frame": 0,
            "ataque_anim_time": 0,
            "ataque_cooldown": 0,
            "dano_aplicado": False,
            "morrendo": False,
            "morto": False,
        }

    # Adicionar zumbis 
    lista_zumbis = [criar_zumbi(x=430, y=50, velocidade=0.6, alcance_deteccao=55),
        criar_zumbi(x=720, y=60, velocidade=0.6, alcance_deteccao=70),
        criar_zumbi(x=1060, y=220, velocidade=1, alcance_deteccao=130),
        criar_zumbi(x=860, y=220, velocidade=1.2, alcance_deteccao=100, tipo="axe", dano=2, vida=5)]

    if opcao_menu == "novo":
        salvar_jogo()
    elif opcao_menu == "continuar":
        dados_save = carregar_jogo()
        if dados_save:
            try:
                jogador.x = int(dados_save.get("pos_x", jogador.x))
                jogador.y = int(dados_save.get("pos_y", jogador.y))
                ultima_direcao = dados_save.get("direcao", ultima_direcao)
                tem_taco = dados_save.get("tem_taco", str(tem_taco)) == "True"
                taco_no_chao = dados_save.get("taco_no_chao", str(taco_no_chao)) == "True"
                taco_rect.x = int(dados_save.get("taco_x", taco_rect.x))
                taco_rect.y = int(dados_save.get("taco_y", taco_rect.y))
                morto = dados_save.get("morto", str(morto)) == "True"
                vida_jogador = int(dados_save.get("vida_jogador", 8))
                zumbis_mortos = int(dados_save.get("zumbis_mortos", 0))
                for i, zumbi in enumerate(lista_zumbis):
                    status_str = dados_save.get(f"zumbi_{i}_vivo", "True")
                    zumbi["vivo"] = (status_str == "True")
                    morto_str = dados_save.get(f"zumbi_{i}_morto", "False")
                    zumbi["morto"] = (morto_str == "True")
                    if zumbi["morto"]:
                        zumbi["frame"] = len(ANIMACOES_ZUMBI[zumbi["tipo"]]["death"]["left"]) - 1
                

                if morto:
                    if ultima_direcao == "left": animacao_atual = morte_left_list
                    else: animacao_atual = morte_right_list
                    frame = len(animacao_atual) - 1
                elif ultima_direcao == "down": animacao_atual = idle_down_list
                elif ultima_direcao == "up": animacao_atual = idle_up_list
                elif ultima_direcao == "left": animacao_atual = idle_left_list
                elif ultima_direcao == "right": animacao_atual = idle_right_list
            except (ValueError, TypeError) as erro:
                print(f"[SAVE] Save invalido, iniciando um novo jogo: {erro}")
        else:
            print("[SAVE] Nenhum save encontrado, iniciando um novo jogo.")

    rodando_jogo = True

    while rodando_jogo:
        dt = clock.tick(60)
        perto_do_taco = (abs(jogador.centerx - taco_rect.centerx) < 20 and abs(jogador.centery - taco_rect.centery) < 20)

        for evento in pygame.event.get():
            if evento.type == QUIT:
                salvar_jogo()
                pygame.quit()
                sys.exit()

            if evento.type == KEYDOWN and evento.key == K_s:
                if mensagem_cama_ativa:
                    mensagem_cama_ativa = False

            if evento.type == KEYDOWN and evento.key == K_ESCAPE:
                resultado_pausa = tela_pausa()
                if resultado_pausa == "sair":
                    salvar_jogo()
                    rodando_jogo = False

            if evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                if tem_taco ==True:
                    som_taco.play()
                if not atacar and not pegar and not morrer and not morto and not mensagem_cama_ativa:
                    atacar = True
                    anim_time = 0
                    frame = 0

                    if ultima_direcao == 'down': animacao_atual = soco_down_list
                    elif ultima_direcao == 'up': animacao_atual = soco_up_list
                    elif ultima_direcao == 'left': animacao_atual = soco_left_list
                    elif ultima_direcao == 'right': animacao_atual = soco_right_list

                    
                    for zumbi in lista_zumbis:
                        if zumbi["vivo"] and zumbi["dano_cooldown"] <= 0:
                            dist = math.hypot(jogador.centerx - zumbi["rect"].centerx, jogador.centery - zumbi["rect"].centery)
                            if dist <= alcance_ataque_jogador:
                                if tem_taco == False:
                                    zumbi["vida"] -= 1
                                    zumbi["dano_cooldown"] = 500
                                    som_soco.play()
                                elif tem_taco == True:
                                    zumbi["vida"] -= 2
                                    zumbi["dano_cooldown"] = 500
                                    som_taco.play()
                                if zumbi["vida"] <= 0:
                                    zumbi["vivo"] = False
                                    zumbis_mortos += 1
                                    zumbi["atacando"] = False
                                    zumbi["morrendo"] = True
                                    zumbi["frame"] = 0
                                    zumbi["anim_time"] = 0

            if evento.type == KEYDOWN and evento.key == K_e:
                if not pegar and not atacar and not morrer and not morto:
                    if perto_do_taco and taco_no_chao:
                        pegar = True
                        taco_no_chao = False
                        tem_taco = True
                        anim_time = 0
                        frame = 0

                        if ultima_direcao == 'down': animacao_atual = pegar_down_list
                        elif ultima_direcao == 'up': animacao_atual = pegar_up_list
                        elif ultima_direcao == 'left': animacao_atual = pegar_left_list
                        elif ultima_direcao == 'right': animacao_atual = pegar_right_list
                
                if jogador.colliderect(area_final):
                    acao = mostrar_final()
                    if acao == "menu":
                        rodando_jogo = False

                        # Abrir portas
                if not morto and not morrer:
                    if jogador.colliderect(area_teleporte):
                        jogador.x = destino_x
                        jogador.y = destino_y
                        som_porta2.play()

                
                if not morto and not morrer:
                    if jogador.colliderect(area_teleporte2):
                        jogador.x = destino_x2
                        jogador.y = destino_y2
                        som_porta2.play()

                if not morto and not morrer:
                    if jogador.colliderect(area_teleporte3):
                        jogador.x = destino_x3
                        jogador.y = destino_y3
                        som_porta2.play()

                if not morto and not morrer:
                    if jogador.colliderect(area_teleporte4):
                        jogador.x = destino_x4
                        jogador.y = destino_y4
                        som_porta2.play()
                
                if not morto and not morrer:
                    if jogador.colliderect(area_teleporte5):
                        jogador.x = destino_x5
                        jogador.y = destino_y5
                        som_porta2.play()
                
                if not morto and not morrer:
                    if jogador.colliderect(area_teleporte6):
                        jogador.x = destino_x6
                        jogador.y = destino_y6
                        som_porta2.play()

                if not morto and not morrer:
                    if jogador.colliderect(area_teleporte7):
                        jogador.x = destino_x7
                        jogador.y = destino_y7
                        som_porta2.play()

            if evento.type == KEYDOWN and evento.key == K_l:
                if not morrer and not morto:
                    morrer = True
                    frame = 0
                    anim_time = 0

                    if ultima_direcao == 'right': animacao_atual = morte_right_list
                    elif ultima_direcao == 'left': animacao_atual = morte_left_list

        if not rodando_jogo:
            break

        teclas = pygame.key.get_pressed()

        if not atacar and not pegar and not morrer and not morto:
            vel = velocidade_shift if teclas[K_LSHIFT] else velocidade
            mover = False
            dx = 0; dy = 0

            if teclas[K_a]: dx -= 1; animacao_atual = run_left_list; ultima_direcao = 'left'
            if teclas[K_d]: dx += 1; animacao_atual = run_right_list; ultima_direcao = 'right'
            if teclas[K_w]: dy -= 1; animacao_atual = run_up_list; ultima_direcao = 'up'
            if teclas[K_s]: dy += 1; animacao_atual = run_down_list; ultima_direcao = 'down'
                
            if dx != 0 or dy != 0:
                tamanho = math.sqrt(dx * dx + dy * dy)
                dx /= tamanho
                dy /= tamanho
                dx *= vel
                dy *= vel
                mover = True

            jogador.x += dx
            for parede in paredes:
                if jogador.colliderect(parede):
                    if dx > 0: jogador.right = parede.left
                    elif dx < 0: jogador.left = parede.right

            jogador.y += dy
            for parede in paredes:
                if jogador.colliderect(parede):
                    if dy > 0: jogador.bottom = parede.top
                    elif dy < 0: jogador.top = parede.bottom

            if not mover:
                if ultima_direcao == "down": animacao_atual = idle_down_list
                elif ultima_direcao == "up": animacao_atual = idle_up_list
                elif ultima_direcao == "left": animacao_atual = idle_left_list
                elif ultima_direcao == "right": animacao_atual = idle_right_list

        if dano_cooldown_jogador > 0:
            dano_cooldown_jogador -= dt
            flash_timer_jogador += dt
            if flash_timer_jogador >= 80:
                flash_timer_jogador = 0
                mostrar_vermelho_jogador = not mostrar_vermelho_jogador
        else:
            mostrar_vermelho_jogador = False

        for zumbi in lista_zumbis:

            if zumbi["morrendo"]:
                zumbi["anim_time"] += dt
                if zumbi["anim_time"] >= 96:
                    zumbi["anim_time"] = 0
                    max_frame_morte = len(ANIMACOES_ZUMBI[zumbi["tipo"]]["death"]["left"]) - 1
                    if zumbi["frame"] < max_frame_morte:
                        zumbi["frame"] += 1
                    else:
                        zumbi["morrendo"] = False
                        zumbi["morto"] = True  
                continue

            if zumbi["morto"]:
                continue  

            if not zumbi["vivo"]:
                continue

            if zumbi["dano_cooldown"] > 0:
                zumbi["dano_cooldown"] -= dt
                zumbi["flash_timer"] += dt
                if zumbi["flash_timer"] >= 80:
                    zumbi["flash_timer"] = 0
                    zumbi["mostrar_vermelho"] = not zumbi["mostrar_vermelho"]
            else:
                zumbi["mostrar_vermelho"] = False

            if zumbi["ataque_cooldown"] > 0:
                zumbi["ataque_cooldown"] -= dt

            dx_z = jogador.centerx - zumbi["rect"].centerx
            dy_z = jogador.centery - zumbi["rect"].centery
            distancia = math.hypot(dx_z, dy_z)

            zumbi["movendo"] = False

            if zumbi["atacando"]:
                zumbi["ataque_anim_time"] += dt
                if zumbi["ataque_anim_time"] >= 96:
                    zumbi["ataque_anim_time"] = 0
                    zumbi["ataque_frame"] += 1

                    if (zumbi["ataque_frame"] >= 3 and not zumbi["dano_aplicado"]
                            and not morto and dano_cooldown_jogador <= 0
                            and distancia <= 16):
                        zumbi["dano_aplicado"] = True
                        vida_jogador -= zumbi["dano"]
                        som_vida.play()
                        dano_cooldown_jogador = dano_cooldown_max
                        if vida_jogador <= 0 and not morrer and not morto:
                            morrer = True
                            frame = 0
                            anim_time = 0
                            if ultima_direcao == 'right': animacao_atual = morte_right_list
                            elif ultima_direcao == 'left': animacao_atual = morte_left_list

                    if zumbi["ataque_frame"] >= 4:
                        zumbi["ataque_frame"] = 0
                        zumbi["atacando"] = False
                        zumbi["ataque_cooldown"] = 900

            elif distancia <= 15 and not morto and zumbi["ataque_cooldown"] <= 0:
                zumbi["atacando"] = True
                zumbi["dano_aplicado"] = False
                zumbi["ataque_frame"] = 0
                zumbi["ataque_anim_time"] = 0

            elif 14 < distancia <= zumbi["alcance_deteccao"] and not morto:
                zumbi["movendo"] = True
                dx_norm = dx_z / distancia
                dy_norm = dy_z / distancia

                zumbi["rect"].x += dx_norm * zumbi["velocidade"]
                for parede in paredes:
                    if zumbi["rect"].colliderect(parede):
                        if dx_norm > 0: zumbi["rect"].right = parede.left
                        elif dx_norm < 0: zumbi["rect"].left = parede.right

                zumbi["rect"].y += dy_norm * zumbi["velocidade"]
                for parede in paredes:
                    if zumbi["rect"].colliderect(parede):
                        if dy_norm > 0: zumbi["rect"].bottom = parede.top
                        elif dy_norm < 0: zumbi["rect"].top = parede.bottom

      
                if abs(dx_z) > abs(dy_z) * 1.5:
                    zumbi["direcao"] = "right" if dx_z > 0 else "left"
                elif abs(dy_z) > abs(dx_z) * 1.5:
                    zumbi["direcao"] = "down" if dy_z > 0 else "up"
            
            if not zumbi["atacando"]:
                zumbi["anim_time"] += dt
                if zumbi["anim_time"] >= 96:
                    zumbi["anim_time"] = 0
                    zumbi["frame"] = (zumbi["frame"] + 1) % 6

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
            elif not morto:
                frame += 1
                if frame >= len(animacao_atual):
                    frame = 0
                    if atacar: atacar = False
                    if pegar:
                        pegar = False
                        if ultima_direcao == 'down': animacao_atual = idle_down_list
                        elif ultima_direcao == 'up': animacao_atual = idle_up_list
                        elif ultima_direcao == 'left': animacao_atual = idle_left_list
                        elif ultima_direcao == 'right': animacao_atual = idle_right_list

        camera_x = jogador.centerx - (LARGURA // ZOOM) // 2
        camera_y = jogador.centery - (ALTURA // ZOOM) // 2

        tela_jogo.fill((0, 0, 0))
        
        sprite_base = animacao_atual[frame]
        if mostrar_vermelho_jogador:
            sprite = obter_sprite_vermelha(sprite_base)
        else:
            sprite = sprite_base

        offset_x = (sprite.get_width() - jogador.width) // 2
        offset_y = sprite.get_height() - jogador.height
        pos_sprite = (jogador.x - camera_x - offset_x, jogador.y - camera_y - offset_y)

        taco_sprite = None
        pos_taco = None
        if tem_taco and not pegar and not morrer and not morto:
            if atacar:
                if ultima_direcao == 'down': taco_sprite = taco_down_ataque_list[frame]
                elif ultima_direcao == 'up': taco_sprite = taco_up_ataque_list[frame]
                elif ultima_direcao == 'left': taco_sprite = taco_left_ataque_list[frame]
                elif ultima_direcao == 'right': taco_sprite = taco_right_ataque_list[frame]
            else:
                if ultima_direcao == 'down': taco_sprite = taco_down_idle_list[frame]
                elif ultima_direcao == 'up': taco_sprite = taco_up_idle_list[frame]
                elif ultima_direcao == 'left': taco_sprite = taco_left_idle_list[frame]
                elif ultima_direcao == 'right': taco_sprite = taco_right_idle_list[frame]

            taco_offset_x = (taco_sprite.get_width() - jogador.width) // 2
            taco_offset_y = taco_sprite.get_height() - jogador.height
            pos_taco = (jogador.x - camera_x - taco_offset_x, jogador.y - camera_y - taco_offset_y)
        
        for layer in MapaOriginal.visible_layers:
            if hasattr(layer, "data"):
                for x, y, gid in layer:
                    tile = MapaOriginal.get_tile_image_by_gid(gid)
                    if tile:
                        tela_jogo.blit(tile, (x * TILE - camera_x, y * TILE - camera_y))

            if layer.name == "JOGADOR":
                if taco_sprite is not None and ultima_direcao == "up": tela_jogo.blit(taco_sprite, pos_taco)
                tela_jogo.blit(sprite, pos_sprite)
                if taco_sprite is not None and ultima_direcao != "up": tela_jogo.blit(taco_sprite, pos_taco)


                for zumbi in lista_zumbis:
                    if zumbi["vivo"] or zumbi["morrendo"] or zumbi["morto"]:

                        anims_tipo = ANIMACOES_ZUMBI[zumbi["tipo"]]

                        if zumbi["morrendo"] or zumbi["morto"]:
                            anim_z = anims_tipo["death"]["left"] if zumbi["direcao"] == "left" else anims_tipo["death"]["right"]
                            indice_frame = zumbi["frame"]

                        elif zumbi["atacando"]:
                            anim_z = anims_tipo["attack"][zumbi["direcao"]]
                            indice_frame = zumbi["ataque_frame"]

                        elif zumbi["movendo"]:
                            anim_z = anims_tipo["walk"][zumbi["direcao"]]
                            indice_frame = zumbi["frame"]

                        else:
                            anim_z = anims_tipo["idle"][zumbi["direcao"]]
                            indice_frame = zumbi["frame"]

                        indice_frame = min(indice_frame, len(anim_z) - 1)
                        zumbi_sprite_base = anim_z[indice_frame]
                        
                        if zumbi["mostrar_vermelho"] and zumbi["vivo"]:
                            zumbi_sprite = obter_sprite_vermelha(zumbi_sprite_base)
                        else:
                            zumbi_sprite = zumbi_sprite_base

                        z_offset_x = (zumbi_sprite.get_width() - zumbi["rect"].width) // 2
                        z_offset_y = zumbi_sprite.get_height() - zumbi["rect"].height
                        z_pos = (zumbi["rect"].x - camera_x - z_offset_x, zumbi["rect"].y - camera_y - z_offset_y)
                        
                        tela_jogo.blit(zumbi_sprite, z_pos)

        if taco_no_chao:
            tela_jogo.blit(imagem_taco, (taco_rect.x - camera_x, taco_rect.y - camera_y))

        #teste
        #pygame.draw.rect(tela_jogo, (0, 0, 255), (area_teleporte6.x - camera_x, area_teleporte6.y - camera_y, area_teleporte6.width, area_teleporte6.height), 2)
        #pygame.draw.rect(tela_jogo, (0, 0, 255), (area_teleporte7.x - camera_x, area_teleporte7.y - camera_y, area_teleporte7.width, area_teleporte7.height), 2)

        tela_zoom = pygame.transform.scale(tela_jogo, (LARGURA, ALTURA))
        tela.blit(tela_zoom, (0, 0))

        for zumbi in lista_zumbis:
            if zumbi["vivo"]:
                desenhar_hud_zumbi(tela_jogo, zumbi, camera_x, camera_y)

        tela_zoom = pygame.transform.scale(tela_jogo, (LARGURA, ALTURA))
        tela.blit(tela_zoom, (0, 0))

        if morto:
            acao = tela_game_over()
            if acao == "sair":
                rodando_jogo = False 

        if mensagem_cama_ativa:
            texto_cama = "APERTE 'S' PARA LEVANTAR DA CAMA"
            sombra_txt = fonte_mensagem_cama.render(texto_cama, True, (10, 10, 15))
            branco_txt = fonte_mensagem_cama.render(texto_cama, True, (200, 200, 190))
            rect_txt = branco_txt.get_rect(center=(LARGURA // 2, ALTURA - 60))

            tela.blit(sombra_txt, (rect_txt.x + 3, rect_txt.y + 3))
            tela.blit(branco_txt, rect_txt)

        texto_kills = fonte_botao_menu.render(f"Kills: {zumbis_mortos}", True, COR_TITULO_BRANCO)
        sombra_kills = fonte_botao_menu.render(f"Kills: {zumbis_mortos}", True, COR_SOMBRA)
        
        pos_x_kills = LARGURA - texto_kills.get_width() - 20
        pos_y_kills = 20
        
        tela.blit(sombra_kills, (pos_x_kills + 2, pos_y_kills + 2))
        tela.blit(texto_kills, (pos_x_kills, pos_y_kills))

        
        desenhar_hud_jogador(tela, vida_jogador)


        pygame.display.flip()