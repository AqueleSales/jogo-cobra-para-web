# ARQUIVO main.py CORRIGIDO E OTIMIZADO PARA PYGBAG
import pygame
import random
import os
import sys
import asyncio
from collections import deque

# --- Constantes e Configurações Iniciais ---
pygame.init()
PRETO = (0, 0, 0)
BRANCO_FUNDO = (20, 20, 20)
VERDE_COBRA = (4, 184, 53)
BRANCO_TEXTO = (240, 240, 240)
AMARELO_AVISO = (255, 221, 0)
CORES_FANTASMAS = [(255, 0, 0), (255, 182, 193), (0, 255, 255), (255, 165, 0), (160, 32, 240)]
COR_FANTASMA_FUGINDO = (60, 60, 255)
COR_FANTASMA_FUGINDO_PISCANDO = (240, 240, 240)
COR_FANTASMA_COMIDO = (200, 200, 200)
TAMANHO_BLOCO = 22
LARGURA_GRADE = 25
ALTURA_GRADE = 25
LARGURA_TELA = LARGURA_GRADE * TAMANHO_BLOCO
ALTURA_TELA = ALTURA_GRADE * TAMANHO_BLOCO
MEIO_X, MEIO_Y = LARGURA_GRADE // 2, ALTURA_GRADE // 2
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('Cobra vs Fantasmas')
relogio = pygame.time.Clock()
DURACAO_MODO_CACADOR = 10000
fonte_placar = pygame.font.Font(None, 36)
fonte_menu = pygame.font.Font(None, 50)
fonte_game_over = pygame.font.Font(None, 50)

# --- Carregando Texturas (Imagens) ---
# (Esta seção é idêntica à sua primeira versão, que estava correta)
texturas_parede = {}
texturas_fantasmas = {}
texturas_cobra = {}
texturas_cobra_cacada = {}
textura_maca = None
textura_fantasma_fugindo = None
textura_fantasma_fugindo_piscando = None
textura_fantasma_comido = None

