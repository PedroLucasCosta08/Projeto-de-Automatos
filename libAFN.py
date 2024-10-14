#biblioteca para a criacao do AFD apos a conversao
from libAFD import AFD
from libAFD import criar_afd
from main_func import *

#bibliotecas importantes
import os
from graphviz import Digraph

#--------------AFN------------#

class AFN:
    def __init__(self, estados, alfabeto, func_transicao, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.func_transicao = func_transicao
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

    def transicoes(self, estados_atuais, simbolo):
        novos_estados = set()
        for estado in estados_atuais:
            if (estado, simbolo) in self.func_transicao:
                novos_estados.update(self.func_transicao[(estado, simbolo)])
        return novos_estados

    def is_accepting(self, estados_atuais):
        return any(estado in self.estados_finais for estado in estados_atuais)

    
##--------------------------- FUNCAO PARA CRIACAO DO AFD POS-CONVERSAO----------------------------------------##
    def criar_afd(self, nova_Conversion_list, estado_inicial, estados_finais, alfabeto):

            estados_afd = [str(linha[0]) for linha in nova_Conversion_list]
            estado_inicial_afd = str([estado_inicial])
            estados_finais_afd = [str(linha[0]) for linha in nova_Conversion_list if any(e in estados_finais for e in linha[0])]
                
            func_transicao_afd = {}
                
            for linha in nova_Conversion_list:
                for i in range(len(linha)):
                    if(isinstance(linha[i], set)):
                        linha[i] = list(linha[i])

            
            for linha in nova_Conversion_list:
                for i in range(len(linha)):
                    linha[i] = sorted(linha[i])  

            for linha in nova_Conversion_list:
                estado_atual = str(linha[0])
                for index, simbolo in enumerate(alfabeto, start=1):
                    destino = linha[index]
                    if destino:
                        func_transicao_afd[(estado_atual, simbolo)] = str(destino)

            return AFD(estados_afd, alfabeto, func_transicao_afd, estado_inicial_afd, estados_finais_afd)
    
### --------------------------------- Funções para a Conversão de AFN para AFD ------------------------ ###

    def convertendoAFNparaAFD(self, alfabeto, idAutomato):
        
        os.system('cls')
        Conversion_list = [] 
        for _ in range(2**len(self.estados)):
            row = [None] * (len(alfabeto) + 1)
            Conversion_list.append(row)

        self.gerar_combinacoes_iterativo(self.estados, alfabeto, Conversion_list, self.func_transicao)

        nova_Conversion_list = self.filtrar_estados_alcancaveis(Conversion_list,  self.estado_inicial, alfabeto)
    
        automato_afd_convertido = self.criar_afd(nova_Conversion_list, self.estado_inicial, self.estados_finais, alfabeto)
        print("\nAFD Criado com sucesso!")
        print(f"Estados do AFD: {automato_afd_convertido.estados}")
        print(f"Estado Inicial do AFD: {automato_afd_convertido.estado_inicial}")
        print(f"Estados Finais do AFD: {automato_afd_convertido.estados_finais}")
        print(f"Função de Transição do AFD: {automato_afd_convertido.func_transicao}")
      
        #criando diretorio
        if not os.path.exists("Automatos_Convertidos"):
            os.makedirs("Automatos_Convertidos")

        #criando imagem AFD
        imgAutomatoConvertido = Digraph('AFD')
        imgAutomatoConvertido.format = 'png'
        imgAutomatoConvertido.attr(rankdir='LR')  # Direção da visualização (da esquerda para a direita)
        imgAutomatoConvertido.attr('node', shape='circle')  

        for (estado, simbolo), destinos in automato_afd_convertido.func_transicao.items():
                if(estado == automato_afd_convertido.estados_finais):
                    imgAutomatoConvertido.node(estado, estado, shape= 'doublecircle')
                else:
                    imgAutomatoConvertido.node(estado, estado)
                
                if(destinos != '.'):
                    imgAutomatoConvertido.edge(estado, destinos, label=simbolo) 

        #salvando imagem AFD
        output_path = os.path.join("Automatos_Convertidos", 'AFD_' + idAutomato)
        imgAutomatoConvertido.render(output_path, cleanup=True)

        return automato_afd_convertido

    def gerar_combinacoes_iterativo(self, estados, alfabeto, Conversion_list, func_transicao):
        n = len(estados)
        num_combinacoes = 2 ** n

        for i in range(num_combinacoes):
            combinacao = []

            for j in range(n):
                if (i & (1 << j)) != 0:
                    combinacao.append(estados[j])
                
            Conversion_list[i][0] = combinacao
                
            for letras in range(len(alfabeto)):
                simbolo = alfabeto[letras]
                estados_destino = set()

                for estado in combinacao:
                    if (estado, simbolo) in func_transicao:
                        estados_destino.update(func_transicao[(estado, simbolo)])

                Conversion_list[i][letras + 1] = estados_destino if estados_destino else None

    def filtrar_estados_alcancaveis(self, Conversion_list, estado_inicial, alfabeto):
        estados_alcancaveis = set()
        estados_pendentes = [frozenset([estado_inicial])]

        while estados_pendentes:
            estados_atuais = estados_pendentes.pop()
            estados_alcancaveis.add(estados_atuais)

            for simbolo_index in range(1, len(alfabeto) + 1):
                for linha in Conversion_list:
                    if frozenset(linha[0]) == estados_atuais:
                        estados_destino = linha[simbolo_index]
                        if estados_destino:
                            estados_destino_fs = frozenset(estados_destino)
                            if estados_destino_fs not in estados_alcancaveis:
                                estados_pendentes.append(estados_destino_fs)

        nova_Conversion_list = [linha for linha in Conversion_list if frozenset(linha[0]) in estados_alcancaveis]
        return nova_Conversion_list
### ----------------------------------------------------------------------------------------------------------------- ###

##------------------------------------------- FUNCAO PARA RECONHECIMENTO DE CADEIA DO AFN ---------------------------------------## 

    def reconhecer_cadeiaAFN(self, entrada):
        estados_atuais = {self.estado_inicial}

        for simbolo in entrada:
            print(f"Estados atuais: {estados_atuais}")
            print(f"Entrada atual: {simbolo}")
            estados_atuais = self.transicoes(estados_atuais, simbolo)
            print(f"Próximos estados: {estados_atuais}")

        if self.is_accepting(estados_atuais):
            return True
        else:
            return False
    
## -------------------------------------------------------------------------------------------------------------------------- ##
