import streamlit as st
from google.oauth2.service_account import Credentials
import pandas as pd


def get_credentials():

    path = "/Users/joaoc/gcloud-creds/rj-smtr-credentials.json"

    return Credentials.from_service_account_file(
        path,
        scopes=[
            "https://www.googleapis.com/auth/bigquery",
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/drive",
        ],
    )


@st.cache(allow_output_mutation=True)
def query_gbq(query, project_id="rj-smtr", update=1):

    return pd.read_gbq(
        query,
        project_id=project_id,
        credentials=get_credentials(),
    )