try:
    caminho_texturas = 'PyTexture2'
    textura_maca_original = pygame.image.load(os.path.join(caminho_texturas, 'maca.png')).convert_alpha()
    textura_maca = pygame.transform.scale(textura_maca_original, (TAMANHO_BLOCO, TAMANHO_BLOCO))
    
    nomes_texturas = ['vertical', 'horizontal', 'canto_se', 'canto_sd', 'canto_ie', 'canto_id', 't_cima', 't_baixo', 't_esquerda', 't_direita', 'fim_cima', 'fim_baixo', 'fim_esquerda', 'fim_direita', 'cruz', 'parede_cheia', 'parede_isolada']
    for nome in nomes_texturas:
        arquivo = f"{nome}.png"
        caminho_completo = os.path.join(caminho_texturas, arquivo)
        img = pygame.image.load(caminho_completo).convert()
        texturas_parede[nome] = pygame.transform.scale(img, (TAMANHO_BLOCO, TAMANHO_BLOCO))
    
    nomes_arquivos_fantasmas = ['fantasma_vermelho.png', 'fantasma_rosa.png', 'fantasma_azul.png', 'fantasma_laranja.png', 'fantasma_roxo.png']
    for i, nome_arquivo in enumerate(nomes_arquivos_fantasmas):
        cor_fantasma = CORES_FANTASMAS[i]
        caminho_completo = os.path.join(caminho_texturas, nome_arquivo)
        img_original = pygame.image.load(caminho_completo).convert_alpha()
        texturas_fantasmas[cor_fantasma] = pygame.transform.scale(img_original, (TAMANHO_BLOCO, TAMANHO_BLOCO))

    textura_fantasma_fraco_original = pygame.image.load(os.path.join(caminho_texturas, 'fantasma_fraco.png')).convert_alpha()
    textura_fantasma_fugindo = pygame.transform.scale(textura_fantasma_fraco_original, (TAMANHO_BLOCO, TAMANHO_BLOCO))
    textura_fantasma_fugindo_piscando = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
    pygame.draw.circle(textura_fantasma_fugindo_piscando, COR_FANTASMA_FUGINDO_PISCANDO, (TAMANHO_BLOCO // 2, TAMANHO_BLOCO // 2), TAMANHO_BLOCO // 2 - 2)
    textura_fantasma_comido = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
    olho_rect = pygame.Rect(TAMANHO_BLOCO // 4 - 1, TAMANHO_BLOCO // 3, 4, 4)
    pygame.draw.rect(textura_fantasma_comido, BRANCO_TEXTO, olho_rect)
    olho_rect.x += TAMANHO_BLOCO // 2
    pygame.draw.rect(textura_fantasma_comido, BRANCO_TEXTO, olho_rect)
    
    def carregar_sprites_cobra(dicionario, sufixo=''):
        cabeca_original = pygame.image.load(os.path.join(caminho_texturas, f'cobra_cabeca{sufixo}.png')).convert_alpha()
        dicionario['cabeca_cima'] = pygame.transform.scale(cabeca_original, (TAMANHO_BLOCO, TAMANHO_BLOCO))
        dicionario['cabeca_baixo'] = pygame.transform.rotate(dicionario['cabeca_cima'], 180)
        dicionario['cabeca_direita'] = pygame.transform.rotate(dicionario['cabeca_cima'], 270)
        dicionario['cabeca_esquerda'] = pygame.transform.rotate(dicionario['cabeca_cima'], 90)
        cauda_original = pygame.image.load(os.path.join(caminho_texturas, f'cobra_cauda{sufixo}.png')).convert_alpha()
        dicionario['cauda_baixo'] = pygame.transform.scale(cauda_original, (TAMANHO_BLOCO, TAMANHO_BLOCO))
        dicionario['cauda_cima'] = pygame.transform.rotate(dicionario['cauda_baixo'], 180)
        dicionario['cauda_direita'] = pygame.transform.rotate(dicionario['cauda_baixo'], 90)
        dicionario['cauda_esquerda'] = pygame.transform.rotate(dicionario['cauda_baixo'], 270)
        nomes_corpo_cobra = ['horizontal', 'vertical', 'ie', 'id', 'se', 'sd']
        for nome in nomes_corpo_cobra:
            arquivo = f'cobra_{nome}{sufixo}.png'
            img_original = pygame.image.load(os.path.join(caminho_texturas, arquivo)).convert_alpha()
            dicionario[nome] = pygame.transform.scale(img_original, (TAMANHO_BLOCO, TAMANHO_BLOCO))
    
    carregar_sprites_cobra(texturas_cobra)
    carregar_sprites_cobra(texturas_cobra_cacada, sufixo='_cacada')

except Exception as e:
    print(f"Erro fatal ao carregar imagens: {e}")

# --- Funções e Classes do Jogo ---
# (Todas as funções e classes do seu primeiro código, que estavam funcionando bem)
def escolher_textura_parede(labirinto, x, y):
    cima = labirinto[y - 1][x] == 1 if y > 0 else True
    baixo = labirinto[y + 1][x] == 1 if y < ALTURA_GRADE - 1 else True
    esq = labirinto[y][x - 1] == 1 if x > 0 else True
    dir = labirinto[y][x + 1] == 1 if x < LARGURA_GRADE - 1 else True
    vizinhos = (cima, baixo, esq, dir)
    num_vizinhos = sum(vizinhos)
    if num_vizinhos == 4: return texturas_parede['parede_cheia']
    if num_vizinhos == 3:
        if not cima: return texturas_parede['t_cima']
        if not baixo: return texturas_parede['t_baixo']
        if not esq: return texturas_parede['t_esquerda']
        if not dir: return texturas_parede['t_direita']
    if num_vizinhos == 2:
        if cima and baixo: return texturas_parede['vertical']
        if esq and dir: return texturas_parede['horizontal']
        if baixo and dir: return texturas_parede['canto_se']
        if baixo and esq: return texturas_parede['canto_sd']
        if cima and dir: return texturas_parede['canto_ie']
        if cima and esq: return texturas_parede['canto_id']
    if num_vizinhos == 1:
        if baixo: return texturas_parede['fim_cima']
        if cima: return texturas_parede['fim_baixo']
        if dir: return texturas_parede['fim_esquerda']
        if esq: return texturas_parede['fim_direita']
    if num_vizinhos == 0: return texturas_parede['cruz']
    return texturas_parede['parede_cheia']

def buscar_caminho_bfs(labirinto, inicio, fim):
    fila = deque([[inicio]])
    visitados = {inicio}
    while fila:
        caminho = fila.popleft()
        x, y = caminho[-1]
        if (x, y) == fim: return caminho
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            prox_x, prox_y = x + dx, y + dy
            if (0 <= prox_x < LARGURA_GRADE and 0 <= prox_y < ALTURA_GRADE and
                    labirinto[prox_y][prox_x] == 0 and (prox_x, prox_y) not in visitados):
                novo_caminho = list(caminho)
                novo_caminho.append((prox_x, prox_y))
                fila.append(novo_caminho)
                visitados.add((prox_x, prox_y))
    return None

def criar_atalhos_no_labirinto(labirinto):
    QUANTIDADE_DE_ATALHOS = 80
    becos_sem_saida = []
    for y in range(2, ALTURA_GRADE - 2):
        for x in range(2, LARGURA_GRADE - 2):
            if labirinto[y][x] == 0:
                vizinhos_parede = sum([labirinto[y - 1][x], labirinto[y + 1][x], labirinto[y][x - 1], labirinto[y][x + 1]])
                if vizinhos_parede == 3: becos_sem_saida.append((x, y))
    random.shuffle(becos_sem_saida)
    for i in range(min(QUANTIDADE_DE_ATALHOS, len(becos_sem_saida))):
        x, y = becos_sem_saida[i]
        paredes_quebraveis = []
        if y > 1 and labirinto[y - 1][x] == 1 and labirinto[y - 2][x] == 0: paredes_quebraveis.append((x, y - 1))
        if y < ALTURA_GRADE - 2 and labirinto[y + 1][x] == 1 and labirinto[y + 2][x] == 0: paredes_quebraveis.append((x, y + 1))
        if x > 1 and labirinto[y][x - 1] == 1 and labirinto[y][x - 2] == 0: paredes_quebraveis.append((x - 1, y))
        if x < LARGURA_GRADE - 2 and labirinto[y][x + 1] == 1 and labirinto[y][x + 2] == 0: paredes_quebraveis.append((x + 1, y))
        if paredes_quebraveis:
            px, py = random.choice(paredes_quebraveis)
            labirinto[py][px] = 0

def gerar_labirinto_hibrido():
    labirinto = [[0 for _ in range(LARGURA_GRADE)] for _ in range(ALTURA_GRADE)]
    for x in range(LARGURA_GRADE):
        labirinto[0][x] = 1
        labirinto[ALTURA_GRADE - 1][x] = 1
    for y in range(ALTURA_GRADE):
        labirinto[y][0] = 1
        labirinto[y][LARGURA_GRADE - 1] = 1
    casa_l, casa_a = 11, 6
    x_inicio_casa, y_inicio_casa = MEIO_X - casa_l // 2, MEIO_Y - casa_a // 2
    for y in range(y_inicio_casa, y_inicio_casa + casa_a):
        for x in range(x_inicio_casa, x_inicio_casa + casa_l):
            labirinto[y][x] = 1
    for y in range(y_inicio_casa + 1, y_inicio_casa + casa_a - 1):
        for x in range(x_inicio_casa + 1, x_inicio_casa + casa_l - 1):
            labirinto[y][x] = 0
    labirinto[y_inicio_casa][MEIO_X] = 0
    for y in range(2, ALTURA_GRADE - 2):
        for x in range(2, LARGURA_GRADE - 2):
            is_in_house = (x_inicio_casa <= x < x_inicio_casa + casa_l and y_inicio_casa <= y < y_inicio_casa + casa_a)
            if not is_in_house:
                labirinto[y][x] = 1
    start_x, start_y = random.randrange(3, LARGURA_GRADE - 3, 2), random.randrange(3, ALTURA_GRADE - 3, 2)
    while (x_inicio_casa <= start_x < x_inicio_casa + casa_l and y_inicio_casa <= start_y < y_inicio_casa + casa_a):
        start_x, start_y = random.randrange(3, LARGURA_GRADE - 3, 2), random.randrange(3, ALTURA_GRADE - 3, 2)
    def cavar(x, y):
        labirinto[y][x] = 0
        direcoes = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(direcoes)
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if 2 < ny < ALTURA_GRADE - 3 and 2 < nx < LARGURA_GRADE - 3 and labirinto[ny][nx] == 1:
                labirinto[y + dy // 2][x + dx // 2] = 0
                cavar(nx, ny)
    cavar(start_x, start_y)
    criar_atalhos_no_labirinto(labirinto)
    labirinto[0][MEIO_X] = 0; labirinto[1][MEIO_X] = 0; labirinto[2][MEIO_X] = 0
    labirinto[ALTURA_GRADE - 1][MEIO_X] = 0; labirinto[ALTURA_GRADE - 2][MEIO_X] = 0; labirinto[ALTURA_GRADE - 3][MEIO_X] = 0
    labirinto[MEIO_Y][0] = 0; labirinto[MEIO_Y][1] = 0; labirinto[MEIO_Y][2] = 0
    labirinto[MEIO_Y][LARGURA_GRADE - 1] = 0; labirinto[MEIO_Y][LARGURA_GRADE - 2] = 0; labirinto[MEIO_Y][LARGURA_GRADE - 3] = 0
    if labirinto[3][MEIO_X] == 1: labirinto[3][MEIO_X] = 0
    if labirinto[ALTURA_GRADE - 4][MEIO_X] == 1: labirinto[ALTURA_GRADE - 4][MEIO_X] = 0
    if labirinto[MEIO_Y][3] == 1: labirinto[MEIO_Y][3] = 0
    if labirinto[MEIO_Y][LARGURA_GRADE - 4] == 1: labirinto[MEIO_Y][LARGURA_GRADE - 4] = 0
    pos_iniciais_fantasmas = []
    locais_spawn_possiveis = []
    for y in range(y_inicio_casa + 1, y_inicio_casa + casa_a - 1):
        for x in range(x_inicio_casa + 1, x_inicio_casa + casa_l - 1):
            locais_spawn_possiveis.append(pygame.math.Vector2(x, y))
    random.shuffle(locais_spawn_possiveis)
    for i in range(min(5, len(locais_spawn_possiveis))):
        pos_iniciais_fantasmas.append(locais_spawn_possiveis[i])
    portais = {(0, MEIO_X): (ALTURA_GRADE - 2, MEIO_X), (ALTURA_GRADE - 1, MEIO_X): (1, MEIO_X),
               (MEIO_Y, 0): (MEIO_Y, LARGURA_GRADE - 2), (MEIO_Y, LARGURA_GRADE - 1): (MEIO_Y, 1)}
    pos_inicial_cobra = pygame.math.Vector2(MEIO_X, ALTURA_GRADE - 2)
    return labirinto, pos_inicial_cobra, portais, pos_iniciais_fantasmas

class Fantasma:
    def __init__(self, pos_inicial, labirinto, cor_cacando):
        self.pos = pos_inicial.copy(); self.labirinto = labirinto; self.base = pos_inicial.copy()
        self.cor_cacando = cor_cacando; self.estado = 'cacando'; self.caminho = []
        self.movimento_ticker = 0; self.recalculo_ticker = 0
    def desenhar(self, tempo_fim_cacador):
        rect = pygame.Rect(self.pos.x * TAMANHO_BLOCO, self.pos.y * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO)
        textura_a_desenhar = None
        if self.estado == 'fugindo':
            tempo_atual = pygame.time.get_ticks()
            if tempo_fim_cacador - tempo_atual < 3000 and (tempo_atual // 250) % 2 == 0:
                textura_a_desenhar = textura_fantasma_fugindo_piscando
            else:
                textura_a_desenhar = textura_fantasma_fugindo
        elif self.estado == 'comido': textura_a_desenhar = textura_fantasma_comido
        else: textura_a_desenhar = texturas_fantasmas.get(self.cor_cacando)
        if textura_a_desenhar: tela.blit(textura_a_desenhar, rect.topleft)
    def obter_movimento_aleatorio_valido(self):
        movimentos_validos = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            prox_x, prox_y = self.pos.x + dx, self.pos.y + dy
            if (0 <= prox_x < LARGURA_GRADE and 0 <= prox_y < ALTURA_GRADE and self.labirinto[int(prox_y)][int(prox_x)] == 0):
                movimentos_validos.append(pygame.math.Vector2(prox_x, prox_y))
        return random.choice(movimentos_validos) if movimentos_validos else self.pos
    def mover(self, cobra, dificuldade, outros_fantasmas):
        velocidade_fantasma = 1 + dificuldade
        self.movimento_ticker += 1
        if self.movimento_ticker < (10 - velocidade_fantasma): return
        self.movimento_ticker = 0
        pos_alvo_final = None
        if self.estado == 'cacando':
            if dificuldade == 1:
                if random.random() < 0.8: self.pos = self.obter_movimento_aleatorio_valido(); return
                else: pos_alvo_final = cobra.corpo[0]
            elif dificuldade == 2:
                if random.random() < 0.25: self.pos = self.obter_movimento_aleatorio_valido(); return
                else: pos_alvo_final = cobra.corpo[0]
            elif dificuldade == 3: pos_alvo_final = cobra.corpo[0] + cobra.direcao * 4
        elif self.estado == 'fugindo':
            pos_alvo_final = random.choice([(1, 1), (LARGURA_GRADE - 2, 1), (1, ALTURA_GRADE - 2), (LARGURA_GRADE - 2, ALTURA_GRADE - 2)])
        elif self.estado == 'comido':
            pos_alvo_final = self.base
            if self.pos == self.base: self.estado = 'cacando'
        if pos_alvo_final:
            self.recalculo_ticker += 1
            if not self.caminho or self.recalculo_ticker > 15:
                pos_alvo_tupla = (int(pos_alvo_final.x), int(pos_alvo_final.y)) if isinstance(pos_alvo_final, pygame.math.Vector2) else pos_alvo_final
                self.caminho = buscar_caminho_bfs(self.labirinto, (int(self.pos.x), int(self.pos.y)), pos_alvo_tupla)
                self.recalculo_ticker = 0
            if self.caminho and len(self.caminho) > 1:
                prox_passo_pos = pygame.math.Vector2(self.caminho[1][0], self.caminho[1][1])
                if prox_passo_pos in [f.pos for f in outros_fantasmas if f is not self]: return
                self.pos = prox_passo_pos
                self.caminho.pop(0)
            else: self.caminho = []

class Cobra:
    def __init__(self, labirinto, pos_inicial, portais):
        self.labirinto = labirinto; self.corpo = [pos_inicial.copy()]; self.portais = portais
        self.direcao = pygame.math.Vector2(0, 0); self.crescer = False
        self.buffer_direcao = deque(); self.movimento_ticker = 0
    def mover(self):
        self.movimento_ticker += 1
        if self.movimento_ticker < 2: return
        self.movimento_ticker = 0
        if self.direcao.length() == 0: return
        if self.buffer_direcao:
            proxima_direcao = self.buffer_direcao.popleft()
            if proxima_direcao * -1 != self.direcao: self.direcao = proxima_direcao
        proxima_cabeca = self.corpo[0] + self.direcao
        pos_tupla = (int(proxima_cabeca.y), int(proxima_cabeca.x))
        if pos_tupla in self.portais: proxima_cabeca.y, proxima_cabeca.x = self.portais[pos_tupla]
        # Adiciona uma verificação para garantir que a posição é válida no labirinto
        if not (0 <= int(proxima_cabeca.y) < ALTURA_GRADE and 0 <= int(proxima_cabeca.x) < LARGURA_GRADE):
            return # Sai da função se estiver fora dos limites
        if self.labirinto[int(proxima_cabeca.y)][int(proxima_cabeca.x)] == 1:
            self.buffer_direcao.clear(); return
        corpo_copia = self.corpo[:-1]
        if self.crescer:
            corpo_copia = self.corpo[:]; self.crescer = False
        self.corpo = [proxima_cabeca] + corpo_copia
    def mudar_direcao(self, nova_direcao):
        if len(self.buffer_direcao) < 2: self.buffer_direcao.append(nova_direcao)
    def desenhar(self, modo_cacador):
        sprites = texturas_cobra_cacada if modo_cacador else texturas_cobra
        if not self.corpo: return # Checagem de segurança
        cabeca = self.corpo[0]
        rect_cabeca = pygame.Rect(cabeca.x * TAMANHO_BLOCO, cabeca.y * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO)
        if self.direcao.y == -1: tela.blit(sprites['cabeca_cima'], rect_cabeca)
        elif self.direcao.y == 1: tela.blit(sprites['cabeca_baixo'], rect_cabeca)
        elif self.direcao.x == -1: tela.blit(sprites['cabeca_esquerda'], rect_cabeca)
        elif self.direcao.x == 1: tela.blit(sprites['cabeca_direita'], rect_cabeca)
        else: tela.blit(sprites['cabeca_cima'], rect_cabeca)
        for i, segmento in enumerate(self.corpo):
            if i == 0: continue
            rect = pygame.Rect(segmento.x * TAMANHO_BLOCO, segmento.y * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO)
            anterior = self.corpo[i - 1]
            if i == len(self.corpo) - 1:
                vetor_cauda = anterior - segmento
                if vetor_cauda.y == -1: tela.blit(sprites['cauda_cima'], rect)
                elif vetor_cauda.y == 1: tela.blit(sprites['cauda_baixo'], rect)
                elif vetor_cauda.x == -1: tela.blit(sprites['cauda_esquerda'], rect)
                elif vetor_cauda.x == 1: tela.blit(sprites['cauda_direita'], rect)
            else:
                proximo = self.corpo[i + 1]
                vetor_anterior = anterior - segmento
                vetor_proximo = proximo - segmento
                if vetor_anterior.x == vetor_proximo.x: tela.blit(sprites['vertical'], rect)
                elif vetor_anterior.y == vetor_proximo.y: tela.blit(sprites['horizontal'], rect)
                else:
                    if (vetor_anterior.y == -1 and vetor_proximo.x == 1) or (vetor_anterior.x == 1 and vetor_proximo.y == -1): tela.blit(sprites['se'], rect)
                    elif (vetor_anterior.y == -1 and vetor_proximo.x == -1) or (vetor_anterior.x == -1 and vetor_proximo.y == -1): tela.blit(sprites['sd'], rect)
                    elif (vetor_anterior.y == 1 and vetor_proximo.x == 1) or (vetor_anterior.x == 1 and vetor_proximo.y == 1): tela.blit(sprites['ie'], rect)
                    elif (vetor_anterior.y == 1 and vetor_proximo.x == -1) or (vetor_anterior.x == -1 and vetor_proximo.y == 1): tela.blit(sprites['id'], rect)
    def solicitar_crescimento(self): self.crescer = True
    def checar_colisao_fatal(self): return self.corpo[0] in self.corpo[1:]

class Comida:
    def __init__(self, labirinto, corpo_cobra):
        self.labirinto = labirinto
        self.reposicionar(corpo_cobra)
    def desenhar(self):
        if textura_maca: tela.blit(textura_maca, (self.pos.x * TAMANHO_BLOCO, self.pos.y * TAMANHO_BLOCO))
    def reposicionar(self, corpo_cobra):
        locais_possiveis = []
        for y in range(ALTURA_GRADE):
            for x in range(LARGURA_GRADE):
                if self.labirinto[y][x] == 0:
                    pos = pygame.math.Vector2(x, y)
                    if pos not in corpo_cobra: locais_possiveis.append(pos)
        if locais_possiveis: self.pos = random.choice(locais_possiveis)
        else: self.pos = pygame.math.Vector2(1, 1)

def desenhar_elementos(labirinto, cobra, comida, fantasmas, pontuacao, dificuldade, macas_para_cacar, modo_cacador, mostrar_ui, tempo_fim_cacador):
    for y, linha in enumerate(labirinto):
        for x, celula in enumerate(linha):
            if celula == 1:
                tela.blit(escolher_textura_parede(labirinto, x, y), (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO))
    cobra.desenhar(modo_cacador)
    comida.desenhar()
    for fantasma in fantasmas:
        fantasma.desenhar(tempo_fim_cacador)
    if mostrar_ui:
        altura_barra_ui = 40
        barra_ui = pygame.Surface((LARGURA_TELA, altura_barra_ui), pygame.SRCALPHA)
        barra_ui.fill((20, 20, 20, 200))
        tela.blit(barra_ui, (0, 0))
        texto_placar = fonte_placar.render(f"Pontos: {pontuacao}", True, BRANCO_TEXTO)
        tela.blit(texto_placar, (20, 5))
        if modo_cacador: texto_cacada = fonte_placar.render("MODO CAÇADA!", True, AMARELO_AVISO)
        else: texto_cacada = fonte_placar.render(f"Caçada em: {macas_para_cacar} maçãs", True, BRANCO_TEXTO)
        rect_cacada = texto_cacada.get_rect(center=(LARGURA_TELA / 2, altura_barra_ui / 2))
        tela.blit(texto_cacada, rect_cacada)
        texto_dificuldade = fonte_placar.render(f"Dificuldade: {dificuldade}", True, BRANCO_TEXTO)
        rect_dificuldade = texto_dificuldade.get_rect(right=LARGURA_TELA - 20, centery=altura_barra_ui / 2)
        tela.blit(texto_dificuldade, rect_dificuldade)

def desenhar_menu_pausa():
    filtro = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    filtro.fill((0, 0, 0, 170))
    tela.blit(filtro, (0, 0))
    largura_botao, altura_botao = 200, 50
    btn_voltar = pygame.Rect(LARGURA_TELA / 2 - largura_botao / 2, ALTURA_TELA / 2 - 80, largura_botao, altura_botao)
    btn_reiniciar = pygame.Rect(LARGURA_TELA / 2 - largura_botao / 2, ALTURA_TELA / 2, largura_botao, altura_botao)
    btn_sair = pygame.Rect(LARGURA_TELA / 2 - largura_botao / 2, ALTURA_TELA / 2 + 80, largura_botao, altura_botao)
    botoes = {'voltar': btn_voltar, 'reiniciar': btn_reiniciar, 'sair': btn_sair}
    for nome, rect in botoes.items():
        pygame.draw.rect(tela, (60, 60, 60), rect, border_radius=10)
        texto_surf = fonte_menu.render(nome.capitalize(), True, BRANCO_TEXTO)
        texto_rect = texto_surf.get_rect(center=rect.center)
        tela.blit(texto_surf, texto_rect)
    return botoes

# --- NOVO: Função para desenhar a tela de Game Over ---
def desenhar_tela_game_over(pontuacao):
    filtro = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    filtro.fill((0, 0, 0, 180))
    tela.blit(filtro, (0,0))
    
    texto_go = fonte_game_over.render("GAME OVER", True, BRANCO_TEXTO)
    rect_go = texto_go.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 - 60))
    tela.blit(texto_go, rect_go)
    
    texto_pontos = fonte_placar.render(f"Pontuação final: {pontuacao}", True, BRANCO_TEXTO)
    rect_pontos = texto_pontos.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2))
    tela.blit(texto_pontos, rect_pontos)

    texto_restart = fonte_placar.render("Aperte ESPAÇO para reiniciar", True, AMARELO_AVISO)
    rect_restart = texto_restart.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 + 60))
    tela.blit(texto_restart, rect_restart)

