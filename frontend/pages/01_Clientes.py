import streamlit as st
import datetime
import requests
import pandas as pd

st.set_page_config(layout="wide")
st.image("agendar.png", width=200)
st.title("Área do Cliente")

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

# Função para obter os nomes dos clientes
def get_client_names():
    response = requests.get("http://backend:8000/clientes/")
    if response.status_code == 200:
        clientes = response.json()
        return sorted([cliente['nome'] for cliente in clientes])
    else:
        st.error("Erro ao obter os nomes dos clientes")
        return []

# Obtendo os nomes dos clientes
client_names = get_client_names()

with st.expander('Adicionar um Novo Cliente'):
    with st.form('new_cliente'):
        nome_do_cliente = st.text_input('Nome do Cliente')
        data_nascimento_cliente_input = st.text_input('Data de Nascimento (dd-mm-aaaa)')
        cpf_cliente = st.text_input('CPF')
        uf_cliente = st.text_input('UF')
        cidade_cliente = st.text_input('Cidade')
        bairro_cliente = st.text_input('Bairro')
        rua_cliente = st.text_input('Rua/Logradouro')
        numero_cliente = st.text_input('Número')
        email_cliente = st.text_input('E-mail')
        telefone_cliente = st.text_input('Telefone')

        submit_button = st.form_submit_button('Adicionar Novo Cliente')

        if submit_button:
           
            # Tratamento da data inserida pelo usuário
            # Se o usuário digitar a data com '/' o python trata o dado
            data_nascimento = data_nascimento_cliente_input.replace('/', '-')
            # Aqui transformamos a string em data
            data_nascimento = datetime.datetime.strptime(data_nascimento, '%d-%m-%Y')
            # Aqui transformamos a data no modelo padrão aceito pelo banco de dados
            data_nascimento_formatada = data_nascimento.strftime('%Y-%m-%d')

            # Fazendo requisição na API
            response = requests.post(
                "http://backend:8000/clientes/",
                json={
                    "nome": nome_do_cliente,
                    "data_nascimento": data_nascimento_formatada,
                    "cpf": cpf_cliente,
                    "uf": uf_cliente,
                    "cidade": cidade_cliente,
                    "bairro": bairro_cliente,
                    "rua": rua_cliente,
                    "numero": numero_cliente,
                    "email": email_cliente,
                    "telefone": telefone_cliente
                },
            )

            show_response_message(response)      

# Visualizar Todos os Clientes
with st.expander("Visualizar Clientes"):
    if st.button("Exibir Todos os Clientes"):
        response = requests.get("http://backend:8000/clientes/")
        if response.status_code == 200:
            clientes = response.json()
            df = pd.DataFrame(clientes)

            # Renomenado colunas
            df = df.rename(columns={
                "id": "ID",
                "nome": "Nome Cliente",
                "data_nascimento": "Data de Nascimento",
                "cpf": "CPF",
                "uf": "Estado",
                "cidade": "Cidade",
                "bairro": "Bairro",
                "rua": "Rua",
                "numero": "Número",
                "email": "E-mail",
                "telefone": "Telefone",
                "created_at": "Criado em:"
            })

            # Ordenar Dataframe por ordem alfabética
            df = df.sort_values(by = 'Nome Cliente')
            st.subheader('Relatório de Cadastro', divider='rainbow')
            st.dataframe(df, hide_index = True)
        
        else:
            show_response_message(response)

