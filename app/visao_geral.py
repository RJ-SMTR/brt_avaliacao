import streamlit as st
import pandas as pd
import numpy as np
from utils import query_gbq, highlight_by_index


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
            highlight_by_index(
                satis_corredor.query(f'corredor_estacao == "{corredor}"')
                .rename(
                    columns={
                        "seriedade_simples": "Status",
                        "nome_estacao": "# Estações",
                    }
                )[["Status", "# Estações"]]
                .set_index("Status")
            )
        )

    st.subheader("Satisfação por Responsável")

    satis_responsavel = query_gbq(
        "SELECT * FROM rj-smtr.brt_manutencao.satisfacao_geral_responsavel", update=5
    )

    for responsavel in satis_responsavel["nome_exibicao_responsavel"].unique():

        st.write(f"##### {responsavel}")

        st.dataframe(
            highlight_by_index(
                satis_responsavel.query(f'nome_exibicao_responsavel == "{responsavel}"')
                .query('seriedade_simples != "Sem Avaliação"')
                .groupby(["nome_exibicao_responsavel", "seriedade_simples"])
                .count()
                .reset_index()
                .rename(
                    columns={
                        "seriedade_simples": "Status",
                        "nome_estacao": "# Estações",
                    }
                )[["Status", "# Estações"]]
                .set_index("Status")
            )
        )
