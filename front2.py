import streamlit as st
from main_func import *  # Importa as funções auxiliares do seu projeto
import os
from graphviz import Digraph


# Configuração da página
st.set_page_config(page_title="Projeto de Teoria da Computação", layout="wide")
 
def get_state():
    if 'page' not in st.session_state:
        st.session_state.page = 1 #main
    if 'AFN_or_AFD_or_Turing' not in st.session_state:
        st.session_state.AFN_or_AFD_or_Turing = ""
    if 'num_automatos' not in st.session_state:
        st.session_state.num_automatos = 0
    if 'idAutomato' not in st.session_state:
        st.session_state.idAutomato = 0
    if 'automatos' not in st.session_state:
        st.session_state.automatos = {}

def main():
    st.title("Projeto de Teoria da Computação")

    AFN_or_AFD_or_Turing= st.selectbox("Selecione oque deseja: ", ["AFN", "AFD", "M.Turing"])
    create_button = st.button(label='Criar ' + AFN_or_AFD_or_Turing)
    if create_button: 
        st.session_state.page = 2 #pagina para criar AFNs ou AFDs ou Turing
        st.session_state.AFN_or_AFD_or_Turing = AFN_or_AFD_or_Turing

    if st.session_state.num_automatos > 0:
        st.header("Visualizar e Testar Automatos Criados :")
        view_button = st.button(label="Visualizar Automatos")
        if view_button:
            st.session_state.page = 3 #pagina para visualizar AFNs, AFDs e Maquinas de Turing
        
        for id in st.session_state.automatos:
            if st.session_state.automatos[id]["tipo"] == "AFN":
                hasAFN = True
                break
            else:
                hasAFN = False
        
        if hasAFN:
            st.header("Converter AFNs para AFDs")
            convert_button = st.button("Converter AFNs")
            if convert_button:
                st.session_state.page = 4

        for id in st.session_state.automatos:
            if st.session_state.automatos[id]["tipo"] == "AFDconvertido":
                hasAFDconvertido = True
                break
            else:
                hasAFDconvertido = False
    
        if hasAFDconvertido:
            st.header("Minimizar AFD convertido")
            minimize_button = st.button("Minimizar")
            if minimize_button:
                st.session_state.page = 5

