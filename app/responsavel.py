import streamlit as st
import pandas as pd
from utils import query_gbq, highlight_by_column


def main():
    """
    main
    """

    satis_estacoes = query_gbq(
        """
            select 
                t1.*,
                trim(split(seriedade, '(')[safe_offset(0)]) seriedade_simples,
                t2.nome_exibicao_responsavel
            from `rj-smtr.brt_manutencao.questionario_recentes` t1
            join `rj-smtr.brt_manutencao.responsaveis` t2
            on t1.id_responsavel = t2.id_responsavel
            """,
        update=3,
    )

    satis_estacoes["nome_problema_simples"] = satis_estacoes["nome_problema"].apply(
        lambda x: x.split("(")[0]
    )

    responsavel = st.selectbox(
        "Selecione um responsavel",
        satis_estacoes["nome_exibicao_responsavel"].sort_values().unique(),
    )

    nome_problema = st.selectbox(
        "Selecione um problema",
        satis_estacoes.query(f"nome_exibicao_responsavel == '{responsavel}'")[
            "nome_problema_simples"
        ]
        .sort_values()
        .unique(),
    )

    problema = satis_estacoes.query(
        f"nome_exibicao_responsavel == '{responsavel}'"
    ).query(f'nome_problema_simples == "{nome_problema}"')

    st.subheader("Avaliações")

    filterby = ["Urgência", "Insatisfatório"]
    problemas_selecionados = problema[problema["seriedade_simples"].isin(filterby)]

    if len(problemas_selecionados):

        st.dataframe(
            problemas_selecionados.groupby("seriedade_simples")
            .count()[["dt"]]
            .T.assign(hack="")
            .set_index("hack")
        )

        entorno = (
            problemas_selecionados.query('categoria_problema == "Externo"')
            .rename(
                columns={
                    "nome_estacao": "Estação",
                    "seriedade_simples": "Status",
                }
            )
            .sort_values(by="Status", ascending=False)
            .set_index("Estação")[["Status"]]
        )

        if len(entorno):
            st.subheader("Estação Entorno")

            st.dataframe(highlight_by_column(entorno, "Status"))

        dentro = (
            problemas_selecionados.query('categoria_problema == "Interno"')
            .rename(
                columns={
                    "nome_estacao": "Estação",
                    "seriedade_simples": "Status",
                }
            )
            .sort_values(by="Status", ascending=False)
            .set_index("Estação")[["Status"]]
        )

        if len(dentro):

            st.subheader("Estação Dentro")

            st.dataframe(highlight_by_column(dentro, "Status"))
    else:

        st.warning(f"Não existem avaliações negativas")