# Obter Detalhes de um Cliente      
with st.expander("Obter Detalhes de um Cliente"):
    name_client = st.selectbox("Nome do Paciente", options=[""] + client_names)
    if st.button("Buscar Cliente"):
        response = requests.get(f"http://backend:8000/clientes/nome/{name_client}")
        if response.status_code == 200:
            clientes = response.json()
            df = pd.DataFrame([clientes])

            # Renomenado colunas
            df = df.rename(columns={
                "id": "ID",
                "nome": "Nome Cliente",
                "data_nascimento": "Data de Nascimento",
                "cpf": "CPF",
                "uf": "Estado",
                "cidade": "Cidade",
                "bairro": "Bairro",
                "rua": "Rua",
                "numero": "Número",
                "email": "E-mail",
                "telefone": "Telefone",
                "created_at": "Criado em:"
            })
            st.subheader('Informações Cadastrais', divider='rainbow')
            st.dataframe(df, hide_index = True)
        # TABELA DE AGENDAMENTOS

        response = requests.get(f"http://backend:8000/agenda/nome/{name_client}")
        if response.status_code == 200:
            agendamento = response.json()
            df_agendamentos = pd.DataFrame(agendamento)

            if df_agendamentos.empty:
                st.error("Nenhum agendamento encontrado para o cliente selecionado.")
            else:            
                # Renomear as colunas para nomes mais amigáveis
                df_agendamentos = df_agendamentos.rename(columns={
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
                df_agendamentos["data_hora_agendada"] = pd.to_datetime(df_agendamentos["Data Agendada"] + " " + df_agendamentos["Hora Agendada"])
                df_agendamentos = df_agendamentos.sort_values(by="data_hora_agendada")

                # Excluir a coluna auxiliar
                df_agendamentos = df_agendamentos.drop(columns=["data_hora_agendada"])

                # Exibe o DataFrame sem o índice
                st.subheader('Todos os Agendamentos', divider='rainbow')
                st.dataframe(df_agendamentos, hide_index = True)
        else:
            show_response_message(response)


# Deletar Cliente
with st.expander("Excluir Cliente"):
    delete_id = st.number_input("ID do Cliente para Exclusão", min_value=1, format="%d")
    if st.button("Excluir Cliente"):
        response = requests.delete(f"http://backend:8000/clientes/{delete_id}")
        show_response_message(response)

# Atualizar Produto
with st.expander("Atualizar dados do Cliente"):
    with st.form("update_cliente"):
        update_id = st.number_input("ID do Cliente", min_value=1, format="%d")
        update_nome_do_cliente = st.text_input('Nome do Cliente')
        update_data_nascimento_cliente = st.text_input('Data de Nascimento (dd-mm-aaaa)')
        update_cpf_cliente = st.text_input('CPF')
        update_uf_cliente = st.text_input('UF')
        update_cidade_cliente = st.text_input('Cidade')
        update_bairro_cliente = st.text_input('Bairro')
        update_rua_cliente = st.text_input('Rua/Logradouro')
        update_numero_cliente = st.text_input('Número')
        update_email_cliente = st.text_input('E-mail')
        update_telefone_cliente = st.text_input('Telefone')

        update_button = st.form_submit_button("Atualizar Dados")

        if update_button:
            update_dados = {} # iniciando solitiação json
            if update_nome_do_cliente:
                update_dados["nome"] = update_nome_do_cliente
            if update_data_nascimento_cliente:
                update_dados["data_nascimento"] = update_data_nascimento_cliente
            if update_cpf_cliente:    
                update_dados['cpf'] = update_cpf_cliente
            if update_uf_cliente:
                update_dados['uf'] = update_uf_cliente
            if update_cidade_cliente:
                update_dados['cidade'] = update_cidade_cliente
            if update_bairro_cliente:
                update_dados['bairro'] = update_bairro_cliente
            if update_rua_cliente:
                update_dados['rua'] = update_rua_cliente
            if update_numero_cliente:
                update_dados['numero'] = update_numero_cliente
            if update_email_cliente:
                update_dados['email'] = update_email_cliente
            if update_telefone_cliente:
                update_dados['telefone'] = update_telefone_cliente
            
            if update_dados:
                response = requests.put(
                    f"http://backend:8000/clientes/{update_id}" , json=update_dados
                )

                show_response_message(response)
            else:
                st.error("Nenhuma informação fornecida para atualização, ou ID não encontrado.")

