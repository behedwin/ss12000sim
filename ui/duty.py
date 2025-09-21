import streamlit as st
from util import gen_id
from datetime import date

def load_ui_duty_form(db, duty_roles):
    persons_list = list(db["persons"].keys())
    org_list = list(db["organisations"].keys())
    st.subheader("Duties")
    with st.expander("Skapa duty"):
        if not persons_list or not org_list:
            st.info("Ingen person eller organisation tillgänglig")
        else:
            duty_person = st.selectbox("Person", list(db["persons"].keys()), format_func=lambda x: f"{db['persons'][x]['GivenName']} {db['persons'][x]['FamilyName']}", key="d_person")
            duty_org = st.selectbox("Organisation", list(db["organisations"].keys()), format_func=lambda x: db['organisations'][x]['DisplayName'], key="d_org")
            duty_role = st.selectbox("DutyRole", duty_roles, key="d_role")
            duty_start = st.date_input("StartDate", key="d_start", value=date.today())
            duty_end = st.date_input("EndDate", key="d_end")
            signature = st.text_input("Signature", key="d_signature", value="auto-sign")

            if st.button("Lägg till duty", key="btn_add_duty"):
                duty_id = gen_id()
                db["duties"][duty_id] = {
                    "DutyId": duty_id,
                    "PersonId": duty_person,
                    "OrganisationId": duty_org,
                    "StartDate": duty_start.isoformat(),
                    "EndDate": duty_end.isoformat() if duty_end else None,
                    "DutyRole": duty_role,
                    "Signature": signature
                }
                st.success(f"Duty skapad: {duty_role}")
