import os
from libAFN import AFN 
from libAFD import AFD
from graphviz import Digraph
import random
from turing import *

##_-------------------------------FUNCAO PARA DEFINIÇÂO DA FUNCAO DE TRANSICAO----------------------------##
def define_func_transition(estados, alfabeto):
    func_transicao = {}
    print("Defina as funções de transição:")
    for estado in estados:
        for simbolo in alfabeto:
            print(f"{estado}\t----->\t{simbolo}\t----->\t", end="")
            proximos_estados = input().split()

            if proximos_estados == ["."]:
                func_transicao[(estado, simbolo)] = set()
            else:
                func_transicao[(estado, simbolo)] = set(proximos_estados)

    return func_transicao
##----------------------------------------------------------------------------------------------------------##

##-----------------FUNCAO PARA CRIACAO DE DIRETORIO_-------------------------------------##
def create_directory(new_directory):

        if not os.path.exists(new_directory):
            os.makedirs(new_directory)
##-----------------=-----------------------------------------------------------------##

##-----------------------------FUNCAO PARA CRIACAO DA IMAGEM DO AUTOMATOS----------------------------##
def create_img(automato):

    #Criação para AFD
    if(isinstance(automato, AFD)):
        imgAutomato = Digraph('AFD')
        imgAutomato.format = 'png'
        imgAutomato.attr(rankdir='LR')  # Direção da visualização (da esquerda para a direita)
        imgAutomato.attr('node', shape='circle')  

        for (estado, simbolo), destinos in automato.func_transicao.items():
                if(estado == automato.estados_finais):
                    imgAutomato.node(estado, estado, shape= 'doublecircle')
                else:
                    imgAutomato.node(estado, estado)
                
                if(destinos != '.'):
                    imgAutomato.edge(estado, destinos, label=simbolo) 

    #Criação para AFN
    elif(isinstance(automato, AFN)):
        imgAutomato = Digraph('AFN')
        imgAutomato.format = 'png'
        imgAutomato.attr(rankdir='LR')  # Direção da visualização (da esquerda para a direita)
        imgAutomato.attr('node', shape='circle')    

        for (estado, simbolo), destinos in automato.func_transicao.items():
            if(estado == automato.estados_finais):
                imgAutomato.node(estado, estado, shape = 'doublecircle')
            else:
                imgAutomato.node(estado, estado)
                
            if(destinos != '.'):
                for destino in destinos:
                    imgAutomato.edge(tail_name=estado, head_name=destino, label=simbolo)

    return imgAutomato
##--------------------------------------------------------------------------------------------------------------------## 

##-----------------------------FUNCAO PARA CRIACAO DA IMAGEM DA M.TURING----------------------------##
def create_img_MTuring(MTuring):
    dot = Digraph(comment='Máquina de Turing', format='png')
    all_states = set()
    for (estado, _), (estado_destino, _, _) in MTuring.func_transicao.items():
        all_states.add(estado)
        all_states.add(estado_destino)

    for estado in all_states:
        if estado in MTuring.estados_finais:
            dot.node(estado, estado, shape='doublecircle')
        else:
            dot.node(estado, estado)
        
    for (estado, simbolo), (estado_destino, simbolo_escrito, movimento) in MTuring.func_transicao.items():
        label = f'{simbolo} -> {simbolo_escrito}, {movimento}'
        dot.edge(estado, estado_destino, label=label)

    return dot
##--------------------------------------------------------------------------------------------------------------------## 

def save_img_Turing(imgMTuring, new_directory):

    output_path = os.path.join(new_directory, 'M_Turing')
   
    imgMTuring.render(output_path, cleanup=True)  

##-----------------------------------FUNCAO PARA SALVAR AS IMAGENS------------------------------------------##
def save_img(imgAutomato, new_directory, idAutomato, afn=None, afd=None):
    if afd:
        output_path = os.path.join(new_directory, 'AFD_' + idAutomato)
    elif afn:
        output_path = os.path.join(new_directory, 'AFN_' + idAutomato)
    else:
        output_path = os.path.join(new_directory, 'AFD_Convertido_' + idAutomato)
        
    imgAutomato.render(output_path, cleanup=True)    
##--------------------------------------------------------------------------------------------------------------##

## -------------------------- FUNCAO PARA GERAR STRINGS ALEATORIAS PARA O TESTE DE EQUIVALENCIA ----------------------##

def gerador_cadeias(alfabeto, max_cadeias, max_tamanho):
    #Gera uma lista de cadeias aleatórias baseadas em um alfabeto.#
    cadeias = []
    for _ in range(max_cadeias):
        length = random.randint(1, max_tamanho)  # Gera um comprimento aleatório para a string
        string = ''.join(random.choice(alfabeto) for _ in range(length))  # Cria a string
        cadeias.append(string)
    return cadeias

## -------------------------------------------------------------------------------------------------------------------##