def createObj():
    st.title("Pagina de Criação de " + st.session_state.AFN_or_AFD_or_Turing)

    estados = alfabeto = estado_inicial = estados_finais = ""

    if (st.session_state.AFN_or_AFD_or_Turing == "AFN" or st.session_state.AFN_or_AFD_or_Turing == "AFD"): #AFN ou AFD
        estados = st.text_input("Informe o conjunto de estados (separados por espaço)", " ").split()
        alfabeto = st.text_input("Informe o alfabeto (separados por espaço)", " ").split()
        estado_inicial = st.selectbox("Selecione o estado inicial", estados)
        estados_finais = st.multiselect("Selecione os estados finais", estados)

        if(estados != "" and alfabeto != "" and estado_inicial != "" and estados_finais != ""):
            st.subheader("Definir Funções de Transição")
            func_transicao = {}
            for estado in estados:
                for simbolo in alfabeto:
                    transicao = st.text_input(f"Transição de {estado} com '{simbolo}' (separados por vírgula)", "")
                    destinos = [s.strip() for s in transicao.split(',') if s.strip()]
                    func_transicao[(estado, simbolo)] = destinos

            submit_button = st.button(label='Criar Automato')

        if submit_button:
            st.session_state.idAutomato += 1
            idAutomato = st.session_state.idAutomato
            afd = True
            afn = False
            for destinos in func_transicao.values():
                if len(destinos) > 1:
                    afd = False
                    afn = True
                    break

            if(st.session_state.AFN_or_AFD_or_Turing == "AFN" and afn):
                automato = AFN(estados, alfabeto, func_transicao, estado_inicial, estados_finais)
                tipo = "AFN"
            elif(st.session_state.AFN_or_AFD_or_Turing == "AFD" and afd):
                func_transicao = {key: next(iter(value)) if value else None for key, value in func_transicao.items()}
                automato = AFD(estados, alfabeto, func_transicao, estado_inicial, estados_finais)
                tipo = "AFD"
            elif(st.session_state.AFN_or_AFD_or_Turing == "AFN" and not afn):
                st.error("Criação de AFN impossível! O automato não é não-determinístico.")
                return
            elif(st.session_state.AFN_or_AFD_or_Turing == "AFD" and not afd):
                st.error("Criação de AFD impossível! O automato não é determinístico.")
                return
            else:
                st.error("Opção inválida selecionada.")
                return

            # Criação do diretório para salvar imagens
            new_directory = f'Automatos_{tipo}'
            create_directory(new_directory)

            # Geração e salvamento da imagem do automato
            imgAutomato = create_img(automato)
            strIDAutomato = str(idAutomato)
            if afn:
                save_img(imgAutomato, new_directory, strIDAutomato, afn=True)
            elif afd:
                save_img(imgAutomato, new_directory, strIDAutomato, afd=True)

            # Armazenamento do automato no estado da sessão
            st.session_state.automatos[idAutomato] = {
                'tipo': tipo,
                'automato': automato,
                'diretorio': new_directory
            }

            st.success(f"{tipo} criado e salvo com sucesso! ID: {idAutomato}")

            st.session_state.num_automatos = st.session_state.num_automatos + 1
            st.session_state.page = 1
    else:
        alfabeto = st.text_input("Informe o alfabeto (separados por espaço)", " ").split()
        fita = list(st.text_input("Informe a fita: "  ))
        
        for i in fita:
            if i not in alfabeto:
                st.error("Fita Invalida!")
                break
            else:
                simbolo_vazio = estados = estado_inicial = estados_finais = ""

                simbolo_vazio = st.text_input("Informe o Simbolo Vazio: ")
                estados = st.text_input("Informe os estados (separados por espaço)", " ").split()
                estado_inicial = st.selectbox("Selecione o estado inicial", estados)
                estados_finais = st.multiselect("Selecione os estados finais", estados)
                
                if(estados != "" and alfabeto != "" and estado_inicial != "" and estados_finais != "" and simbolo_vazio != ""):
                    st.subheader("Defina as funções de transição no formato: <novo_estado> <simbolo_escrever> <movimento>:")
                    func_transicao = {}
                    for estado in estados:
                        for simbolo in alfabeto:
                            transicao = st.text_input(f"Transição de {estado} com '{simbolo}' ")
                            if transicao == ".":
                                continue  
                            elif transicao:
                                transicao = transicao.split()
                                if len(transicao) == 3:
                                    novo_estado = transicao[0]
                                    simbolo_escrever = transicao[1]
                                    movimento = transicao[2]

                                    func_transicao[(estado, simbolo)] = (novo_estado, simbolo_escrever, movimento)
                                else:
                                    st.error("Entrada inválida! Por favor, insira no formato: <novo_estado> <simbolo_escrever> <movimento>")
                           

                    submit_button = st.button(label='Criar M.Turing')
                    if submit_button:

                        newTuring = Turing(
                            fita,
                            simbolo_vazio, 
                            estado_inicial, 
                            estados_finais, 
                            func_transicao
                        )

                        st.success("M.Turing Criada com Sucesso!")
                        new_directory = f'M.Turings'
                        create_directory(new_directory)

                        # Geração e salvamento da imagem da M.Turing
                        imgMTuring = create_img_MTuring(newTuring)
                        
                        save_img_Turing(imgMTuring, new_directory)

                        st.success(f"M.Turing criada e salva com sucesso!")

                        st.image(os.path.join(new_directory, f"M_Turing.png"), caption=f"Maquina de Turing")

                        newTuring.turing()

        if st.button("Voltar Para o Menu"):
            st.session_state.page = 1                

