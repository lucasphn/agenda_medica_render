import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("Agenda Médica")

st.markdown('O link público do Power BI não permite dados em tempo real. Portanto, neste ambiente, os dados serão atualizados a cada 1 hora. Em um ambiente corporativo, incorporamos o Power BI com um link seguro, possibilitando o acesso em tempo real.')

# Código HTML do iframe com CSS para responsividade
iframe_code = """
<style>

    .responsive-iframe-container {
        position: relative;
        width: 100%;
        padding-bottom: 56.25%;
        height: 0;
        overflow: hidden;
    }
    .responsive-iframe-container iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 109%;
        border: 0;
    }
</style>

    <div class="responsive-iframe-container">
        <iframe title="Agenda Médica" src="https://app.powerbi.com/view?r=eyJrIjoiZjFkMzc3NjctYjY2MC00OGNiLWE3MDMtYmU0YzU2NjBiOWRjIiwidCI6IjVhY2IyMzk2LWE2ZWEtNDY2Yy1iYmZlLWQ5YTM5MzZmZjUzOCJ9&navContentPaneEnabled=false" allowFullScreen="true"></iframe>
    </div>
"""

# Renderiza o iframe usando o components.html
components.html(iframe_code, height=1507)
