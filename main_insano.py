import pygame
import sys
import math
import random
from pytmx.util_pygame import load_pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN, K_w, K_a, K_s, K_d, K_e, K_LSHIFT, K_SPACE

pygame.init()
pygame.mixer.init()

# ===== CONFIGURAÇÕES =====
LARGURA = 800
ALTURA = 600
ZOOM = 2
TILE = 16
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("🔥 COMBATE FINAL 🔥")
clock = pygame.time.Clock()

# ===== CARREGAMENTO DO MAPA =====
MapaOriginal = load_pygame("MapaOriginal.tmx")
tela_jogo = pygame.Surface((LARGURA // ZOOM, ALTURA // ZOOM))

# Colisões
paredes = []
camada_colisao = MapaOriginal.get_layer_by_name("Colisao")
for x, y, gid in camada_colisao:
    if gid:
        paredes.append(pygame.Rect(x * TILE, y * TILE, TILE, TILE))

MAPA_LARGURA = MapaOriginal.width * TILE
MAPA_ALTURA = MapaOriginal.height * TILE

# ===== SISTEMA DE PARTÍCULAS =====
class Particula:
    def __init__(self, x, y, vel_x, vel_y, cor, tamanho=3, vida=30):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.cor = cor
        self.tamanho = tamanho
        self.vida = vida
        self.vida_max = vida

    def atualizar(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.1  # Gravidade
        self.vida -= 1

    def desenhar(self, surface, camera_x, camera_y):
        alpha = int(255 * (self.vida / self.vida_max))
        cor_com_alpha = (*self.cor[:3], alpha)
        pygame.draw.circle(surface, self.cor, (int(self.x - camera_x), int(self.y - camera_y)), self.tamanho)

    def vivo(self):
        return self.vida > 0

# ===== SISTEMA DE INIMIGOS =====
class Inimigo:
    def __init__(self, x, y, jogador, dificuldade=1):
        self.x = x
        self.y = y
        self.jogador = jogador
        self.rect = pygame.Rect(x, y, 14, 14)
        self.vel_x = 0
        self.vel_y = 0
        self.velocidade = 1 + (dificuldade * 0.3)
        self.vida = 3 * dificuldade
        self.vida_max = self.vida
        self.dano = 1 * dificuldade
        self.alcance = 30
        self.tempo_ataque = 0
        self.cooldown_ataque = 60
        self.cor = (255, 50, 50)
        self.dificuldade = dificuldade

    def atualizar(self, paredes, particulas):
        # Movimento em direção ao jogador
        dx = self.jogador.x - self.x
        dy = self.jogador.y - self.y
        distancia = math.sqrt(dx**2 + dy**2)

        if distancia > 0:
            self.vel_x = (dx / distancia) * self.velocidade
            self.vel_y = (dy / distancia) * self.velocidade

        # Movimento X com colisão
        self.x += self.vel_x
        self.rect.x = self.x
        for parede in paredes:
            if self.rect.colliderect(parede):
                if self.vel_x > 0:
                    self.x = parede.left - self.rect.width
                else:
                    self.x = parede.right

        # Movimento Y com colisão
        self.y += self.vel_y
        self.rect.y = self.y
        for parede in paredes:
            if self.rect.colliderect(parede):
                if self.vel_y > 0:
                    self.y = parede.top - self.rect.height
                else:
                    self.y = parede.bottom

        self.rect.x = self.x
        self.rect.y = self.y

        # Cooldown de ataque
        if self.tempo_ataque > 0:
            self.tempo_ataque -= 1

        # Limites do mapa
        self.x = max(0, min(self.x, MAPA_LARGURA - self.rect.width))
        self.y = max(0, min(self.y, MAPA_ALTURA - self.rect.height))

    def desenhar(self, surface, camera_x, camera_y):
        # Corpo
        pygame.draw.rect(surface, self.cor, (self.x - camera_x, self.y - camera_y, self.rect.width, self.rect.height))
        
        # Olhos
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x - camera_x + 4), int(self.y - camera_y + 4)), 2)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x - camera_x + 10), int(self.y - camera_y + 4)), 2)
        
        # Barra de vida
        barra_largura = 14
        barra_altura = 2
        barra_x = self.x - camera_x
        barra_y = self.y - camera_y - 5
        
        pygame.draw.rect(surface, (50, 50, 50), (barra_x, barra_y, barra_largura, barra_altura))
        vida_ratio = self.vida / self.vida_max
        pygame.draw.rect(surface, (0, 255, 0), (barra_x, barra_y, barra_largura * vida_ratio, barra_altura))

    def sofrer_dano(self, dano, particulas, x_origem, y_origem):
        self.vida -= dano
        
        # Knockback
        dx = self.x - x_origem
        dy = self.y - y_origem
        distancia = math.sqrt(dx**2 + dy**2) or 1
        
        self.x += (dx / distancia) * 5
        self.y += (dy / distancia) * 5

        # Partículas de dano
        for _ in range(5):
            vel_x = random.uniform(-2, 2)
            vel_y = random.uniform(-3, -1)
            particulas.append(Particula(self.x, self.y, vel_x, vel_y, (255, 100, 0), 3, 20))

    def vivo(self):
        return self.vida > 0

