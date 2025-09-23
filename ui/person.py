import streamlit as st
from util import gen_id
import pandas as pd

def load_ui_person_form(db, sex_types):
    st.subheader("Personer")
    with st.expander("Skapa person"):
        given = st.text_input("GivenName", key="p_given")
        family = st.text_input("FamilyName", key="p_family")
        middle = st.text_input("MiddleName", key="p_middle")
        civic = st.text_input("CivicNo (YYYYMMDDNNNN)", key="p_civic")
        birth = st.date_input("BirthDate", key="p_birth")
        sex = st.selectbox("Sex", sex_types, key="p_sex")
        student_email = st.text_input("StudentEmail", key="p_studentemail")
        staff_email = st.text_input("StaffEmail", key="p_staffemail")
        personal_email = st.text_input("PersonalEmail", key="p_personalemail")
        student_upn = st.text_input("StudentEduPersonPrincipalName", key="p_s_upn")
        staff_upn = st.text_input("StaffEduPersonPrincipalName", key="p_st_upn")
        if st.button("Lägg till person", key="btn_add_person"):
            new_id = gen_id()
            db["persons"][new_id] = {
                "PersonId": new_id,
                "GivenName": given,
                "FamilyName": family,
                "MiddleName": middle,
                "CivicNo": civic,
                "BirthDate": birth.isoformat(),
                "Sex": sex,
                "StudentEmail": student_email,
                "StaffEmail": staff_email,
                "PersonalEmail": personal_email,
                "StudentEduPersonPrincipalName": student_upn,
                "StaffEduPersonPrincipalName": staff_upn
            }
            st.success(f"Person skapad: {given} {family}")

def load_ui_person_table(db):
    with st.expander("Visa personer"):
        st.write("Lista över alla personer")
        df = pd.DataFrame(db["persons"].values())
        search = st.text_input("Sök person")
        if search:
            mask = df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)
            df = df[mask]

        st.dataframe(df)
