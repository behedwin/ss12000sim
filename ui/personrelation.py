import streamlit as st
from util import gen_id
from datetime import date

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