def showObjandTest():
    st.sidebar.header("Automatos Criados")
    if st.session_state.automatos:
        selected_id = st.sidebar.selectbox("Selecione o ID do Automato: ", list(st.session_state.automatos.keys()))
        automato_info = st.session_state.automatos[selected_id]
        automato = automato_info['automato']
        tipo = automato_info['tipo']
        diretorio = automato_info['diretorio']
        if tipo == "AFDconvertido":
            idAFN = automato_info['idAFNoriginal']

        st.subheader(f"Automato ID: {selected_id} ({tipo})")

        # Exibição dos detalhes do automato
        st.write(f"**Estados**: {automato.estados}")
        st.write(f"**Alfabeto**: {automato.alfabeto}")
        st.write(f"**Estado Inicial**: {automato.estado_inicial}")
        st.write(f"**Estados Finais**: {automato.estados_finais}")
        st.write("**Funções de Transição**:")
        for (estado, simbolo), destino in automato.func_transicao.items():
            st.write(f"δ({estado}, {simbolo}) → {destino}")

        # Exibição da imagem do automato
        if(tipo == "AFD"):
            st.image(os.path.join(diretorio, f"AFD_{selected_id}.png"), caption=f"Automato ID: {selected_id}")
        elif(tipo == "AFN"):
            st.image(os.path.join(diretorio, f"AFN_{selected_id}.png"), caption=f"Automato ID: {selected_id}")
        elif(tipo == "AFDconvertido"):
            st.image(os.path.join(diretorio, f"AFD_{selected_id}_converted.png"), caption=f"Automato ID: {selected_id}")
            
        ok = ""
        st.subheader(f"Teste de Cadeia Para o Automato de ID: {selected_id}")
        cadeiaParaTeste = st.text_input("Insira a cadeia de entrada: ")
        for letra in cadeiaParaTeste:
            if letra not in automato.alfabeto:
                ok = "False"
                break
            else:
                ok = "True"
        if ok == "True":
            if tipo == "AFD":
                reconheceu = automato.reconhecer_cadeiaAFD(cadeiaParaTeste)
                if reconheceu:
                    st.success("Cadeia aceita pelo AFD!")
                else:
                    st.error("Cadeia não foi aceita pelo AFD!")

            elif tipo == "AFDconvertido":
                reconheceu = automato.reconhecer_cadeiaAFD(cadeiaParaTeste)
                if reconheceu:
                    st.success("Cadeia aceita pelo AFD!")
                else:
                    st.error("Cadeia não foi aceita pelo AFD!")

                st.header("Teste de Equivalencia!")
                st.subheader(f"Automato Convertido ID: {selected_id}, AFN original: {idAFN}")
                AFDreconheceu = automato.reconhecer_cadeiaAFD(cadeiaParaTeste)
                
                automato_info = st.session_state.automatos[idAFN]
                AFNorigem = automato_info['automato']

                AFNreconheceu = AFNorigem.reconhecer_cadeiaAFN(cadeiaParaTeste)
                if AFDreconheceu and AFNreconheceu:
                    st.success("AFN e AFD convertido Equivalentes!")
                else:
                    st.error("AFN e AFD convertido não Equivalentes!")

            elif tipo == "AFN":
                reconheceu = automato.reconhecer_cadeiaAFN(cadeiaParaTeste)
                if reconheceu:
                    st.success("Cadeia aceita pelo AFN!")
                else:
                    st.error("Cadeia não foi aceita pelo AFN!")
        elif ok == "":
            st.error("Digite uma Cadeia!")
        elif ok == "False":
            st.error("Cadeia Não Presente no Alfabeto!!")

    if st.sidebar.button("Voltar para o Menu"):
        st.session_state.page = 1

