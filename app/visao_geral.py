import streamlit as st
import pandas as pd
import numpy as np
from utils import query_gbq


def main():
    """
    main
    """

    st.subheader("Satisfação por Corredor")

    satis_estacao = query_gbq(
        "SELECT * FROM rj-smtr.brt_manutencao.satisfacao_geral_estacao", update=8
    )

    satis_corredor = (
        satis_estacao.groupby(["corredor_estacao", "seriedade_simples"])
        .count()
        .reset_index()
    )

    for corredor in satis_corredor["corredor_estacao"].unique():

        st.write(f"##### {corredor}")

        st.dataframe(
            satis_corredor.query(f'corredor_estacao == "{corredor}"')
            .rename(
                columns={"seriedade_simples": "Status", "nome_estacao": "# Estações"}
            )[["Status", "# Estações"]]
            .set_index("Status")
        )

    st.subheader("Satisfação por Estação")

    st.dataframe(
        satis_estacao.rename(
            columns={"seriedade_simples": "Status", "nome_estacao": "Estação"}
        )
        .sort_values(by="ordem_seriedade", ascending=False)[["Estação", "Status"]]
        .assign(hack="")
        .set_index("hack")
    )

    st.subheader("Satisfação por Responsável")

    satis_responsavel = query_gbq(
        "SELECT * FROM rj-smtr.brt_manutencao.satisfacao_geral_responsavel", update=5
    )

    for responsavel in satis_responsavel["nome_exibicao_responsavel"].unique():

        st.write(f"##### {responsavel}")

        st.dataframe(
            satis_responsavel.query(f'nome_exibicao_responsavel == "{responsavel}"')
            .query('seriedade_simples != "Sem Avaliação"')
            .groupby(["nome_exibicao_responsavel", "seriedade_simples"])
            .count()
            .reset_index()
            .rename(
                columns={"seriedade_simples": "Status", "nome_estacao": "# Estações"}
            )[["Status", "# Estações"]]
            .set_index("Status")
        )
