import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from gui import gui_main
from ui.comon import show_db_map,show_db_view,get_enum_values,load_ui_title, load_ui_button_loadExampledata, load_ui_viewMode, load_print_json_section
from ui.org import load_ui_organisation_form
from ui.person import load_ui_person_form
from ui.duty import load_ui_duty_form
from ui.enrolment import load_ui_enrolment_form
from ui.group import load_ui_groupManagement_form
from ui.export import load_export_section
from ui.personrelation import load_ui_personrelation_form
from ui.importdata import load_import_section

def main():
    st.set_page_config(layout="wide") 

    # Init session_state
    if "page" not in st.session_state:
        st.session_state.page = "Hem"
    
    if "db" not in st.session_state:
        st.session_state["db"] = {k:{} for k in ["organisations","persons","enrolments","duties","personrelations",
                        "groups","groupmemberships","assignmentroles","activities","groupassignments","dutyassignments","syllabus"]}
        db = st.session_state.db

    db = st.session_state.db

    enums = get_enum_values()
    school_types = enums["school_types"]
    sex_types = enums["sex_types"]
    duty_roles = enums["duty_roles"]
    person_relation_types = enums["person_relation_types"]
    group_types = enums["group_types"]
    assignment_roles = enums["assignment_roles"]
    activity_types = enums["activity_types"]

    # --- Sidebar meny ---
    with st.sidebar:
        st.markdown("")
        selected = option_menu(
            menu_title=None,
            options=["Hem", "Organisation", "Personer", "Inskrivningar", "Anställningar", "Grupper","Föräldrar","JSON", "Export", "Import"],
            #icons=["house", "bar-chart", "gear"],
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {
                    "padding": "0px",
                    "background-color": "#1E1E2F00",
                    "width": "200px"   # <-- här sätter du bredden
                },
                "icon": {"color": "white", "font-size": "20px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin":"0px",
                    "color": "#bbb",
                    "--hover-color": "#2D2D44",
                },
                "nav-link-selected": {
                    "background-color": "#6B63FF00",
                    "color": "white",
                }
            }
        )
        st.session_state.page = selected

    

    # --- Innehåll per sida ---
    if st.session_state.page == "Hem":
        st.title("Hem")

        load_ui_button_loadExampledata(db)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Organisation", len(db["organisations"]))
        with col2:
            st.metric("Personer", len(db["persons"]))
        with col3:
            st.metric("Inskrivningar", len(db["enrolments"]))



        col4, col5, col6 = st.columns(3)
        with col4:
            st.metric("Anställningar", len(db["duties"]))
        with col5:
            st.metric("Grupper", len(db["groups"]))
        with col6:
            st.metric("Aktiviteter", len(db["activities"]))
        st.write("")
        


    elif st.session_state.page == "Organisation":
        load_ui_organisation_form(db, school_types)
        with st.expander("Visa organisationer"):
            st.write("Lista över alla skolor/organisationer")
            df = pd.DataFrame(db["organisations"].values())
            st.dataframe(df)

    elif st.session_state.page == "Personer":
        load_ui_person_form(db, sex_types)
        with st.expander("Visa personer"):
            st.write("Lista över alla personer")
            df = pd.DataFrame(db["persons"].values())
            st.dataframe(df)
    
    elif st.session_state.page == "Föräldrar":
        load_ui_personrelation_form(db, person_relation_types)
        with st.expander("Visa personrelationer"):
            st.write("Lista över alla personrelationer")
            df = pd.DataFrame(db["personrelations"].values())
            if "Responsible" in df.columns:
                df["ResponsibleName"] = df["Responsible"].map(lambda pid: f"{db['persons'][pid]['GivenName']} {db['persons'][pid]['FamilyName']}" if pid in db["persons"] else "")
            if "ResponsibleFor" in df.columns:
                df["ResponsibleForName"] = df["ResponsibleFor"].map(lambda pid: f"{db['persons'][pid]['GivenName']} {db['persons'][pid]['FamilyName']}" if pid in db["persons"] else "")
            st.dataframe(df)

    elif st.session_state.page == "Inskrivningar":
        load_ui_enrolment_form(db, school_types)
        with st.expander("Visa inskrivningar"):
            st.write("Lista över alla inskrivningar")
            df = pd.DataFrame(db["enrolments"].values())
            if "OrganisationId" in df.columns:
                df["OrganisationName"] = df["OrganisationId"].map(lambda oid: db["organisations"][oid]["DisplayName"] if oid in db["organisations"] else "")
            if "PersonId" in df.columns:
                df["PersonName"] = df["PersonId"].map(lambda pid: f"{db['persons'][pid]['GivenName']} {db['persons'][pid]['FamilyName']}" if pid in db["persons"] else "")
            st.dataframe(df)
    
    elif st.session_state.page == "Anställningar":
        load_ui_duty_form(db, duty_roles)
        with st.expander("Visa anställningar"):
            st.write("Lista över alla anställningar")
            df = pd.DataFrame(db["duties"].values())
            if "OrganisationId" in df.columns:
                df["OrganisationName"] = df["OrganisationId"].map(lambda oid: db["organisations"][oid]["DisplayName"] if oid in db["organisations"] else "")
            if "PersonId" in df.columns:
                df["PersonName"] = df["PersonId"].map(lambda pid: f"{db['persons'][pid]['GivenName']} {db['persons'][pid]['FamilyName']}" if pid in db["persons"] else "")
            st.dataframe(df)

    elif st.session_state.page == "Grupper":
        load_ui_groupManagement_form(db, group_types,school_types)
        st.write("")
        with st.expander("Visa grupper"):
            st.write("Lista över alla grupper")
            df = pd.DataFrame(db["groups"].values())
            if "OrganisationId" in df.columns:
                df["OrganisationName"] = df["OrganisationId"].map(lambda oid: db["organisations"][oid]["DisplayName"] if oid in db["organisations"] else "")
            st.dataframe(df)
        with st.expander("Visa aktiviteter"):
            st.write("Lista över aktiviteter")
            df = pd.DataFrame(db["activities"].values())
            if "OrganisationId" in df.columns:
                df["OrganisationName"] = df["OrganisationId"].map(lambda oid: db["organisations"][oid]["DisplayName"] if oid in db["organisations"] else "")
            st.dataframe(df)
        with st.expander("Visa grupps koppling till aktivitet"):
            st.write("Lista över gruppers koppling till aktiviteter")
            df = pd.DataFrame(db["groupassignments"].values())
            if "GroupId" in df.columns:
                df["GroupName"] = df["GroupId"].map(lambda gid: db["groups"][gid]["DisplayName"] if gid in db["groups"] else "")
            if "ActivityId" in df.columns:
                df["ActivityName"] = df["ActivityId"].map(lambda aid: db["activities"][aid]["DisplayName"] if aid in db["activities"] else "")
            st.dataframe(df)
        with st.expander("Visa elevers gruppkopplingar"):
            st.write("Lista över elever i grupper")
            df = pd.DataFrame(db["groupmemberships"].values())
            if "PersonId" in df.columns:
                df["PersonName"] = df["PersonId"].map(lambda pid: f"{db['persons'][pid]['GivenName']} {db['persons'][pid]['FamilyName']}" if pid in db["persons"] else "")
            if "GroupId" in df.columns:
                df["GroupName"] = df["GroupId"].map(lambda gid: db["groups"][gid]["DisplayName"] if gid in db["groups"] else "")
            st.dataframe(df)
        with st.expander("Visa personals koppling i organisatoriska grupper"):
            st.write("Lista över personal i organisationsgrupper")
            df = pd.DataFrame(db["assignmentroles"].values())
            if "GroupId" in df.columns:
                df["GroupName"] = df["GroupId"].map(lambda gid: db["groups"][gid]["DisplayName"] if gid in db["groups"] else "")
            if "DutyId" in df.columns:
                df["PersonName"] = df["DutyId"].map(
                    lambda did: f"{db['persons'][db['duties'][did]['PersonId']]['GivenName']} {db['persons'][db['duties'][did]['PersonId']]['FamilyName']}"
                    if did in db["duties"] and db["duties"][did]["PersonId"] in db["persons"] else ""
                )
            st.dataframe(df)
        with st.expander("Visa personals koppling i aktivitetsgrupper"):
            st.write("Lista över personal i aktivitetsgrupper")
            df = pd.DataFrame(db["dutyassignments"].values())
            if "DutyId" in df.columns:
                df["PersonName"] = df["DutyId"].map(
                    lambda did: f"{db['persons'][db['duties'][did]['PersonId']]['GivenName']} {db['persons'][db['duties'][did]['PersonId']]['FamilyName']}"
                    if did in db["duties"] and db["duties"][did]["PersonId"] in db["persons"] else ""
                )
            if "ActivityId" in df.columns:
                df["ActivityName"] = df["ActivityId"].map(lambda aid: db["activities"][aid]["DisplayName"] if aid in db["activities"] else "")
            st.dataframe(df)


    elif st.session_state.page == "Export":
        load_export_section(db)

    elif st.session_state.page == "Import":
        load_import_section(db)

    elif st.session_state.page == "JSON":
        load_print_json_section(db)

if __name__ == "__main__":
    main()