# ===== JOGADOR MELHORADO =====
class Jogador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 16, 16)
        self.velocidade = 1
        self.velocidade_shift = 1.5
        self.vida = 20
        self.vida_max = 20
        self.stamina = 100
        self.stamina_max = 100
        self.stamina_recover = 1
        self.stamina_cost = 0.5
        self.dano = 5
        self.alcance_ataque = 40
        self.tempo_ataque = 0
        self.cooldown_ataque = 20
        self.contador_hits = 0
        self.score = 0
        self.nivel = 1

    def sofrer_dano(self, dano):
        self.vida -= dano
        self.vida = max(0, self.vida)

    def curar(self, quantidade):
        self.vida = min(self.vida + quantidade, self.vida_max)

    def adicionar_score(self, pontos):
        self.score += pontos
        if self.score % 500 == 0:  # Level up a cada 500 pontos
            self.nivel += 1
            self.vida_max += 5
            self.vida = self.vida_max
            self.dano += 1

# ===== CARREGAMENTO DE ANIMAÇÕES =====
def carregar_sprites():
    sprites = {}
    
    try:
        # Idle
        idle_down = pygame.image.load('Character_down_idle-Sheet6.png')
        idle_right = pygame.image.load('Character_side_idle-Sheet6.png')
        idle_left = pygame.image.load('Character_side-left_idle-Sheet6.png')
        idle_up = pygame.image.load('Character_up_idle-Sheet6.png')

        # Run
        run_down = pygame.image.load('Character_down_run-Sheet6.png')
        run_right = pygame.image.load('Character_side_run-Sheet6.png')
        run_left = pygame.image.load('Character_side-left_run-Sheet6.png')
        run_up = pygame.image.load('Character_up_run-Sheet6.png')

        # Punch
        soco_down = pygame.image.load('Character_down_punch-Sheet4.png')
        soco_up = pygame.image.load('Character_up_punch-Sheet4.png')
        soco_left = pygame.image.load('Character_side-left_punch-Sheet4.png')
        soco_right = pygame.image.load('Character_side_punch-Sheet4.png')

        # Pick-up
        pegar_down = pygame.image.load('Character_down_Pick-up-Sheet3.png')
        pegar_up = pygame.image.load('Character_up_Pick-up-Sheet3.png')
        pegar_left = pygame.image.load('Character_side-left_Pick-up-Sheet3.png')
        pegar_right = pygame.image.load('Character_side_Pick-up-Sheet3.png')

        # Criar dicionários
        for nome, sprite in [('idle_down', idle_down), ('idle_right', idle_right), 
                             ('idle_left', idle_left), ('idle_up', idle_up),
                             ('run_down', run_down), ('run_right', run_right),
                             ('run_left', run_left), ('run_up', run_up),
                             ('soco_down', soco_down), ('soco_up', soco_up),
                             ('soco_left', soco_left), ('soco_right', soco_right),
                             ('pegar_down', pegar_down), ('pegar_up', pegar_up),
                             ('pegar_left', pegar_left), ('pegar_right', pegar_right)]:
            sprites[nome] = sprite

        return sprites
    except:
        print("⚠️ Alguns sprites não encontrados, continuando sem eles...")
        return {}

# Carregar sprites
sprites = carregar_sprites()

