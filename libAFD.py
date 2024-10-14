import os
#----------- AFD -------------#
class AFD:
    def __init__(self, estados, alfabeto, func_transicao, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.func_transicao = func_transicao
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais
        self.estado_atual = estado_inicial

    def transicao(self, simbolo):
        if (self.estado_atual, simbolo) in self.func_transicao:
            self.estado_atual = self.func_transicao[(self.estado_atual, simbolo)]
        else:
            raise ValueError("Transição inválida para o símbolo de entrada.")

    def is_accepting(self):
        return self.estado_atual in self.estados_finais

#------------------------------------- FUNCOES PARA MINIMIZACAO DE AFDs ---------------------------------------------# 

    def minimize(self):
        # Inicialmente separa os estados em finais e não finais
        P = [set(self.estados_finais), set(self.estados) - set(self.estados_finais)]

        # Processo iterativo de minimização
        while True:
            new_P = []
            for group in P:
                # Cria um dicionário para novos subgrupos baseados em transições equivalentes
                subgroups = {}
                for state in group:
                    # Cria uma assinatura para o estado baseado nas transições
                    signature = tuple((symbol, frozenset(self._find_group(self.func_transicao.get((state, symbol)), P))) for symbol in self.alfabeto)
                    if signature not in subgroups:
                        subgroups[signature] = set()
                    subgroups[signature].add(state)
                new_P.extend(subgroups.values())

            if new_P == P:
                break
            P = new_P
        
        # Reconstroi o AFD minimizado
        new_states = {frozenset(group): 'q' + str(i) for i, group in enumerate(P)}
        new_transitions = {}
        new_final_states = set()

        for group, name in new_states.items():
            for state in group:
                if state in self.estados_finais:
                    new_final_states.add(name)
                break

            for symbol in self.alfabeto:
                dest_group = self._find_group(self.func_transicao.get((next(iter(group)), symbol)), P)
                if dest_group is not None:
                    new_transitions[(name, symbol)] = new_states[frozenset(dest_group)]

        new_initial_state = new_states[frozenset(self._find_group(self.estado_inicial, P))]

        return AFD(new_states.values(), self.alfabeto, new_transitions, new_initial_state, new_final_states)

    def _find_group(self, state, groups):
        for group in groups:
            if state in group:
                return group
        return None


    ##--------------- função para reconhecer a entrada de uma cadeia do AFD ---------------##


    def reconhecer_cadeiaAFD(self, entrada):
        estado_atual = self.estado_inicial

        for simbolo in entrada:
            print(f"Estado atual: {estado_atual}")
            print(f"Entrada atual: {simbolo}")

            if (estado_atual, simbolo) in self.func_transicao and self.func_transicao[(estado_atual, simbolo)]:
                estado_atual = self.func_transicao[(estado_atual, simbolo)]
                print(f"Próximo estado: {estado_atual}")
            else:
                estado_atual = None
                print("O autômato não reconheceu a linguagem")
                break

        if estado_atual in self.estados_finais:
            return True
        else:
            return False

# ------------------ FUNCAO AUXILIAR PARA A CRIAÇÃO DE UM AFD APóS A CONVERSÂO DO AFN PARA O AFD ----------------------------------##


def criar_afd( nova_Conversion_list, estado_inicial, estados_finais, alfabeto):

        estados_afd = [str(linha[0]) for linha in nova_Conversion_list]
        estado_inicial_afd = str([estado_inicial])
        estados_finais_afd = [str(linha[0]) for linha in nova_Conversion_list if any(e in estados_finais for e in linha[0])]
            
        func_transicao_afd = {}

        for linha in nova_Conversion_list:
            estado_atual = str(linha[0])
            for index, simbolo in enumerate(alfabeto, start=1):
                destino = linha[index]
                if destino:
                    func_transicao_afd[(estado_atual, simbolo)] = str(destino)

        return AFD(estados_afd, alfabeto, func_transicao_afd, estado_inicial_afd, estados_finais_afd)