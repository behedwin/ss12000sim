import streamlit as st
from gui import gui_main

st.set_page_config(layout="wide") 

def main():

    if "db" not in st.session_state:
        st.session_state["db"] = {k:{} for k in ["organisations","persons","enrolments","duties","personrelations",
                        "groups","groupmemberships","assignmentroles","activities","groupassignments","dutyassignments"]}
        db = st.session_state.db

    db = st.session_state.db

    gui_main(db)

if __name__ == "__main__":
    main()