# Processar animações
def processar_animacoes(sprites):
    animacoes = {}
    
    # Idle e Run (6 frames)
    for direcao, sprite_key_idle, sprite_key_run in [
        ('down', 'idle_down', 'run_down'),
        ('up', 'idle_up', 'run_up'),
        ('left', 'idle_left', 'run_left'),
        ('right', 'idle_right', 'run_right')
    ]:
        animacoes[f'idle_{direcao}_list'] = []
        animacoes[f'run_{direcao}_list'] = []
        
        if sprite_key_idle in sprites:
            sprite = sprites[sprite_key_idle]
            for i in range(6):
                pos_x = i * (sprite.get_width() // 6)
                subsurface = sprite.subsurface((pos_x, 0, sprite.get_width() // 6, sprite.get_height()))
                animacoes[f'idle_{direcao}_list'].append(pygame.transform.scale(subsurface, (16, 16)))
        
        if sprite_key_run in sprites:
            sprite = sprites[sprite_key_run]
            for i in range(6):
                pos_x = i * (sprite.get_width() // 6)
                subsurface = sprite.subsurface((pos_x, 0, sprite.get_width() // 6, sprite.get_height()))
                animacoes[f'run_{direcao}_list'].append(pygame.transform.scale(subsurface, (16, 16)))

    # Punch (4 frames)
    for direcao, sprite_key in [('down', 'soco_down'), ('up', 'soco_up'), ('left', 'soco_left'), ('right', 'soco_right')]:
        animacoes[f'soco_{direcao}_list'] = []
        if sprite_key in sprites:
            sprite = sprites[sprite_key]
            for i in range(4):
                pos_x = i * (sprite.get_width() // 4)
                subsurface = sprite.subsurface((pos_x, 0, sprite.get_width() // 4, sprite.get_height()))
                animacoes[f'soco_{direcao}_list'].append(pygame.transform.scale(subsurface, (16, 16)))

    # Pick-up (3 frames)
    for direcao, sprite_key in [('down', 'pegar_down'), ('up', 'pegar_up'), ('left', 'pegar_left'), ('right', 'pegar_right')]:
        animacoes[f'pegar_{direcao}_list'] = []
        if sprite_key in sprites:
            sprite = sprites[sprite_key]
            for i in range(3):
                pos_x = i * (sprite.get_width() // 3)
                subsurface = sprite.subsurface((pos_x, 0, sprite.get_width() // 3, sprite.get_height()))
                animacoes[f'pegar_{direcao}_list'].append(pygame.transform.scale(subsurface, (16, 16)))

    return animacoes

animacoes = processar_animacoes(sprites)

# ===== INICIALIZAÇÃO DO JOGO =====
jogador = Jogador(MAPA_LARGURA // 3.2, MAPA_ALTURA // 3)
animacao_atual = animacoes.get('idle_right_list', [pygame.Surface((16, 16))])
ultima_direcao = "right"
frame = 0
anim_time = 0
atacar = False
pegar = False

# Listas de entidades
inimigos = []
particulas = []
wave = 1
tempo_proximo_inimigo = 0
inimigos_derrotados = 0
tempo_jogo = 0
venceu = False

# Fonte para HUD
font_grande = pygame.font.Font(None, 48)
font_media = pygame.font.Font(None, 32)
font_pequena = pygame.font.Font(None, 24)

# ===== LOOP PRINCIPAL =====
running = True
while running:
    dt = clock.tick(FPS)
    tempo_jogo += dt

    # ===== EVENTOS =====
    for evento in pygame.event.get():
        if evento.type == QUIT:
            running = False

        if evento.type == MOUSEBUTTONDOWN and evento.button == 1:
            if not atacar and not pegar and jogador.tempo_ataque <= 0:
                atacar = True
                anim_time = 0
                frame = 0
                jogador.tempo_ataque = jogador.cooldown_ataque
                jogador.contador_hits = 0

                direcao_ataque = ultima_direcao
                if direcao_ataque in ['down', 'up', 'left', 'right']:
                    animacao_atual = animacoes.get(f'soco_{direcao_ataque}_list', animacoes.get('idle_right_list', [pygame.Surface((16, 16))]))

        if evento.type == KEYDOWN and evento.key == K_e:
            if not pegar and not atacar and jogador.tempo_ataque <= 0:
                pegar = True
                anim_time = 0
                frame = 0
                direcao_pegar = ultima_direcao
                animacao_atual = animacoes.get(f'pegar_{direcao_pegar}_list', animacoes.get('idle_right_list', [pygame.Surface((16, 16))]))

    # ===== ENTRADA =====
    teclas = pygame.key.get_pressed()

    if not atacar and not pegar:
        vel = jogador.velocidade_shift if teclas[K_LSHIFT] else jogador.velocidade
        
        if teclas[K_LSHIFT]:
            if jogador.stamina > 0:
                jogador.stamina -= jogador.stamina_cost
            else:
                vel = jogador.velocidade
        else:
            jogador.stamina = min(jogador.stamina + jogador.stamina_recover, jogador.stamina_max)

        mover = False
        dx = 0
        dy = 0

        if teclas[K_a]:
            dx = -vel
            animacao_atual = animacoes.get('run_left_list', animacoes.get('idle_right_list', [pygame.Surface((16, 16))]))
            ultima_direcao = 'left'
            mover = True

        if teclas[K_d]:
            dx = vel
            animacao_atual = animacoes.get('run_right_list', animacoes.get('idle_right_list', [pygame.Surface((16, 16))]))
            ultima_direcao = 'right'
            mover = True

        # Movimento X com colisão
        jogador.x += dx
        jogador.rect.x = jogador.x
        for parede in paredes:
            if jogador.rect.colliderect(parede):
                if dx > 0:
                    jogador.x = parede.left - jogador.rect.width
                else:
                    jogador.x = parede.right
                jogador.rect.x = jogador.x

        if teclas[K_w]:
            dy = -vel
            animacao_atual = animacoes.get('run_up_list', animacoes.get('idle_right_list', [pygame.Surface((16, 16))]))
            ultima_direcao = 'up'
            mover = True

        if teclas[K_s]:
            dy = vel
            animacao_atual = animacoes.get('run_down_list', animacoes.get('idle_right_list', [pygame.Surface((16, 16))]))
            ultima_direcao = 'down'
            mover = True

        # Movimento Y com colisão
        jogador.y += dy
        jogador.rect.y = jogador.y
        for parede in paredes:
            if jogador.rect.colliderect(parede):
                if dy > 0:
                    jogador.y = parede.top - jogador.rect.height
                else:
                    jogador.y = parede.bottom
                jogador.rect.y = jogador.y

        # Limites do mapa
        jogador.x = max(0, min(jogador.x, MAPA_LARGURA - jogador.rect.width))
        jogador.y = max(0, min(jogador.y, MAPA_ALTURA - jogador.rect.height))

        if not mover:
            animacao_atual = animacoes.get(f'idle_{ultima_direcao}_list', animacoes.get('idle_right_list', [pygame.Surface((16, 16))]))

    # Cooldown de ataque
    if jogador.tempo_ataque > 0:
        jogador.tempo_ataque -= 1

    # ===== ATUALIZAÇÃO DE ANIMAÇÃO =====
    anim_time += dt

    if len(animacao_atual) > 0:
        if anim_time >= 96:
            frame += 1
            anim_time = 0

            if frame >= len(animacao_atual):
                frame = 0
                if atacar:
                    # Checar colisão com inimigos
                    for inimigo in inimigos[:]:
                        dx = inimigo.x - jogador.x
                        dy = inimigo.y - jogador.y
                        distancia = math.sqrt(dx**2 + dy**2)

                        if distancia < jogador.alcance_ataque and inimigo.tempo_ataque <= 0:
                            inimigo.sofrer_dano(jogador.dano, particulas, jogador.x, jogador.y)
                            jogador.contador_hits += 1

                            # Partículas de impacto
                            for _ in range(8):
                                vel_x = random.uniform(-3, 3)
                                vel_y = random.uniform(-3, 1)
                                particulas.append(Particula(inimigo.x + 7, inimigo.y + 7, vel_x, vel_y, (255, 200, 0), 2, 15))

                    atacar = False

                if pegar:
                    pegar = False

                animacao_atual = animacoes.get(f'idle_{ultima_direcao}_list', animacoes.get('idle_right_list', [pygame.Surface((16, 16))]))
                frame = 0

    # ===== SISTEMA DE ONDAS DE INIMIGOS =====
    tempo_proximo_inimigo += dt

    max_inimigos = 3 + (wave // 2)
    intervalo_spawn = max(500 - (wave * 50), 200)

    if len(inimigos) < max_inimigos and tempo_proximo_inimigo > intervalo_spawn:
        x = random.randint(0, MAPA_LARGURA - 16)
        y = random.randint(0, MAPA_ALTURA - 16)
        
        # Garantir que não spawna muito perto
        while math.sqrt((x - jogador.x)**2 + (y - jogador.y)**2) < 100:
            x = random.randint(0, MAPA_LARGURA - 16)
            y = random.randint(0, MAPA_ALTURA - 16)

        inimigos.append(Inimigo(x, y, jogador, wave))
        tempo_proximo_inimigo = 0

    # ===== ATUALIZAÇÃO DE INIMIGOS =====
    for inimigo in inimigos[:]:
        inimigo.atualizar(paredes, particulas)

        # Colisão com jogador (dano)
        if jogador.rect.colliderect(inimigo.rect) and inimigo.tempo_ataque <= 0:
            jogador.sofrer_dano(inimigo.dano)
            inimigo.tempo_ataque = inimigo.cooldown_ataque

        inimigo.tempo_ataque -= 1

        if not inimigo.vivo():
            inimigos.remove(inimigo)
            jogador.adicionar_score(100 * wave)
            inimigos_derrotados += 1

            # Droppar vida
            if random.random() < 0.2:
                for _ in range(3):
                    vel_x = random.uniform(-2, 2)
                    vel_y = random.uniform(-3, -1)
                    particulas.append(Particula(inimigo.x, inimigo.y, vel_x, vel_y, (0, 255, 0), 4, 30))

    # ===== ATUALIZAÇÃO DE PARTÍCULAS =====
    for particula in particulas[:]:
        particula.atualizar()
        if not particula.vivo():
            particulas.remove(particula)

    # ===== VERIFICAÇÕES DE VITÓRIA/DERROTA =====
    if jogador.vida <= 0:
        running = False

    # Aumentar onda a cada 5 inimigos derrotados
    if inimigos_derrotados > 0 and inimigos_derrotados % 5 == 0 and inimigos_derrotados // 5 != wave:
        wave = inimigos_derrotados // 5 + 1

    # ===== CÂMERA =====
    camera_x = jogador.x + 8 - (LARGURA // ZOOM) // 2
    camera_y = jogador.y + 8 - (ALTURA // ZOOM) // 2

    # ===== RENDERIZAÇÃO =====
    tela_jogo.fill((20, 20, 30))

    # Renderizar mapa
    for layer in MapaOriginal.visible_layers:
        if hasattr(layer, "data"):
            for x, y, gid in layer:
                tile = MapaOriginal.get_tile_image_by_gid(gid)
                if tile:
                    tela_jogo.blit(tile, (x * TILE - camera_x, y * TILE - camera_y))

    # Renderizar partículas
    for particula in particulas:
        particula.desenhar(tela_jogo, camera_x, camera_y)

    # Renderizar inimigos
    for inimigo in inimigos:
        inimigo.desenhar(tela_jogo, camera_x, camera_y)

    # Renderizar jogador
    if len(animacao_atual) > 0:
        tela_jogo.blit(animacao_atual[frame], (jogador.x - camera_x, jogador.y - camera_y))

    # Efeito de ataque visual
    if atacar and frame > 0:
        # Círculo de ataque
        if ultima_direcao == 'right':
            pos_ataque = (jogador.x + 20 - camera_x, jogador.y + 8 - camera_y)
        elif ultima_direcao == 'left':
            pos_ataque = (jogador.x - 20 - camera_x, jogador.y + 8 - camera_y)
        elif ultima_direcao == 'up':
            pos_ataque = (jogador.x + 8 - camera_x, jogador.y - 20 - camera_y)
        else:  # down
            pos_ataque = (jogador.x + 8 - camera_x, jogador.y + 20 - camera_y)

        pygame.draw.circle(tela_jogo, (255, 200, 0, 100), pos_ataque, jogador.alcance_ataque // 2)

    # ===== APLICAR ZOOM =====
    tela_zoom = pygame.transform.scale(tela_jogo, (LARGURA, ALTURA))
    tela.blit(tela_zoom, (0, 0))

    # ===== HUD =====
    # Barra de vida
    vida_ratio = jogador.vida / jogador.vida_max
    barra_largura = 200
    barra_altura = 20
    barra_x = 20
    barra_y = 20

    pygame.draw.rect(tela, (50, 50, 50), (barra_x, barra_y, barra_largura, barra_altura))
    pygame.draw.rect(tela, (0, 255, 0), (barra_x, barra_y, int(barra_largura * vida_ratio), barra_altura))
    pygame.draw.rect(tela, (255, 255, 255), (barra_x, barra_y, barra_largura, barra_altura), 2)

    vida_text = font_pequena.render(f"❤️ {jogador.vida}/{jogador.vida_max}", True, (255, 255, 255))
    tela.blit(vida_text, (barra_x + 10, barra_y + 2))

    # Barra de stamina
    stamina_ratio = jogador.stamina / jogador.stamina_max
    stamina_y = barra_y + barra_altura + 10

    pygame.draw.rect(tela, (50, 50, 50), (barra_x, stamina_y, barra_largura, 10))
    pygame.draw.rect(tela, (0, 150, 255), (barra_x, stamina_y, int(barra_largura * stamina_ratio), 10))
    pygame.draw.rect(tela, (255, 255, 255), (barra_x, stamina_y, barra_largura, 10), 1)

    # Score
    score_text = font_media.render(f"Score: {jogador.score}", True, (255, 215, 0))
    tela.blit(score_text, (LARGURA - 300, 20))

    # Wave
    wave_text = font_media.render(f"Wave: {wave}", True, (255, 100, 0))
    tela.blit(wave_text, (LARGURA - 300, 60))

    # Nível
    nivel_text = font_pequena.render(f"Level: {jogador.nivel} | Inimigos: {len(inimigos)}/{max_inimigos}", True, (100, 255, 100))
    tela.blit(nivel_text, (20, ALTURA - 40))

    # Cooldown de ataque
    if jogador.tempo_ataque > 0:
        cooldown_percent = (jogador.cooldown_ataque - jogador.tempo_ataque) / jogador.cooldown_ataque
        pygame.draw.circle(tela, (255, 100, 0), (LARGURA - 100, ALTURA - 50), 20)
        pygame.draw.arc(tela, (255, 200, 0), (LARGURA - 120, ALTURA - 70, 40, 40), -3.14/2, -3.14/2 + (3.14 * 2 * cooldown_percent), 3)

    # FPS
    fps_text = font_pequena.render(f"FPS: {int(clock.get_fps())}", True, (150, 150, 150))
    tela.blit(fps_text, (LARGURA - 150, ALTURA - 40))

    pygame.display.flip()

# ===== TELA DE GAME OVER =====
tela.fill((0, 0, 0))
game_over_text = font_grande.render("💀 GAME OVER 💀", True, (255, 0, 0))
score_final_text = font_media.render(f"Score Final: {jogador.score}", True, (255, 255, 255))
wave_final_text = font_media.render(f"Wave: {wave}", True, (255, 255, 255))
inimigos_text = font_media.render(f"Inimigos Derrotados: {inimigos_derrotados}", True, (255, 255, 255))
tempo_text = font_pequena.render(f"Tempo: {tempo_jogo // 1000}s", True, (200, 200, 200))
restart_text = font_pequena.render("Pressione qualquer tecla para sair...", True, (150, 150, 150))

tela.blit(game_over_text, (LARGURA // 2 - game_over_text.get_width() // 2, 50))
tela.blit(score_final_text, (LARGURA // 2 - score_final_text.get_width() // 2, 150))
tela.blit(wave_final_text, (LARGURA // 2 - wave_final_text.get_width() // 2, 200))
tela.blit(inimigos_text, (LARGURA // 2 - inimigos_text.get_width() // 2, 250))
tela.blit(tempo_text, (LARGURA // 2 - tempo_text.get_width() // 2, 300))
tela.blit(restart_text, (LARGURA // 2 - restart_text.get_width() // 2, 400))

pygame.display.flip()

# Aguardar input para sair
while True:
    for evento in pygame.event.get():
        if evento.type == QUIT or evento.type == KEYDOWN:
            pygame.quit()
            sys.exit()
