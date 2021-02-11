import streamlit as st
import visao_geral
import estacao
import responsavel

# Hide Menu
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Avaliação das estações BRT")

option = st.selectbox("Selecione uma visão", ["Geral", "Estações", "Responsáveis"])

if option == "Geral":

    visao_geral.main()

elif option == "Estações":

    estacao.main()

elif option == "Responsáveis":

    responsavel.main()
