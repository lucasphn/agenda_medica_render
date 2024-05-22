import streamlit as st
import datetime
import requests
import pandas as pd

st.set_page_config(layout="wide")
st.image("agendar.png", width=200)
st.title("Área do Profissional")

# Função auxiliar para exibir mensagens de erro detalhadas
def show_response_message(response):
    if response.status_code == 200:
        st.success("Operação realizada com sucesso!")
    else:
        try:
            data = response.json()
            if "detail" in data:
                # Se o erro for uma lista, extraia as mensagens de cada erro
                if isinstance(data["detail"], list):
                    errors = "\n".join([error["msg"] for error in data["detail"]])
                    st.error(f"Erro: {errors}")
                else:
                    # Caso contrário, mostre a mensagem de erro diretamente
                    st.error(f"Erro: {data['detail']}")
        except ValueError:
            st.error("Erro desconhecido. Não foi possível decodificar a resposta.")

# Função para obter os nomes dos profissionais
def get_profisional_names():
    response = requests.get("http://backend:8000/profissional/")
    if response.status_code == 200:
        profissionais = response.json()
        return sorted([profissional['nome'] for profissional in profissionais])
    else:
        st.error("Erro ao obter os nomes dos profissionais")
        return []

# Obtendo os nomes dos profissionais
profissionais_names = get_profisional_names()

with st.expander('Adicionar um Novo Profissional'):
    with st.form('new_profissional'):
        nome_do_profissional = st.text_input('Nome do Profissional')
        area_de_atuacao = st.text_input('Área de Atuação')

        submit_button = st.form_submit_button('Adicionar Novo Profissional')

        if submit_button:

            # Fazendo requisição na API
            response = requests.post(
                "http://backend:8000/profissional/",
                json={
                    "nome": nome_do_profissional,
                    "area_atuacao": area_de_atuacao
                },
            )

            show_response_message(response)      

# Visualizar Todos os cadastros
with st.expander("Visualizar Profissionais"):
    if st.button("Exibir Todos os cadastros"):
        response = requests.get("http://backend:8000/profissional/")
        if response.status_code == 200:
            profissionais = response.json()
            df = pd.DataFrame(profissionais)

            # Renomenado colunas
            df = df.rename(columns={
                "id": "ID",
                "nome": "Nome do Profissional",
                "area_atuacao": "Área de atuação",
                "created_at": "Criado em:"
            })

            # Ordenar Dataframe por ordem alfabética
            df = df.sort_values(by = 'Nome do Profissional')

            st.subheader('Relatório de Cadastro', divider='rainbow')
            st.dataframe(df, hide_index = True)
        
        else:
            show_response_message(response)

# Obter Detalhes de um Profisional      
with st.expander("Obter Detalhes de um Profissional"):
    name_profisisonal = st.selectbox("Nome do Profissional", options=[""] + profissionais_names)
    if st.button("Buscar Profissional"):
        response = requests.get(f"http://backend:8000/profissional/nome/{name_profisisonal}")
        if response.status_code == 200:
            profissionais = response.json()
            df = pd.DataFrame([profissionais])

            # Renomenado colunas
            df = df.rename(columns={
                "id": "ID",
                "nome": "Nome do Profissional",
                "area_atuacao": "Área de atuação",
                "created_at": "Criado em:"
            })
            
            st.subheader('Informações Cadastrais', divider='rainbow')
            st.dataframe(df, hide_index = True)

        # TABELA DE AGENDAMENTOS

        response = requests.get(f"http://backend:8000/agenda/profissional/{name_profisisonal}")
        if response.status_code == 200:
            agendamento = response.json()
            df = pd.DataFrame(agendamento)
            if df.empty:
                st.error("Nenhum agendamento encontrado para o cliente selecionado.")
            else:
                # Renomear as colunas para nomes mais amigáveis
                df = df.rename(columns={
                    "id": "ID",
                    "data_agendada": "Data Agendada",
                    "hora_agendada": "Hora Agendada",
                    "nome_paciente": "Nome do Paciente",
                    "nome_medico": "Nome do Médico",
                    "categoria_agendamento": "Categoria de Agendamento",
                    "price": "Preço",
                    "email_paciente": "Email do Paciente",
                    "description": "Descrição",
                    "created_at": "Criado em"
                })

                # Ordenar o DataFrame por data_agendada e hora_agendada
                df["data_hora_agendada"] = pd.to_datetime(df["Data Agendada"] + " " + df["Hora Agendada"])
                df = df.sort_values(by="data_hora_agendada")

                # Excluir a coluna auxiliar
                df = df.drop(columns=["data_hora_agendada"])

                # Ordenar o DataFrame por data_agendada e hora_agendada
                df["data_hora_agendada"] = pd.to_datetime(df["Data Agendada"] + " " + df["Hora Agendada"])
                df = df.sort_values(by="data_hora_agendada")

                # Excluir a coluna auxiliar
                df = df.drop(columns=["data_hora_agendada"])

                # Exibe o DataFrame sem o índice
                st.subheader('Todos os Agendamentos', divider='rainbow')
                st.dataframe(df, hide_index = True)
        else:
            show_response_message(response)


# Deletar Profissional
with st.expander("Excluir Profissional"):
    id_profissional = st.number_input("ID do Profissional para Exclusão", min_value=1, format="%d")
    if st.button("Excluir Profissional"):
        response = requests.delete(f"http://backend:8000/profissional/{id_profissional}")
        show_response_message(response)

# Atualizar Produto
with st.expander("Atualizar dados do Profissional"):
    with st.form("update_profissional"):
        update_id = st.number_input("ID do Profissional", min_value=1, format="%d")
        update_nome_do_profissional = st.text_input('Nome do Profissional')
        update_area_de_atuacao = st.text_input('Área de Atuação')

        update_button = st.form_submit_button("Atualizar Dados")

        if update_button:
            update_dados = {} # iniciando solitiação json
            if update_nome_do_profissional:
                update_dados["nome"] = update_nome_do_profissional
            if update_area_de_atuacao:
                update_dados["area_atuacao"] = update_area_de_atuacao
          
            if update_dados:
                response = requests.put(
                    f"http://backend:8000/profissional/{update_id}" , json=update_dados
                )

                show_response_message(response)
            else:
                st.error("Nenhuma informação fornecida para atualização, ou ID não encontrado.")

