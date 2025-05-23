#IMPORTAÇÕES:
import pygame
import funcional
from random import randint, choice

#INICIALIZAR PYGAME:
pygame.init()

#CRIA DICIONARIOS QUE ACESSAM OS SPRITES:
#Imagens durante o dia:
imagens_dia = {
    'cenario': [pygame.image.load('Sprites (dia)/Cenario/Estrada 1.png'), pygame.image.load('Sprites (dia)/Cenario/Nuvem.png')],
    'Dinos': [pygame.image.load(f'Sprites (dia)/Dinos/Dino {num}.png') for num in range(1, 9)],
    'Obstaculo': [pygame.image.load(f'Sprites (dia)/Obstaculos/Cacto {num}.png') for num in range(1, 8)] + [pygame.image.load(f'Sprites (dia)/Obstaculos/Passaro {num}.png') for num in range(1, 3)],
    'restart': [pygame.image.load('Sprites (dia)/Outros/Voltar.png'), pygame.image.load('Sprites (dia)/Outros/game over.png')],
}
#Redimenciona as imagens do dia:
funcional.mudarEscala(imagens_dia, 'dict', (10, 10))
funcional.mudarEscala(imagens_dia['Dinos'], 'list', (2, 2), True)
for passaro in imagens_dia['Obstaculo'][7:9]:
    tamanho = (passaro.get_width() * 2, passaro.get_height() * 2)
    imagens_dia['Obstaculo'][imagens_dia['Obstaculo'].index(passaro)] = pygame.transform.scale(passaro, (tamanho))

#Imagens durante a noite:
imagens_noite = {
    'cenario': [pygame.image.load('Sprites (noite)/Cenario (noite)/Estrada 1.png'), pygame.image.load('Sprites (noite)/Cenario (noite)/Nuvem.png')],
    'Dinos': [pygame.image.load(f'Sprites (noite)/Dinos (noite)/Dino {num}.png') for num in range(1, 8)],
    'Obstaculo': [pygame.image.load(f'Sprites (noite)/Obstaculos (noite)/Cacto {num}.png') for num in range(1, 8)] + [pygame.image.load(f'Sprites (noite)/Obstaculos (noite)/Passaro {num}.png') for num in range(1, 3)],
    'restart': [pygame.image.load('Sprites (noite)/Outros (noite)/Voltar.png'), pygame.image.load('Sprites (noite)/Outros (noite)/game over.png')],
}
#Redimenciona as imagens da noite:
funcional.mudarEscala(imagens_noite, 'dict', (10, 10))
funcional.mudarEscala(imagens_noite['Dinos'], 'list', (2, 2), True)
for passaro in imagens_noite['Obstaculo'][7:9]:
    tamanho = (passaro.get_width() * 2, passaro.get_height() * 2)
    imagens_noite['Obstaculo'][imagens_noite['Obstaculo'].index(passaro)] = pygame.transform.scale(passaro, (tamanho))

#CRIA UM DICIONARIO QUE AJUDA NO CONTROLE DE FLUXO DO SOM:
fluxo_de_som = {
    'pulo': True,
    'batida': True,
    'pontuação': True
}

#JANELA:
dimensão = (1000, 500)
#Cria a janela:
janela = pygame.display.set_mode(dimensão)
#Titulo da janela:
pygame.display.set_caption('Dino Brawser Game')
#Icone da janela:
pygame.display.set_icon(imagens_dia['Dinos'][0])

#CRIA A ALTURA DA BASE SOB A QUAL O DINO E OS CACTOS FICARAM:
base_elementos = (dimensão[1] * 60 / 100) + 12

#CONTADOR DE ITERAÇÕES ENTRE OS OBSTACULOS, PARA CALCULAR O INTERVALO ENTRE CADA UM OBSTACULO   :
iterações_entre_obstaculos = 0

#DEFINI A VARIAVEL DO LOOP QUE FAZ O JOGO FUNCIONAR:
continuar = True

