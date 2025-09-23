import streamlit as st
from util import gen_id
import pandas as pd

def load_ui_organisation_form(db, school_types):
    st.subheader("Organisationer")
    with st.expander("Skapa organisation"):
        org_name = st.text_input("DisplayName", key="org_name")
        org_school_types = st.multiselect("SchoolTypes", school_types, key="org_schooltypes")
        org_start = st.date_input("StartDate", key="org_start")
        org_end = st.date_input("EndDate", key="org_end")
        org_code = st.text_input("SchoolUnitCode", key="org_code")
        org_short = st.text_input("ShortName", key="org_short")
        if st.button("Lägg till organisation", key="btn_add_org"):
            new_id = gen_id()
            db["organisations"][new_id] = {
                "OrganisationId": new_id,
                "DisplayName": org_name,
                "SchoolTypes": org_school_types,
                "StartDate": org_start.isoformat(),
                "EndDate": org_end.isoformat() if org_end else None,
                "SchoolUnitCode": org_code,
                "ShortName": org_short
            }
            st.success(f"Organisation skapad: {org_name}")

def load_ui_organisation_table(db):
    with st.expander("Visa organisationer"):
        st.write("Lista över alla skolor/organisationer")
        df = pd.DataFrame(db["organisations"].values())
        search = st.text_input("Sök organisation")
        if search:
            mask = df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)
            df = df[mask]        
        st.dataframe(df)