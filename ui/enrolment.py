import streamlit as st
from util import gen_id
from datetime import date
import pandas as pd

def load_ui_enrolment_form(db, school_types):
    persons_list = list(db["persons"].keys())
    org_list = list(db["organisations"].keys())
    st.subheader("Enrolments")
    with st.expander("Skapa enrolment"):

        if not persons_list or not org_list:
            st.info("Ingen person eller organisation tillgänglig")
        else:
            enrol_person = st.selectbox(
                "Elev",
                list(db["persons"].keys()),
                format_func=lambda x: f"{db['persons'][x]['GivenName']} {db['persons'][x]['FamilyName']}",
                key="enrol_person"
            )
            enrol_org = st.selectbox(
                "Organisation",
                list(db["organisations"].keys()),
                format_func=lambda x: db['organisations'][x]['DisplayName'],
                key="enrol_org"
            )
            school_type = st.selectbox("SchoolType", school_types, key="enrol_school_type")
            school_year = st.text_input("SchoolYear", key="enrol_school_year")
            start_date = st.date_input("StartDate", key="enrol_start", value=date.today())
            end_date = st.date_input("EndDate", key="enrol_end")

            if st.button("Lägg till enrolment", key="btn_add_enrol"):
                enrol_id = gen_id()
                db["enrolments"][enrol_id] = {
                    "EnrolmentId": enrol_id,
                    "OrganisationId": enrol_org,
                    "PersonId": enrol_person,
                    "SchoolType": school_type,
                    "StartDate": start_date.isoformat(),
                    "EndDate": end_date.isoformat() if end_date else None,
                    "SchoolYear": school_year
                }
                st.success(f"Enrolment skapad: {db['persons'][enrol_person]['GivenName']} → {school_year}")

def load_ui_enrolment_table(db):
    with st.expander("Visa inskrivningar"):
        st.write("Lista över alla inskrivningar")
        df = pd.DataFrame(db["enrolments"].values())
        if "OrganisationId" in df.columns:
            df["OrganisationName"] = df["OrganisationId"].map(lambda oid: db["organisations"][oid]["DisplayName"] if oid in db["organisations"] else "")
        if "PersonId" in df.columns:
            df["PersonName"] = df["PersonId"].map(lambda pid: f"{db['persons'][pid]['GivenName']} {db['persons'][pid]['FamilyName']}" if pid in db["persons"] else "")

        search = st.text_input("Sök inskrivning (elev)")
        if search:
            mask = df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)
            df = df[mask]
        st.dataframe(df)
        

