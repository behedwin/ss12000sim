import streamlit as st
import uuid
from datetime import date
import pandas as pd


def gen_id():
    return str(uuid.uuid4())

def today():
    return date.today().isoformat()

def export_csv(data_dict):
    dfs = {}
    for key, items in data_dict.items():
        if items:
            df = pd.DataFrame(items.values())
            dfs[key] = df
    return dfs


