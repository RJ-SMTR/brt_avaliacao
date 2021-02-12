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

st.image("imgs/smtr-logo.jpeg")

st.title("Avaliação das estações BRT")


res = st.radio("Selecione uma Visão", ["Geral", "Estações", "Responsáveis"])


if res == "Geral":
    visao_geral.main()


elif res == "Estações":
    estacao.main()

else:
    responsavel.main()