#LOOP DO JOGO:
while True:
    #DEFINE O LIMITE DE ITERAÇÕES DO LOOP POR SEGUNDO:
    limite = 60     #<-- Cada 60 iterações equivale a um 1 segundo (60 = 1)
    #Chama objeto Clock() para definir o limite de iteraçõies:
    limitador = pygame.time.Clock()

    #DEFINE OS SPRITES QUE SERÃO USADOS INICIALMENTE:
    lista_imagens = imagens_dia

    #ORGANIZA O CICLO ENTRE NOITE DIA PARA UM NÃO HAVER INTERFERENCIA ENTRE NOITE E DIA:
    ciclo_circadiano = True

    #AO A PONTUAÇÃO CHEGAR EM 700 PONTOS, O NUMERO DE VERIFICAÇÕES SERÁ LIMITADO:
    pontuação_chave = True      #Faz com que o ciclo circadiano só altere uma vez, quando a pontuação chegar a um número divisivel por 700

    #ARMAZENA AS INFORMAÇÕES DA ÁREA DE FUNDO NO QUAL O JOGO FICA (layout):
    info_layout = {
        'posicao': [0, (dimensão[1] * 20 / 100), dimensão[0], (dimensão[1] * 60 / 100)],
        'cor': (255, 255, 255)
        }

    #DEFINE A COR DA JANELA:
    cor_janela = (225, 225, 225)

    #CRIA UM DICIONÁRIO COM TODOS OS ELEMENTOS PRESENTES NO JOGO:
    lista_de_elementos = {
        'estrada': (funcional.elementos(janela, lista_imagens['cenario'][0], [dimensão[0] - lista_imagens['cenario'][0].get_width(), base_elementos - 12]),
                    funcional.elementos(janela, lista_imagens['cenario'][0], [dimensão[0], base_elementos - 12])),
        'obstaculos': set(),
        'passaro': set(),
        'Nuvens': set(),
        'Restart': (funcional.elementos(janela, lista_imagens['restart'][0], [(dimensão[0] / 2) - (lista_imagens['restart'][0].get_width() / 2), (dimensão[1] / 2) - (lista_imagens['restart'][0].get_height() / 2)]),
                    funcional.elementos(janela, lista_imagens['restart'][1], [(dimensão[0] / 2) - (lista_imagens['restart'][1].get_width() / 2), (dimensão[1] / 2) - (lista_imagens['restart'][1].get_height() + 50)]))
            }

    #DEFINI AS MEDIDAS DE TODOS OS ELEMENTOS:
    for indice, lista in lista_de_elementos.items():
        for item in lista:
            item.definirMedidas()

    #DEFINI O AUMENTO DO DESLOCAMENTO POR ITERAÇÃO E O DESLOCAMENTO:
    #Aumento de deslocamento:
    aumento_de_deslocamento = -250
    #Deslocamento:
    deslocamento_de_elementos = aumento_de_deslocamento // limite

    #INFORMAÇÕES E DEFINIÇÕES DOS PONTOS E RECORDES:
    #Fonte utilizada:
    fonte = pygame.font.SysFont('press start 2p regular', 15, False, False)
    #Variavel da pontuação atual:
    pontos = 0
    #Acessa o recorde de pontos:
    record = open('Record', 'r')
    #Dicionários com pontos e record:
    textos = {
        'pontuação': funcional.elementos(janela, fonte.render(f'{pontos:0>5}', False, (100, 100, 100))),
        'record': funcional.elementos(janela, fonte.render(f'HI {record.read()}', False, (100, 100, 100)))
    }
    #Defini a posição dos textos da PONTUAÇÃO e do RECORD:
    textos['pontuação'].posicao = (dimensão[0] - (textos['pontuação'].imagem.get_width() + 5), (info_layout['posicao'][1]) + 5)
    textos['record'].posicao = (textos['pontuação'].posicao[0] - (textos['record'].imagem.get_width() + 20), (info_layout['posicao'][1] + 5))
    #Defini as medidas dos textos da PONTUAÇÃO e do RECORD:
    textos['pontuação'].definirMedidas()
    textos['record'].definirMedidas()
    #Fecha o arquivos do RECORD:
    record.close()

    #DEFINI A VARIAVEL DE TEMPO DA ANIMAÇÃO DOS PONTOS DIVISIVEIS POR 100:
    tempo_animação_pontos = 0

    #AUMENTO DO TEMPO DE INTERVALO ENTRE OBSTACULOS:
    aumento_intervalo = 0

    #CRIA O ELEMENTO DINO (JOGADOR):
    #Defini o TAMANHO e POSIÇÃO do dino:
    tamanho_do_dino = lista_imagens['Dinos'][0].get_rect(topleft=(100, base_elementos - lista_imagens['Dinos'][0].get_height()))
    #Defini o Elemento dino:
    Jogador = funcional.elementos(janela, lista_imagens['Dinos'][0], pygame.Rect(tamanho_do_dino), [0, -10], lista_imagens['Dinos'][2:4])

    #DEFINI A VARIAVEL QUE VERIFICA SE O DINO ESTÁ ABAIXADO OU NÃO:
    abaixar = False

    #CONTADORES PARA DEFINIR A ANIMAÇÃO DO DINO E PASSAROS:
    #Contador da animação do dino:
    animações_do_dino = 1
    #Contador da animação dos passaros:
    animação_passaros = 1

    #DEFINI INFORMAÇÕES DE PULO, COMO: (REDUÇÃO DE VELOCIDADE DO PULO, SE DEVE CONTINUAR PULANDO E BASE)
    #Defini se o dino deve continuar pulando:
    pular = False
    #Defini a base sob a qual o dino ficara:
    base = pygame.Rect(0, Jogador.posicao[1] + Jogador.posicao[-1], dimensão[0], 1)
    #Defini a redução de velocidade do pulo (gravidade):
    redução_do_pulo = 0.6

    #DEFINI O INTERVALO ENTRE A APARIÇÃO DE NOVOS OBSTACULOS E CONTA O NÚMERO DE ITERAÇÕES DO LOOP:
    #intervalo
    intervalo = 1
    contar_iterações = 0

    #DEFINI A COR DA JANELA:
    janela.fill((255, 255, 255))
    
    #MOSTRA O DINO NA TELA:
    Jogador.imagem = imagens_dia['Dinos'][7]
    Jogador.mostrarElemento()

    #ATUALIZA A JANELA:
    pygame.display.update()

    #DEFINI A VARIAVEL CONTINUAR E VARIAVEL CHAVE_COLISÃO:
    #Caso continuar seja True, chave_colisão será False:
    if continuar:
        chave_colisão = False
    #Caso continuar seja False, chave_colisão será True:
    else:
        chave_colisão = True
    #Defini continuar como True:
    continuar = True
    
    #LOOP DE EXECUÇÃO DO JOGO:
    while continuar:
        #Itera todos os obstaculos:
        for obstaculos in list(lista_de_elementos['obstaculos']) + list(lista_de_elementos['passaro']):
            colisão = funcional.colisão(obstaculos, Jogador)

            #COLISÃO:
            #Verifica se houve colisão:
            if colisão:
                chave_colisão = False
                #Toca o som de batida (game over):
                if fluxo_de_som['batida']:
                    pygame.mixer.music.load('Sons/Bater.mp3')
                    pygame.mixer.music.play(0, 0.80)
                    fluxo_de_som['batida'] = False
                
                #Mostra todos os elementos presentes na tela:
                for lista_elemento in lista_de_elementos.values():
                    for elemento in lista_elemento:
                        elemento.mostrarElemento()

                #Define o Sprite do Dino, como sprite de morte:
                Jogador.imagem = lista_imagens['Dinos'][6]

                #Exisbe o record atualizado de pontos:
                textos['record'].mostrarElemento()
                #Exibe a pontuação feita:
                textos['pontuação'].mostrarElemento()

                #Mostra o dino na tela (com o sprite de morte):
                Jogador.mostrarElemento()

                #Exibe a mensagem de "GAME OVER" e o botão de voltar:
                #Game over:
                lista_de_elementos['Restart'][0].mostrarElemento()
                #Voltar:
                lista_de_elementos['Restart'][1].mostrarElemento() 

                #Atualiza a superficie da janela::
                pygame.display.update()

        #VERIFICA EVENTOS NO JOGO:
        for eventos in pygame.event.get():
            #Sai do jogo ao X ser precionado:
            if eventos.type == pygame.QUIT:
                exit()

            #Verifica se o teclado foi PRCIONADO:
            if eventos.type == pygame.KEYDOWN:
                #Verfica se ESPAÇO ou botão CIMA foi precionado:
                if eventos.key == pygame.K_SPACE or eventos.key == pygame.K_UP:
                    #Caso tenha tido colisão, o jogo irá reiniciar:
                    if not chave_colisão:
                        continuar = False
                        fluxo_de_som['batida'] = True
                    #Caso não tenho tido colisão, o dino vai pular e o jogo proceguira:
                    else:
                        if not pular:
                            Jogador.desloc[1] = -11
                            pular = True
                            parar = False
                            redução_do_pulo = 0.6
                #Caso o botão BAIXO tenha sido precionado, o dino ira abaixar:
                if eventos.key == pygame.K_DOWN:
                    #Variavel que controla se o dino abaixou ou não:
                    abaixar = True

            #Verifica se o teclado foi solto:
            if eventos.type == pygame.KEYUP:
                #Verifica se ESPAÇO ou botão CIMA foi solto:
                if eventos.key == pygame.K_SPACE or eventos.key == pygame.K_UP:
                    #Verifica se houve colisão:
                    if chave_colisão:
                        #Caso espaço ou botão cima tenha sido solto, a altura do pulo será limitada:
                        redução_do_pulo = 0.90
                        parar = True
                #Caso o botão BAIXO tenha sido solto, o dino irá abaixar:
                if eventos.key == pygame.K_DOWN:
                    #Variavel que controla se o dino abaixou ou não:
                    abaixar = False

            #Verifica se NÃO houve colisão:
            if not chave_colisão:
                #Verifica se algum botão do mouse foi precionado:
                if eventos.type == pygame.MOUSEBUTTONDOWN:
                    #Defini a posição do mouse:
                    mouse_posicao = pygame.Rect(eventos.pos[0], eventos.pos[1], 1, 1)
                    #Verifica se o botão esquerdo foi precionado:
                    if eventos.button == 1:
                        #Caso botão esquerdo tenha sido precionado, o jogo irá reiniciar:
                        if lista_de_elementos['Restart'][0].posicao.colliderect(mouse_posicao):
                            continuar = False
                            fluxo_de_som['batida'] = True

        #CONTA DE TODOS OS CONTADORES:
        contar_iterações += 1
        animação_passaros += 1
        animações_do_dino += (10 - deslocamento_de_elementos / 4) / limite
        aumento_de_deslocamento -= 0.05
        deslocamento_de_elementos = aumento_de_deslocamento // limite

        #PREENCHE A SUPERFICIE DA JANELA:
        janela.fill(cor_janela)

        #MOSTRAR TELA FORMATADA DE FUNDO:
        pygame.draw.rect(janela, info_layout['cor'], info_layout['posicao'], 0)
        
        #CASO NÃO TENHA TIDO COLISÃO OU JOGO TENHA SIDO REINICIADO, O JOGO IRA RODAR:
        if chave_colisão: 

            #CASO O BOTÃO DE ABAIXAR TENHA SIDO PRECIONADO O DINO IRÁ ABAIXAR:
            if abaixar:
                Jogador.desloc[1] = 15
                #Caso a posição do dino seja igual a posição normal dele, ele irá parar de "pular":
                if Jogador.posicao[1] == base_elementos - Jogador.posicao[-1]:
                    pular = False

            #CASO O BOTÃO DE PULAR TENHA SIDO PRECIONADO O DINO IRÁ PULAR:
            if pular:
                #Toca o som de pulo:
                if fluxo_de_som['pulo']:
                    pygame.mixer.music.load('Sons/Pular.mp3')
                    pygame.mixer.music.play(0, 1.0)
                    fluxo_de_som['pulo'] = False
                #Caso dino tenha encostado no chão, ele para:
                if Jogador.posicao.colliderect(base):
                    #Altera o fluxo de som:
                    fluxo_de_som['pulo'] = True
                    #Caso o botão de pular tenha sido solto o pulo irá parar:
                    if parar:
                        pular = False
                    #Caso o botão de pulo não tenha sido solto o pulo procequira, até que ele seja solto:
                    else:
                        pular = True
                        Jogador.desloc[1] = -11
                        redução_do_pulo = 0.6
                    #Define a posição em Y da base do dino:
                    Jogador.posicao[1] = base_elementos - Jogador.posicao[-1]
                    continue
                    
                #Move o dino (PULO):
                Jogador.mover_Y()
                Jogador.desloc[1] += redução_do_pulo

            #MOVE E ADICIONA CENÁRIOS E OBSTACULOS:
            #Itera o dicionario de elementos e separa em INDICE e VALOR:
            for categorias, lista in lista_de_elementos.items():
                #Caso a categoria do elemento iterado seja "Restart":
                if categorias == 'Restart':
                    continue
                #Itera todos os elementos por categoria (Cenario, Obstaculo e Nuvens):
                for elemento in list(lista):

                    #Verifica se o elemento passou do limite:
                    if elemento.posicao[0] <= (-elemento.imagem.get_width()):
                        #Verifica se especificamente um OBSTACULO, PASSARO ou NUVEM chegou ao limite e o remove do conjunto:
                        if categorias == 'obstaculos' or categorias == 'Nuvens' or categorias == 'passaro':
                            lista_de_elementos[categorias].remove(elemento)
                        #Verifica se especificamente uma das estradas chegou ao limite e o move para o final da outra estrada:
                        if categorias == 'estrada':
                            elemento.posicao[0] = elemento.imagem.get_width()
                        #Caso qualquer outro elemento tenha chegado ao limite sua posição mudara para o inicio.
                        else:
                            elemento.posicao[0] = dimensão[0]
                    
                    #ADICIONA OBSTACULOS E NUVENS A SEUS CONJUNTOS:
                    #Verifica se o numero de iterações é igual ao tempo do intervalo entre os obstaculos:
                    if contar_iterações >= intervalo:
                        intervalo = ((funcional.timeAleatorio(50, 90, 100) * limite) * 4) / (deslocamento_de_elementos * -1) + aumento_intervalo  #<--Defini um novo intervalo
                        #Reinicia a contagem de iterações
                        contar_iterações = 0
                        #Verifica se a pontuação chegou a 400 pontos:
                        if int(pontos) >= 200:
                            #Define um obstaculo aleatório entre todos os obstaculos
                            obstaculo_aleatório = choice(lista_imagens['Obstaculo'])
                        else:
                            #Define um obstaculos aleatório entre os cactos:
                            obstaculo_aleatório = choice(lista_imagens['Obstaculo'][:7])
                        #Define a posição do obstaculo:
                        posicao_obstaculo = lista_imagens['Obstaculo'][0].get_rect(topleft=(dimensão[0], base_elementos - obstaculo_aleatório.get_height()))

                        #Verifica se o obstaculo definido é um passaro:
                        if obstaculo_aleatório in lista_imagens['Obstaculo'][7:]:
                            #Defini a altura aleatóriamente do passaro:
                            altura = choice([base_elementos - obstaculo_aleatório.get_height(),
                                            base_elementos - (obstaculo_aleatório.get_height() * 1.75),
                                            base_elementos - (obstaculo_aleatório.get_height() * 2.3)])
                            #Defini a posição do passaro:
                            posicao_obstaculo = lista_imagens['Obstaculo'][0].get_rect(topleft=(dimensão[0], altura))
                        
                        #Verifica se o obstaculo definido está entre os CACTO:
                        if obstaculo_aleatório in lista_imagens['Obstaculo'][:7]:
                            #Adiciona um novo CACTO ao conjunto:
                            lista_de_elementos['obstaculos'].add(funcional.elementos(janela, obstaculo_aleatório, pygame.Rect(posicao_obstaculo)))
                        #Caso o obstaculo definido não esteja entre os cactos, um passaro será adicionado a seu conjunto:
                        else:
                            lista_de_elementos['passaro'].add(funcional.elementos(janela, obstaculo_aleatório, pygame.Rect(posicao_obstaculo), frame=[lista_imagens['Obstaculo'][7], lista_imagens['Obstaculo'][8]]))
                        #Adiciona uma nova NUVEM ao conjunto NUVEM:
                        lista_de_elementos['Nuvens'].add(funcional.elementos(janela, lista_imagens['cenario'][1], [dimensão[0], randint(int(info_layout['posicao'][1]), int(base_elementos) - 50)]))
                
                    #Defini o deslocamento dos elementos:
                    if categorias == 'Nuvens':
                        elemento.desloc[0] = deslocamento_de_elementos / 3
                    elif categorias == 'passaro':
                        elemento.desloc[0] = deslocamento_de_elementos / 1.1
                    else:  
                        elemento.desloc[0] = deslocamento_de_elementos

                    #Move o elemento:
                    elemento.mover_X()

                    #CICLO CIRCADIANO DO JOGO:
                    #Verifica se a pontuação atual é divisivel por 700:
                    if (int(pontos) + 1) % 700 == 0 and pontuação_chave:
                        #Caso o ciclo circadiano seja True, ficara NOITE:
                        if ciclo_circadiano:
                            #Muda os sprites do jogo, para os sprites de NOITE:
                            lista_imagens = imagens_noite
                            ciclo_circadiano = False
                            #Altera a cor da te la de funfo (Layout):
                            info_layout['cor'] = (25, 25, 25)
                            #Altera a cor da janela:
                            cor_janela = (15, 15, 15)
                        #Caso o ciclo circadiano seja False, ficara DIA:
                        else:
                            #Muda os sprites do jogo, para os sprites de NOITE:
                            lista_imagens = imagens_dia
                            ciclo_circadiano = True
                            #Altera a cor da te la de funfo (Layout):
                            info_layout['cor'] = (255, 255, 255)
                            #Altera a cor da janela:
                            cor_janela = (225, 225, 225)

                        #Muda o sprite das estradas para NOITE ou DIA:
                        for estrada in lista_de_elementos['estrada']:
                            estrada.imagem = lista_imagens['cenario'][0]
                        
                        #Muda o sprite dos elementos de reiniciar, para NOITE ou DIA:
                        for pos, item in enumerate(lista_de_elementos['Restart']):
                            item.imagem = lista_imagens['restart'][pos] 

                    #FAZ COM QUE QUANDO A PONTUAÇÃO FOR DIVISIVEL POR 100, SEJA EMITIDO True EM "pontuação_chave" UMA VEZ:
                    #Verifica se a pontuação é divisivel por 100:
                    if (int(pontos) + 1) % 100 == 0 and pontuação_chave:
                        pontuação_chave = False
                        #Aumento o aumento de intervalo a cada marco de 100 pontos:
                        aumento_intervalo += 1.5
                    #Verifica se a pontuação "não" é divisivel por 100:
                    elif (int(pontos) + 1) % 100 != 0:
                        pontuação_chave = True

                    #ANIMAÇÃO DO PASSARO:
                    #verifica se o elemento seja um passaro:
                    if categorias == 'passaro':
                        #verifica se o contador da animação do passaro seja divisivel por 8:
                        if animação_passaros % 8 == 0:
                            #Altera o sprite principal do passaro:
                            elemento.animar()

                    #MOSTRA O ELEMENTO (CENÁRIO, OBSTACULO E NUVEMS):
                    elemento.mostrarElemento()

            #MOSTRAR E DEFINIR POTUAÇÃO E ANIMAÇÃO DOS 100 PONTOS MULTIPLOS DE 100:
            #Verifica se a pontuação é divisivel por 100:
            if int(pontos) % 100 == 0 and int(pontos) > 0:
                #Verifica o fluxo de som e toca o som da pontuação:
                if fluxo_de_som['pontuação']:
                    som_pontuação = pygame.mixer.Sound('Sons/Pontuação.mp3')
                    som_pontuação.play()
                    fluxo_de_som['pontuação'] = False
                
                #VERIFICA SE O CONTADOR DE INTERAÇÕES É IGUAL A METADE DO LIMITE DE ITERAÇÕES OU IGUAL A 0:
                if iterações_entre_obstaculos == limite / 2 or iterações_entre_obstaculos == 0:
                    #Soma mais um ponto ao tempo de animação da pontuação:
                    tempo_animação_pontos += 1

                #VERIFICA SE O TEMPO DE ANIMAÇÃO DA PONTUAÇÃO É DIVISIVEL POR 2:
                if tempo_animação_pontos % 2 != 0:
                    pass
                #Mostra a pontuação:
                else:
                    textos['pontuação'].mostrarElemento()
                
                #CASO O TEMPO DE ANIMAÇÃO DA PONTUAÇÃO SEJA IGUAL A 8, SERÁ ADICIONADO UM PONTO A PONTUAÇÃO:
                if tempo_animação_pontos == 8:
                    pontos += 1
                    tempo_animação_pontos = 0

            #Caso a pontuação não seja divisivel por 100:
            else:
                #Aumenta a pontuação:
                pontos += (10 - deslocamento_de_elementos / 4) / limite
                #Mostra A pontuação:
                textos['pontuação'].mostrarElemento()
                #Altera o fluxo de som da pontuação:
                fluxo_de_som['pontuação'] = True

            #ADICIONA UM AO CONTADOR DE ITERAÇÃO A CADA ITERAÇÃO E REINICIA SE CHEGAR AO MAXIMO:
            if iterações_entre_obstaculos == limite:
                iterações_entre_obstaculos = 0
            else:
                iterações_entre_obstaculos += 1
                    
            #DEFINI O RECORD E A PONTUAÇÃO ATUAL:
            #Atribui os pontos atuais na pontuação:
            textos['pontuação'].imagem = fonte.render(f'{int(pontos):0>5}', False, (100, 100, 100))
            #Verifica se existe ou não o arquivo RECORD, caso não exista ele criara um novo arquivo:
            funcional.criarArquivo('Record')
            pontuação_record = open('Record', '+r')
            #Se a pontuação atual for superios ao reccord, o record será alterado:
            if int(pontos) > int(pontuação_record.read()):
                #Altera o record:
                pontuação_record.seek(0)
                pontuação_record.write(f'{int(pontos):0>5}')
                textos['record'].imagem = fonte.render(f'HI {int(pontos):0>5}', False, (100, 100, 100))     #Atribui o novo record ao indice record
                pontuação_record.truncate()
                pontuação_record.close()

            #ANIMAÇÃO DE CORRIDA E PULO DO DINO:
            #Caso dino pule, sua animação para:
            if pular:
                Jogador.imagem = lista_imagens['Dinos'][0]
            #Animação de corrida:
            elif int(animações_do_dino) % 2 == 0:
                Jogador.imagem = lista_imagens['Dinos'][2]
            else:
                Jogador.imagem = lista_imagens['Dinos'][3]

            #Animação de abaixar:
            if abaixar:
                    if int(animações_do_dino) % 2 == 0:
                        Jogador.imagem = lista_imagens['Dinos'][4]
                    else:
                        Jogador.imagem = lista_imagens['Dinos'][5]

            #CASO O DINO NÃO ESTEJA PULANDO, SUA POSIÇÃO NORMAL É DEFINIDA:
            if not pular:
                Jogador.posicao = [100, base_elementos - Jogador.posicao[-1]]
                Jogador.definirMedidas()

            #VERIFICA SE A POSIÇÃO DO DINO É DIFERENTE DA BASE:
            if (Jogador.posicao[1] + Jogador.posicao[-1]) != base_elementos:
                #Caso a posição do dino seja diferente da base, o sprite muda:
                Jogador.imagem = lista_imagens['Dinos'][0]

            #MOSTRA O DINO NA TELA
            Jogador.mostrarElemento()

            #ATUALIZA A SUPERFICIE DA JANELA:
            pygame.display.update()

            #LIMITA AS ITERAÇÕES POR SEGUNDO DO LOOP:
            limitador.tick(limite)
