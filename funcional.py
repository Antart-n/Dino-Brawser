'''
Um módulo que usa como base o PYGAME, para facilitar a manipulação de imagens,
criação/verificação de arquivo e probabilidade de numeros. Este módulo pode ser aplicado em projetos semelhantes,
mas ele é feito especialmente para o jogo "Dino Brawser"
'''
import pygame
from random import randint, choice
pygame.init()


class elementos:
    '''
    DESCRIÇÃO:
    |    A classe "elementos" tem a função de simplificar tarefas relacionadas a imagens, como exibir a imagem atribuida
    |    em uma superficie, criar a mascara da imagem, definir a posição, deslocar a imagem e até animar. 
    |    Vale destacar que está classe utiliza como base a biblioteca PYGAME.
    '''
    def __init__(self, local, imagem, posicao=[0, 0], desloc=[0, 0], frame=[]):
        '''
        PARAMETROS:
        |    Param: local -> local onde a imagem será adicionada;
        |    Param: imagem -> Imagem que será adicionada;
        |    Param: posicao -> Uma lista que contem a posição de X e Y, onde a qual a imagem será adicionada;
        |    Param: desloc -> Uma lista com os valores de X e Y, no qual a imagem irá se deslocar;
        |    Param: frame -> Uma lista com os frames da animação da imagem.
        |
        VARIAVEIS:
        |    Var: self.local -> Armazena o local;
        |    Var: self.imagem -> Armazena a imagem;
        |    Var: self.posicao -> Armazena a posição;
        |    Var: self.desloc -> Armazena o deslocamento;
        |    Var: self.mascara -> Armazena a mascara da imagem;
        |    Var: self.frame -> Armazena os frames.
        '''
        self.local = local
        self.imagem = imagem.convert_alpha()
        self.posicao = posicao
        self.desloc = desloc
        self.mascara = pygame.mask.from_surface(self.imagem)
        self.frame = frame


    def mostrarElemento(self):
        '''
        DESCRIÇÃO:
        |    Exibe a imagem na superficie do local, atribuido.
        '''
        self.local.blit(self.imagem, self.posicao)


    def mover_X(self):
        '''
        DESCRIÇÃO:
        |   Altera o valor de X da variavel "posicao" somando com o deslocamento, para dar a impressão de deslocamento.
        |   Exemplo -> (self.posicao[0] += self.desloc[0])
        '''
        self.posicao[0] += self.desloc[0]


    def mover_Y(self):
        '''
        DESCRIÇÃO:
        |   Altera o valor de Y da variavel "posicao" somando com o deslocamento, para dar a impressão de deslocamento.
        |   Exemplo -> (self.posicao[1] += self.desloc[1])
        '''
        self.posicao[1] += self.desloc[1]


    def definirMedidas(self):
        '''
        DESCRIÇÃO:
        |   Atribui a variavel self.posicao, as medidas da imagem com a posição e o tamanho.
        |   Exemplo -> (self.posicao=(X, Y, x, y))
        '''
        self.posicao = self.imagem.get_rect(topleft=(self.posicao))


    def animar(self):
        '''
        DESCRIÇÃO:
        |   Altera a imagem principal, para o próximo frame da lista de frames. Podendo dar a impressão de animação.
        '''
        self.frame.append(self.imagem)
        self.imagem = self.frame[0]
        self.frame.pop(0)


def mudarEscala(itens, tipo, escala=(100, 100), aumento=False):
    '''
    DESCRIÇÃO:
    |    Altera a escala de um grupo de imagens, presentes em listas, tuplas ou dicionários.
    |
    PARAMETROS:
    |    Param: itens -> Corresponde ao grupo de imagens nas quais serão redimencionadas, podem estar dentro de listas, tuplas ou dicionários;
    |    Param: tipo -> Tipo de estrutura de dados. Dentre eles só são permitidos três tipos (listas, tuplas e dicionários).
    |    O tipo deve ser informado ao parametro da sequinte forma, em formato de string: "list", "tuple", "dict".
    |    Param: escala -> Uma tupla com a escala em x e em y que será redimencionado.
    |    Vale destacar que o numero de x e y será multiplicado pelas dimensões atuais da imagem se for para aumentar e dividir
    |    caso for para diminuir a escala.
    |    Param aumento -> Uma valor de False ou True, que define se a escala da imagem irá aumentar ou diminuir. 
    '''
    if tipo == 'dict':
        for categoria, lista in itens.items():
            for item in lista:
                pos = itens[categoria].index(item)
                if aumento:
                    itens[categoria][pos] = pygame.transform.scale(item, (item.get_width() * escala[0], item.get_height() * escala[1]))
                else:
                    itens[categoria][pos] = pygame.transform.scale(item, (item.get_width() / escala[0], item.get_height() / escala[1]))

    elif tipo == 'list' or tipo == 'tuple':
        for item in itens:
            pos = itens.index(item)
            if aumento:
                tamanho = (item.get_width() * escala[0], item.get_height() * escala[1])
            else:
                tamanho = (item.get_width() / escala[0], item.get_height() / escala[1])
            itens[pos] = pygame.transform.scale(item, (tamanho))


def timeAleatorio(*probabilidades):
    '''
    DESCRIÇÃO:
    |    Está função, funciona como um "dado viciado", ela conta quantos valores possui no parametro e retorna o numero do valor escolhido,
    |    mas cada valor pode possuir uma probabilidade diferente de ser retornado. A probabilidade é definida de 0 a 100. A probabilidade da primeira
    |    posição ao ser definida, a probabilidade da posição seguinte é somada com a da posição anterior até que alcance 100, que corresponde a 100%.
    |    Exemplo: (25, 60, 90, 100) = (Posição[1] = 25%, posição[2] = 35%, posição[3] = 30%, posição[4] = 10%)
    |
    PARAMETROS:
    |    Param: *probabilidades -> Parametro com uma tupla com cada posição tendo uma probabilidade diferente de cair aquela posição.
    '''
    tempo_espera = randint(1, 100)
    for pos, porcentagem in enumerate(probabilidades):
        if tempo_espera <= porcentagem:
            return pos + 1


def colisão(elemento1, elemento2):
    '''
    DESCRIÇÃO:
    |    Verifica se houve colisão entre dois elementos diferentes.
    |
    PARAMETROS:
    |    Param: elemento1 -> Primeiro elemento da colisão;
    |    Param: elemento2 -> Segundo elemento da colisão.
    '''
    desvio = (elemento1.posicao.x - elemento2.posicao.x, elemento1.posicao.y - elemento2.posicao.y)
    if elemento2.mascara.overlap(elemento1.mascara, desvio):
        return True
    else:
        return False
    

def criarArquivo(nome):
    '''
    DESCRIÇÃO:
    |    Verifica se o arquivo com o nome inserido existe, caso ele exista nada acontecera,
    |    mas caso não exista, um arquivo com o nome inserido será criado.
    |
    PARAMETROS:
    |    Param: nome -> Nome do arquivo que deseja verificar.
    '''
    try:
        arquivo = open(nome, 'r')
    except:
        arquivo = open(nome, 'w')
        arquivo.write('00000')
    finally:
        arquivo.close()