def convertAFNs():

    st.header("Pagina de Conversão de AFN para AFD")
    if st.session_state.automatos:
        ids_afn = [id for id, info in st.session_state.automatos.items() if info['tipo'] == 'AFN']
        selected_id = st.sidebar.selectbox("Selecione o ID do Automato:", ids_afn)
        automato_info = st.session_state.automatos[selected_id]
        automato = automato_info['automato']
        tipo = automato_info['tipo']
        diretorio = automato_info['diretorio']

        st.subheader(f"Automato ID: {selected_id} ({tipo})")

        # Exibição dos detalhes do automato
        st.write(f"**Estados**: {automato.estados}")
        st.write(f"**Alfabeto**: {automato.alfabeto}")
        st.write(f"**Estado Inicial**: {automato.estado_inicial}")
        st.write(f"**Estados Finais**: {automato.estados_finais}")
        st.write("**Funções de Transição**:")
        for (estado, simbolo), destino in automato.func_transicao.items():
            st.write(f"δ({estado}, {simbolo}) → {destino}")

        # Exibição da imagem do automato
        if(tipo == "AFD"):
            st.image(os.path.join(diretorio, f"AFD_{selected_id}.png"), caption=f"Automato ID: {selected_id}")
        elif(tipo == "AFN"):
            st.image(os.path.join(diretorio, f"AFN_{selected_id}.png"), caption=f"Automato ID: {selected_id}")


        if st.button(f"Converter AFN de ID: {selected_id} para AFD"):
            automatoConvertido = automato.convertendoAFNparaAFD(automato.alfabeto, str(selected_id))
            st.success("Conversão realizada com sucesso!")

            # Salvar o AFD convertido
            create_directory('Automatos_AFD_Convertidos')
            imgAutomatoConv = create_img(automatoConvertido)
            save_img(imgAutomatoConv, "Automatos_AFD_Convertidos", f"{st.session_state.idAutomato + 1}_converted", afd=True)

            # Armazenar o AFD convertido
            st.session_state.idAutomato += 1
            new_id = st.session_state.idAutomato
            st.session_state.automatos[new_id] = {
                'tipo': "AFDconvertido",
                'automato': automatoConvertido,
                'diretorio': "Automatos_AFD_Convertidos",
                'idAFNoriginal' : selected_id
            }

            st.success(f"AFD convertido criado com sucesso! ID: {new_id}")
            st.image(os.path.join("Automatos_AFD_Convertidos", f"AFD_{st.session_state.idAutomato}_converted.png"), caption=f"AFD Convertido ID: {new_id}")

    if st.sidebar.button("Voltar Para o Menu"):
        st.session_state.page = 1

def minimizeAFD():
    st.header("Pagina de Minimização de AFDs Convertidos")
    st.sidebar.header("AFDs Convertidos")
    if st.session_state.automatos:
        ids_afd_convertidos = [id for id, info in st.session_state.automatos.items() if info['tipo'] == 'AFDconvertido']
        selected_id = st.sidebar.selectbox("Selecione o ID do Automato:", ids_afd_convertidos)
        automato_info = st.session_state.automatos[selected_id]
        automato = automato_info['automato']
        tipo = automato_info['tipo']
        diretorio = automato_info['diretorio']
        idAFN = automato_info['idAFNoriginal']

        st.subheader(f"Automato ID: {selected_id} ({tipo})")

        # Exibição dos detalhes do automato
        st.write(f"**Estados**: {automato.estados}")
        st.write(f"**Alfabeto**: {automato.alfabeto}")
        st.write(f"**Estado Inicial**: {automato.estado_inicial}")
        st.write(f"**Estados Finais**: {automato.estados_finais}")
        st.write("**Funções de Transição**:")
        for (estado, simbolo), destino in automato.func_transicao.items():
            st.write(f"δ({estado}, {simbolo}) → {destino}")

        # Exibição da imagem do automato
        st.image(os.path.join("Automatos_AFD_Convertidos", f"AFD_{selected_id}_converted.png"), caption=f"AFD Convertido ID: {selected_id}")

    if st.button("Minimizar"):
        afd_minimizado = automato.minimize()
        create_directory("Automatos_Minimizados")
        img_afd_minimizado = create_img(afd_minimizado)
        save_img(img_afd_minimizado, "Automatos_Minimizados", f"{selected_id}_minimized", afd=True)
        st.success("AFD minimizado criado com sucesso!")
        st.image(os.path.join("Automatos_Minimizados", f"AFD_{selected_id}_minimized.png"), caption=f"AFD Minimizado ID: {selected_id}")

    if st.sidebar.button("Voltar Para o Menu"):
        st.session_state.page = 1

get_state()

# Exibindo páginas com base no estado
if st.session_state.page == 1:
    main()
elif st.session_state.page == 2:
    createObj()
elif st.session_state.page == 3:
    showObjandTest()
elif st.session_state.page == 4:
    convertAFNs()
elif st.session_state.page == 5:
    minimizeAFD()