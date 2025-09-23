import streamlit as st
from util import gen_id
from datetime import date
import pandas as pd

def load_ui_personrelation_form(db, relation_types):
    persons_list = list(db["persons"].keys())
    
    st.subheader("Personrelationer")
    with st.expander("Skapa personrelation"):
        
        if len(persons_list) < 2:
            st.info("Behöver minst två personer för relation")
        else:
            responsible = st.selectbox(
                "Responsible",
                persons_list,
                format_func=lambda x: f"{db['persons'][x]['GivenName']} {db['persons'][x]['FamilyName']}",
                key="pr_responsible"
            )
            responsible_for = st.selectbox(
                "ResponsibleFor",
                [p for p in persons_list if p != responsible],
                format_func=lambda x: f"{db['persons'][x]['GivenName']} {db['persons'][x]['FamilyName']}",
                key="pr_responsible_for"
            )
            relation_type = st.selectbox(
                "RelationType",
                relation_types,
                key="pr_relation_type"
            )
            start_date = st.date_input("StartDate", key="pr_start", value=date.today())
            end_date = st.date_input("EndDate", key="pr_end")
            
            if st.button("Lägg till relation", key="btn_add_relation"):
                rel_id = gen_id()
                db["personrelations"][rel_id] = {
                    "Responsible": responsible,
                    "ResponsibleFor": responsible_for,
                    "RelationType": relation_type,
                    "StartDate": start_date.isoformat(),
                    "EndDate": end_date.isoformat() if end_date else None
                }
                st.success(f"Relation skapad: {db['persons'][responsible]['GivenName']} → {db['persons'][responsible_for]['GivenName']}")

def load_ui_personrelation_table(db):
    with st.expander("Visa personrelationer"):
        st.write("Lista över alla personrelationer")
        df = pd.DataFrame(db["personrelations"].values())
        if "Responsible" in df.columns:
            df["ResponsibleName"] = df["Responsible"].map(lambda pid: f"{db['persons'][pid]['GivenName']} {db['persons'][pid]['FamilyName']}" if pid in db["persons"] else "")
        if "ResponsibleFor" in df.columns:
            df["ResponsibleForName"] = df["ResponsibleFor"].map(lambda pid: f"{db['persons'][pid]['GivenName']} {db['persons'][pid]['FamilyName']}" if pid in db["persons"] else "")

        search = st.text_input("Sök person och relation")
        if search:
            mask = df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)
            df = df[mask]
        st.dataframe(df)
