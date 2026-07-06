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

#Morrer
morte_right = pygame.image.load('Character_side_death3-Sheet6.png')
morte_left = pygame.image.load('Character_side-left_death3-Sheet7.png')

#Taco
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

morte_right_list = []
morte_left_list = []

taco_down_ataque_list = []
taco_up_ataque_list = []
taco_left_ataque_list = []
taco_right_ataque_list = []

taco_down_idle_list = []
taco_up_idle_list = []
taco_left_idle_list = []
taco_right_idle_list = []

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
    taco_down_idle_list.append(pygame.transform.scale(taco_down_idle.subsurface((i * 17, 0, 17, 11)), (16, 16)))
    taco_up_idle_list.append(pygame.transform.scale(taco_up_idle.subsurface((i * 16, 0, 16, 11)), (16, 16)))
    taco_left_idle_list.append(pygame.transform.scale(taco_left_idle.subsurface((i * 16, 0, 16, 13)), (16, 16)))
    taco_right_idle_list.append(pygame.transform.scale(taco_right_idle.subsurface((i * 16, 0, 16, 13)), (16, 16)))

#Soco
for i in range(4):
    soco_down_list.append(pygame.transform.scale(soco_down.subsurface((i * 12, 0, 12, 18)), (16, 16)))
    soco_up_list.append(pygame.transform.scale(soco_up.subsurface((i * 12, 0, 12, 17)), (16, 16)))
    soco_left_list.append(pygame.transform.scale(soco_left.subsurface((i * 20, 0, 20, 18)), (20, 20)))
    soco_right_list.append(pygame.transform.scale(soco_right.subsurface((i * 20, 0, 20, 18)), (20, 20)))
    taco_down_ataque_list.append(pygame.transform.scale(taco_down_ataque.subsurface((i * 20, 0, 20, 25)), (16, 16)))
    taco_up_ataque_list.append(pygame.transform.scale(taco_up_ataque.subsurface((i * 20, 0, 20, 25)), (16, 16)))
    taco_left_ataque_list.append(pygame.transform.scale(taco_left_ataque.subsurface((i * 28, 0, 28, 16)), (20, 20)))
    taco_right_ataque_list.append(pygame.transform.scale(taco_right_ataque.subsurface((i * 28, 0, 28, 16)), (20, 20)))

#Pegar
for i in range(3):
    pegar_down_list.append(pygame.transform.scale(pegar_down.subsurface((i * 12, 0, 12, 16)), (16, 16)))
    pegar_up_list.append(pygame.transform.scale(pegar_up.subsurface((i * 11, 0, 11, 15)), (16, 16)))
    pegar_left_list.append(pygame.transform.scale(pegar_left.subsurface((i * 11, 0, 11, 16)), (16, 16)))
    pegar_right_list.append(pygame.transform.scale(pegar_right.subsurface((i * 11, 0, 11, 16)), (16, 16)))

#Morte
for i in range(7):
    morte_left_list.append(pygame.transform.scale(morte_left.subsurface((i * 21, 0, 21, 16)), (20, 20)))
    morte_right_list.append(pygame.transform.scale(morte_right.subsurface((i * 21, 0, 21, 16)), (20, 20)))

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
COR_BOTAO_DETALHE = (180, 80, 80) # As braçadeiras laterais
COR_CAVEIRA = (200, 60, 150)
COR_BOTAO_DESABILITADO = (40, 50, 60)
COR_SOMBRA = (10, 10, 15)

def desenhar_caveira_pixelada(superficie, x, y, cor):
    """Desenha uma caveira estilo pixel art usando retângulos (substituto da imagem)"""
    # Crânio
    pygame.draw.rect(superficie, cor, (x - 8, y - 8, 16, 12))
    # Maxilar
    pygame.draw.rect(superficie, cor, (x - 5, y + 4, 10, 5))
    # Olhos 
    pygame.draw.rect(superficie, COR_SOMBRA, (x - 6, y - 3, 4, 4))
    pygame.draw.rect(superficie, COR_SOMBRA, (x + 2, y - 3, 4, 4))
    # Nariz
    pygame.draw.rect(superficie, COR_SOMBRA, (x - 1, y + 1, 2, 3))
    # Dentes 
    pygame.draw.line(superficie, COR_SOMBRA, (x - 2, y + 5), (x - 2, y + 8), 1)
    pygame.draw.line(superficie, COR_SOMBRA, (x + 1, y + 5), (x + 1, y + 8), 1)

