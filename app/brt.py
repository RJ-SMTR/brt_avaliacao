import streamlit as st
import visao_geral
import estacao
import responsavel

st.title("Avaliação das estações BRT")

option = st.selectbox("Selecione uma visão", ["Geral", "Estações", "Responsáveis"])

if option == "Geral":

    visao_geral.main()

elif option == "Estações":

    estacao.main()

elif option == "Responsáveis":

    responsavel.main()
