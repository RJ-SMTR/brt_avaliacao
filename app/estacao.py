import streamlit as st
import pandas as pd
import numpy as np
from utils import query_gbq


def main():
    """
    main
    """

    satis_estacoes = query_gbq(
        """select 
                t1.*,
                split(seriedade, '(')[safe_offset(0)] seriedade_simples,
                ordem_seriedade
            from `rj-smtr.brt_manutencao.questionario_recentes` t1
            join `rj-smtr.brt_manutencao.seriedade` t2
            on t1.seriedade = t2.nome_seriedade""",
        update=5,
    )

    corredor = st.selectbox(
        "Selecione um corredor",
        satis_estacoes["corredor_estacao"].sort_values().unique(),
    )

    nome_estacao = st.selectbox(
        "Selecione uma estação",
        satis_estacoes.query(f'corredor_estacao == "{corredor}"')["nome_estacao"]
        .sort_values()
        .unique(),
    )

    estacao = satis_estacoes.query(f'corredor_estacao == "{corredor}"').query(
        f'nome_estacao == "{nome_estacao}"'
    )

    idade_resposta = estacao["idade_resposta_dia"].unique()[0]
    print(type(idade_resposta))
    if np.isnan(idade_resposta):
        st.error(f"#### Esta estação ainda não foi inspecionada")
    elif isinstance(idade_resposta, float):
        if idade_resposta <= 7:
            st.success(f"#### Última inspeção ocorreu há {int(idade_resposta)} dias")
        else:
            st.warning(f"#### Última inspeção ocorreu há {int(idade_resposta)} dias")

    if estacao["seriedade_simples"].unique()[0] != "Sem Avaliação":

        st.dataframe(
            estacao.groupby(["seriedade_simples"])
            .count()[["nome_estacao"]]
            .T.assign(hack="")
            .set_index("hack")
        )

        estacao["nome_problema_simples"] = estacao["nome_problema"].apply(
            lambda x: x.split("(")[0]
        )

        st.subheader("Avaliações Entorno")

        st.dataframe(
            estacao.query('categoria_problema == "Externo"')
            .rename(
                columns={
                    "nome_problema_simples": "Problema",
                    "seriedade_simples": "Status",
                }
            )
            .sort_values(by="Status", ascending=False)
            .assign(hack="")
            .set_index("hack")[["Problema", "Status"]]
        )

        st.subheader("Avaliações Dentro")

        st.dataframe(
            estacao.query('categoria_problema == "Interno"')
            .rename(
                columns={
                    "nome_problema_simples": "Problema",
                    "seriedade_simples": "Status",
                }
            )
            .sort_values(by="Status", ascending=False)
            .assign(hack="")
            .set_index("hack")[["Problema", "Status"]]
        )
