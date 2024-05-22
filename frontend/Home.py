import streamlit as st
import datetime
import requests
import pandas as pd

st.set_page_config(layout="wide")
st.image("agendar.png", width=200)
st.title("Agenda Médica")

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

# Função para obter os detalhes de um cliente pelo nome
def get_client_details(nome_cliente):
    response = requests.get(f"http://backend:8000/clientes/nome/{nome_cliente}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao obter os detalhes do cliente")
        return None

# Obtendo os nomes dos clientes
client_names = get_client_names()

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

# Adicionar Agendamento
with st.expander("Adicionar um Novo Agendamento"):
    nome_cliente = st.selectbox("Nome do Paciente", options=[""] + client_names)  # Adiciona uma opção vazia
    email_cliente = ""

    if nome_cliente:
        cliente = get_client_details(nome_cliente)
        if cliente:
            email_cliente = cliente.get("email", "")

    with st.form("new_agendamento"):

        nome_paciente = nome_cliente
        data_agendada_input = st.text_input('Data do Agendamento (dd-mm-aaaa)')
        hora_agendada = st.selectbox('Horário de Agendamento', 
                                     ['','9:00','9:30','10:00','10:30','11:00','11:30','12:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00'])
        nome_medico = st.selectbox("Nome do Profissional", options=[""] + profissionais_names)
        categoria_agendamento = st.selectbox('Tipo do Agendamento',
                                             ['','Consulta', 'Retorno', 'Exames', 'Cirurgias'])
        price = st.number_input("Valor da Consulta", min_value=0.01, format="%f")
        email_paciente = st.text_input("E-mail do Paciente", value=email_cliente)
        description = st.text_area("Descrição do Agendamento")
        submit_button = st.form_submit_button("Adicionar Agendamento")

        if submit_button:
            try:
                # Tratamento da data inserida pelo usuário
                data_agendada = data_agendada_input.replace('/', '-')
                # Transformamos a string em data
                data_agendada = datetime.datetime.strptime(data_agendada, '%d-%m-%Y')
                # Transformamos a data no modelo padrão aceito pelo banco de dados
                data_agendada_formatada = data_agendada.strftime('%Y-%m-%d')

                # Fazendo requisição na API
                response = requests.post(
                    "http://backend:8000/agenda/",
                    json={
                        "data_agendada": data_agendada_formatada,
                        "hora_agendada": hora_agendada,
                        "nome_paciente": nome_paciente,
                        "nome_medico": nome_medico,
                        "categoria_agendamento": categoria_agendamento,
                        "price": price,
                        "email_paciente": email_paciente,
                        "description": description,
                    },
                )

                show_response_message(response)
            except ValueError:
                st.error("Erro no formato da data. Por favor, use o formato dd-mm-aaaa.")

            

# Visualizar Agendamento
with st.expander("Visualizar Agendamentos"):
    if st.button("Exibir Todos os Agendamentos"):
        response = requests.get("http://backend:8000/agenda/")
        if response.status_code == 200:
            agendamento = response.json()
            df = pd.DataFrame(agendamento)

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

            # Exibir o DataFrame sem o índice
            st.subheader('Relatório de Cadastro', divider='rainbow')
            st.dataframe(df, hide_index = True) # Tabela Dinâmica
            
            #st.table(df_reset) (Tabela estática)
        else:
            show_response_message(response)

# Obter Detalhes de um Agendamento
with st.expander("Obter Detalhes de um Agendamento"):
    get_id = st.number_input("ID do Agendamento", min_value=1, format="%d")
    if st.button("Buscar Agendamento"):
        response = requests.get(f"http://backend:8000/agenda/id/{get_id}")
        if response.status_code == 200:
            agendamento = response.json()
            df = pd.DataFrame([agendamento])

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

            # Exibe o DataFrame sem o índice
            # st.write(df.to_html(index=False), unsafe_allow_html=True)
            st.dataframe(df, hide_index = True)
        else:
            show_response_message(response)

# Deletar Agendamento
with st.expander("Deletar Agendamento"):
    delete_id = st.number_input("ID do Agendamento para Deletar", min_value=1, format="%d")
    if st.button("Deletar Agendamento"):
        response = requests.delete(f"http://backend:8000/agenda/{delete_id}")
        show_response_message(response)

# Atualizar Produto
with st.expander("Atualizar Agendamento"):
    with st.form("update_agendamento"):
        update_id = st.number_input("ID do Agendamento", min_value=1, format="%d")
        new_data_agendada = st.text_input('Data do Agendamento')
        new_hora_agendada = st.selectbox('Horário de Agendamento', 
                                     ['9:00','9:30','10:00','10:30','11:00','11:30','12:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00'])
        new_nome_paciente = st.text_input("Nome do Paciente")
        new_nome_medico = st.selectbox('Nome do Médico',
                                   ['Sarah Maria de Almeida','Catarina Maria de Almeida','Augusto Emanuel de Almeida','Tomás Emanuel de Almeida'])
        new_categoria_agendamento = st.selectbox('Tipo do Agendamento',
                                             ['Consulta', 'Retorno', 'Exames', 'Cirurgias'])
        new_price = st.number_input("Valor da Consulta", min_value=0.01, format="%f")
        new_email_paciente = st.text_input("Email do Paciente")
        new_description = st.text_area("Descrição do Agendamento")

        update_button = st.form_submit_button("Atualizar Agendamento")

        if update_button:
            update_data = {}
            if new_data_agendada:
                update_data["data_agendada"] = new_data_agendada
            if new_hora_agendada:
                update_data["hora_agendada"] = new_hora_agendada
            if new_nome_paciente:
                update_data["nome_paciente"] = new_nome_paciente
            if new_nome_medico:
                update_data["nome_medico"] = new_nome_medico
            if new_categoria_agendamento:
                update_data["categoria_agendamento"] = new_categoria_agendamento
            if new_price > 0:
                update_data["price"] = new_price
            if new_email_paciente:
                update_data["email_paciente"] = new_email_paciente 
            if new_description:
                update_data["description"] = new_description

            if update_data:
                response = requests.put(
                    f"http://backend:8000/agenda/{update_id}", json=update_data
                )
                show_response_message(response)
            else:
                st.error("Nenhuma informação fornecida para atualização")