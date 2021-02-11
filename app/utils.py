import streamlit as st
from google.oauth2.service_account import Credentials
import pandas as pd
import os
import json
import base64
import datetime


def decogind_base64(message):
    # decoding the base64 string
    base64_bytes = message.encode("ascii")
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode("ascii")


def get_credentials():

    creds = json.loads(decogind_base64(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]))
    print(creds)
    # "/Users/joaoc/gcloud-creds/rj-smtr-credentials.json"

    return Credentials.from_service_account_info(
        creds,
        scopes=[
            "https://www.googleapis.com/auth/bigquery",
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/drive",
        ],
    )


@st.cache(allow_output_mutation=True)
def query_gbq(
    query,
    project_id="rj-smtr",
    update=1,
    time=datetime.datetime.now().strftime("%Y-%m-%d-%H"),
):

    return pd.read_gbq(
        query,
        project_id=project_id,
        credentials=get_credentials(),
    )