# --- NOVO: Função que agrupa todas as variáveis do jogo para reiniciar facilmente ---
def setup_jogo():
    """Inicializa e retorna todas as variáveis e objetos para um novo jogo."""
    labirinto, pos_cobra, portais, pos_fantasmas = gerar_labirinto_hibrido()
    
    game_vars = {
        "labirinto_atual": labirinto,
        "cobra": Cobra(labirinto, pos_cobra, portais),
        "comida": Comida(labirinto, [pos_cobra]),
        "fantasmas": [Fantasma(pos, labirinto, CORES_FANTASMAS[i % len(CORES_FANTASMAS)]) for i, pos in enumerate(pos_fantasmas)],
        "pontuacao": 0,
        "dificuldade_fantasma": 1,
        "modo_cacador": False,
        "tempo_fim_cacador": 0,
        "jogo_pausado": False,
        "mostrar_ui": False,
    }
    return game_vars

async def main():
    # --- NOVO: Sistema de Estados do Jogo ---
    game_state = "JOGANDO"
    game_vars = setup_jogo()
    rodando = True
    
    while rodando:
        # --- LÓGICA DO ESTADO "JOGANDO" ---
        if game_state == "JOGANDO":
            # Extrai as variáveis do dicionário para facilitar o uso
            cobra = game_vars["cobra"]
            fantasmas = game_vars["fantasmas"]
            comida = game_vars["comida"]
            
            game_vars['mostrar_ui'] = pygame.key.get_pressed()[pygame.K_TAB]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_vars["jogo_pausado"] = not game_vars["jogo_pausado"]
                    
                    if not game_vars["jogo_pausado"]:
                        if event.key == pygame.K_1: game_vars["dificuldade_fantasma"] = 1
                        if event.key == pygame.K_2: game_vars["dificuldade_fantasma"] = 2
                        if event.key == pygame.K_3: game_vars["dificuldade_fantasma"] = 3
                        nova_direcao = None
                        if event.key in (pygame.K_UP, pygame.K_w): nova_direcao = pygame.math.Vector2(0, -1)
                        if event.key in (pygame.K_DOWN, pygame.K_s): nova_direcao = pygame.math.Vector2(0, 1)
                        if event.key in (pygame.K_LEFT, pygame.K_a): nova_direcao = pygame.math.Vector2(-1, 0)
                        if event.key in (pygame.K_RIGHT, pygame.K_d): nova_direcao = pygame.math.Vector2(1, 0)
                        if nova_direcao:
                            if cobra.direcao.length() == 0: cobra.direcao = nova_direcao
                            else: cobra.mudar_direcao(nova_direcao)

                if event.type == pygame.MOUSEBUTTONDOWN and game_vars["jogo_pausado"]:
                    botoes = desenhar_menu_pausa()
                    if botoes['voltar'].collidepoint(event.pos): game_vars["jogo_pausado"] = False
                    if botoes['reiniciar'].collidepoint(event.pos):
                        game_vars = setup_jogo() # Reinicia o jogo
                    if botoes['sair'].collidepoint(event.pos):
                        rodando = False
            
            if not game_vars["jogo_pausado"]:
                cobra.mover()
                for fantasma in fantasmas:
                    fantasma.mover(cobra, game_vars["dificuldade_fantasma"], fantasmas)
                
                if game_vars["modo_cacador"] and pygame.time.get_ticks() > game_vars["tempo_fim_cacador"]:
                    game_vars["modo_cacador"] = False
                    for fantasma in fantasmas:
                        if fantasma.estado != 'comido': fantasma.estado = 'cacando'
                
                # Checagem de Colisões e Morte
                morreu = False
                if cobra.checar_colisao_fatal():
                    morreu = True
                
                for fantasma in fantasmas:
                    if fantasma.pos == cobra.corpo[0]:
                        if game_vars["modo_cacador"] and fantasma.estado == 'fugindo':
                            fantasma.estado = 'comido'
                            game_vars["pontuacao"] += 50
                        elif fantasma.estado == 'cacando':
                            morreu = True
                
                if morreu:
                    game_state = "GAME_OVER" # --- MUDA O ESTADO PARA GAME OVER
                
                # Lógica de comer a maçã
                if not morreu and cobra.corpo[0] == comida.pos:
                    cobra.solicitar_crescimento()
                    game_vars["pontuacao"] += 10
                    comida.reposicionar(cobra.corpo)
                    
                    macas_comidas = len(cobra.corpo) - 1
                    if macas_comidas >= 10 and not game_vars["modo_cacador"]:
                        game_vars["modo_cacador"] = True
                        game_vars["tempo_fim_cacador"] = pygame.time.get_ticks() + DURACAO_MODO_CACADOR
                        for fantasma in fantasmas:
                            if fantasma.estado != 'comido':
                                fantasma.estado = 'fugindo'
                                fantasma.caminho = []
            
            # Desenha a tela do jogo
            tela.fill(BRANCO_FUNDO)
            macas_para_cacar = max(0, 10 - (len(cobra.corpo)-1))
            desenhar_elementos(game_vars["labirinto_atual"], cobra, comida, fantasmas, game_vars["pontuacao"], game_vars["dificuldade_fantasma"], macas_para_cacar, game_vars["modo_cacador"], game_vars["mostrar_ui"], game_vars["tempo_fim_cacador"])
            if game_vars["jogo_pausado"]:
                desenhar_menu_pausa()

        # --- LÓGICA DO ESTADO "GAME_OVER" ---
        elif game_state == "GAME_OVER":
            desenhar_tela_game_over(game_vars["pontuacao"])
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_vars = setup_jogo() # Reinicia o jogo
                        game_state = "JOGANDO"  # Volta para o estado de jogo
                    if event.key == pygame.K_ESCAPE:
                        rodando = False

        pygame.display.update()
        await asyncio.sleep(1/30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())