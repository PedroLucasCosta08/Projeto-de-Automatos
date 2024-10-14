import os
import streamlit as st

class Turing:
    def __init__(self, fita, simbolo_vazio, estado_inicial, estados_finais, func_transicao):
        self.fita = fita
        self.simbolo_vazio = simbolo_vazio
        self.posicao_fita = 0
        self.estado_atual = estado_inicial
        self.estados_finais = estados_finais
        self.func_transicao = func_transicao

    def transicao(self):
        simbolo_atual = self.fita[self.posicao_fita]
        if (self.estado_atual, simbolo_atual) in self.func_transicao:
            estado_novo, novo_simbolo, direcao = self.func_transicao[(self.estado_atual, simbolo_atual)]
            self.fita[self.posicao_fita] = novo_simbolo

            if direcao == "D":
                self.posicao_fita += 1
                if self.posicao_fita >= len(self.fita):
                    self.fita.append(self.simbolo_vazio)
            elif direcao == "E":
                if self.posicao_fita > 0:
                    self.posicao_fita -= 1 
                else:
                    self.fita.insert(0, self.simbolo_vazio)
            else: 
                raise ValueError("Direção inválida")
            
            self.estado_atual = estado_novo 
        else:
            raise ValueError("Não possui transição definida para esse estado e símbolo") 
        
    def turing(self):
        try:
            while self.estado_atual not in self.estados_finais:
                self.transicao()
                st.success(f"Fita atual: {''.join(self.fita)}, Posição da fita: {self.posicao_fita}, Estado Atual: {self.estado_atual}")
        except ValueError as e:
            st.error(f"Erro: {e}")

def define_func_transition_Turing(estados, alfabeto):
    func_transicao = {}
    print("Defina as funções de transição no formato: <novo_estado> <simbolo_escrever> <movimento>:")
    for estado in estados:
        for simbolo in alfabeto:
            print(f"{estado}\t----->\t{simbolo}\t----->\t", end="")
            input_transicao = input().strip()
            
            if input_transicao == ".":
                continue  
            elif input_transicao:
                input_transicao = input_transicao.split()
                if len(input_transicao) == 3:
                    novo_estado = input_transicao[0]
                    simbolo_escrever = input_transicao[1]
                    movimento = input_transicao[2]

                    func_transicao[(estado, simbolo)] = (novo_estado, simbolo_escrever, movimento)
                else:
                    print("Entrada inválida! Por favor, insira no formato: <novo_estado> <simbolo_escrever> <movimento>")
            else:
                print("Transição não definida, utilizando '.' para pular.")
    
    return func_transicao