def desenhar_botao_menu(superficie, rect, texto, mouse_pos, habilitado=True):
    hover = rect.collidepoint(mouse_pos) if habilitado else False
    
    # Cores 
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
    """Renderiza o mapa original ao fundo com um filtro escuro por cima para simular a imagem"""
    for layer in MapaOriginal.visible_layers:
        
        if hasattr(layer, "data"):
            for x, y, gid in layer:
                tile = MapaOriginal.get_tile_image_by_gid(gid)
                if tile:
                    tile_zoom = pygame.transform.scale(tile, (int(16 * ZOOM), int(16 * ZOOM)))
                    superficie.blit(tile_zoom, (x * int(16 * ZOOM), y * int(16 * ZOOM)))
    
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((10, 20, 25, 210)) # Teal muito escuro e quase opaco
    superficie.blit(overlay, (0, 0))

def desenhar_titulo_jogo(superficie):
    """Renderiza o titulo estilizado 'INTO THE EPIDEMIC'"""
    centro_x = LARGURA // 2
    
    # "INTO THE"
    texto_into = fonte_titulo_menor.render("INTO THE", True, COR_TITULO_BRANCO)
    sombra_into = fonte_titulo_menor.render("INTO THE", True, COR_SOMBRA)
    rect_into = texto_into.get_rect(center=(centro_x, 120))
    superficie.blit(sombra_into, (rect_into.x + 4, rect_into.y + 4))
    superficie.blit(texto_into, rect_into)

    # "EPIDEMIC" dividido para ter o D em vermelho
    # EPI
    texto_epi = fonte_titulo_maior.render("EPI", True, COR_TITULO_VERDE)
    sombra_epi = fonte_titulo_maior.render("EPI", True, COR_SOMBRA)
    # D
    texto_d = fonte_titulo_maior.render("D", True, COR_TITULO_VERMELHO)
    sombra_d = fonte_titulo_maior.render("D", True, COR_SOMBRA)
    # EMIC
    texto_emic = fonte_titulo_maior.render("EMIC", True, COR_TITULO_VERDE)
    sombra_emic = fonte_titulo_maior.render("EMIC", True, COR_SOMBRA)

    largura_total = texto_epi.get_width() + texto_d.get_width() + texto_emic.get_width()
    inicio_x = centro_x - (largura_total // 2)
    y_epidemic = 170

    # EPI
    superficie.blit(sombra_epi, (inicio_x + 5, y_epidemic + 5))
    superficie.blit(texto_epi, (inicio_x, y_epidemic))
    inicio_x += texto_epi.get_width()
    
    # D
    superficie.blit(sombra_d, (inicio_x + 5, y_epidemic + 5))
    superficie.blit(texto_d, (inicio_x, y_epidemic))
    inicio_x += texto_d.get_width()

    # EMIC
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
    overlay.fill((10, 20, 25, 200)) # Mantém a paleta escura da imagem

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
        
        # Desenha pausa
        tela.blit(sombra_pausa, (titulo_pausa_rect.x + 5, titulo_pausa_rect.y + 5))
        tela.blit(titulo_pausa, titulo_pausa_rect)

        desenhar_botao_menu(tela, botao_continuar_pausa, "CONTINUAR", mouse_pos)
        desenhar_botao_menu(tela, botao_sair_pausa, "SAIR", mouse_pos)

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
  

    jogador = pygame.Rect(95, 280, 16, 16)
    taco_rect = pygame.Rect(450, 270, 16, 16)
    taco_no_chao = True
    tem_taco = False
    perto_do_taco = False

    # Estado de animação
    animacao_atual = idle_right_list
    ultima_direcao = "right"
    frame = 0
    anim_time = 0

    atacar = False
    pegar = False
    morto = False
    morrer = False

    velocidade = 1
    velocidade_shift = 1.6

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

                if morto:
                    if ultima_direcao == "left":
                        animacao_atual = morte_left_list
                    else:
                        animacao_atual = morte_right_list
                    frame = len(animacao_atual) - 1
                elif ultima_direcao == "down":
                    animacao_atual = idle_down_list
                elif ultima_direcao == "up":
                    animacao_atual = idle_up_list
                elif ultima_direcao == "left":
                    animacao_atual = idle_left_list
                elif ultima_direcao == "right":
                    animacao_atual = idle_right_list
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
                if not atacar and not pegar and not morrer and not morto and not mensagem_cama_ativa:
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

            if evento.type == KEYDOWN and evento.key == K_e:
                if not pegar and not atacar and not morrer and not morto:
                    if perto_do_taco and taco_no_chao:
                        pegar = True
                        taco_no_chao = False
                        tem_taco = True
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

            if evento.type == KEYDOWN and evento.key == K_l:
                if not morrer and not morto:
                    morrer = True
                    frame = 0
                    anim_time = 0

                    if ultima_direcao == 'right':
                        animacao_atual = morte_right_list
                    elif ultima_direcao == 'left':
                        animacao_atual = morte_left_list

        if not rodando_jogo:
            break

        teclas = pygame.key.get_pressed()

        if not atacar and not pegar and not morrer and not morto:
            vel = velocidade_shift if teclas[K_LSHIFT] else velocidade
            mover = False

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

            jogador.x += dx
            for parede in paredes:
                if jogador.colliderect(parede):
                    if dx > 0:
                        jogador.right = parede.left
                    elif dx < 0:
                        jogador.left = parede.right

            jogador.y += dy
            for parede in paredes:
                if jogador.colliderect(parede):
                    if dy > 0:
                        jogador.bottom = parede.top
                    elif dy < 0:
                        jogador.top = parede.bottom

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

        camera_x = jogador.centerx - (LARGURA // ZOOM) // 2
        camera_y = jogador.centery - (ALTURA // ZOOM) // 2

        tela_jogo.fill((0, 0, 0))
        sprite = animacao_atual[frame]

        offset_x = (sprite.get_width() - jogador.width) // 2
        offset_y = sprite.get_height() - jogador.height

        pos_sprite = (jogador.x - camera_x - offset_x,jogador.y - camera_y - offset_y)

        taco_sprite = None
        pos_taco = None
        if tem_taco and not pegar and not morrer and not morto:
            if atacar:
                if ultima_direcao == 'down':
                    taco_sprite = taco_down_ataque_list[frame]
                elif ultima_direcao == 'up':
                    taco_sprite = taco_up_ataque_list[frame]
                elif ultima_direcao == 'left':
                    taco_sprite = taco_left_ataque_list[frame]
                elif ultima_direcao == 'right':
                    taco_sprite = taco_right_ataque_list[frame]
            else:
                if ultima_direcao == 'down':
                    taco_sprite = taco_down_idle_list[frame]
                elif ultima_direcao == 'up':
                    taco_sprite = taco_up_idle_list[frame]
                elif ultima_direcao == 'left':
                    taco_sprite = taco_left_idle_list[frame]
                elif ultima_direcao == 'right':
                    taco_sprite = taco_right_idle_list[frame]

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

                if taco_sprite is not None and ultima_direcao == "up":
                    tela_jogo.blit(taco_sprite, pos_taco)

                tela_jogo.blit(sprite, pos_sprite)

                if taco_sprite is not None and ultima_direcao != "up":
                    tela_jogo.blit(taco_sprite, pos_taco)


        if taco_no_chao:
            tela_jogo.blit(imagem_taco, (taco_rect.x - camera_x, taco_rect.y - camera_y))

        sprite = animacao_atual[frame]
        offset_x = (sprite.get_width() - jogador.width) // 2
        offset_y = sprite.get_height() - jogador.height
        pos_sprite = (jogador.x - camera_x - offset_x, jogador.y - camera_y - offset_y)




      

        tela_zoom = pygame.transform.scale(tela_jogo, (LARGURA, ALTURA))
        tela.blit(tela_zoom, (0, 0))
        # Essa linha já existe no seu código:
        tela.blit(tela_zoom, (0, 0))

        # === CÓDIGO NOVO: DESENHAR A MENSAGEM COM SOMBRA ===
        if mensagem_cama_ativa:
            texto_cama = "APERTE 'S' PARA LEVANTAR DA CAMA"
            # Renderiza a sombra escura
            sombra_txt = fonte_mensagem_cama.render(texto_cama, True, (10, 10, 15))
            # Renderiza o texto claro
            branco_txt = fonte_mensagem_cama.render(texto_cama, True, (200, 200, 190))
            
            # Centraliza o texto na parte de baixo da tela
            rect_txt = branco_txt.get_rect(center=(LARGURA // 2, ALTURA - 60))
            
            # Desenha a sombra um pouquinho pro lado (+3 pixels) e depois o texto branco
            tela.blit(sombra_txt, (rect_txt.x + 3, rect_txt.y + 3))
            tela.blit(branco_txt, rect_txt)
        # ===================================================

        # Essa linha já existe no seu código:
        
        pygame.display.flip()