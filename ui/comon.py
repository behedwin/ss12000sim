import streamlit as st
from graphviz import Digraph
import pandas as pd
from streamlit_option_menu import option_menu

def load_ui_viewMode():
    view_mode = st.radio("Välj vy:", ["Redigera / Exempeldata", "Visa DB", "Visa DB-struktur"])
    return view_mode

def load_print_json_section(db):
    
    
    col1, col2 = st.columns(2)
    with col1:
        #PRINT ORGANISATION JSON
        st.subheader("Organisationer")
        if db["organisations"]:
            st.json(db["organisations"], expanded=False)

        #PRINT PERSON JSON
        st.subheader("Personer")
        if db["persons"]:
            st.json(db["persons"], expanded=False)

        #PRINT DUTIES JSON
        st.subheader("Duties")
        if db["duties"]:
            st.json(db["duties"], expanded=False)

        #PRINT ENROLMENT JSON
        st.subheader("Enrolments")
        if db["enrolments"]:
            st.json(db["enrolments"], expanded=False)

    with col2:
        #PRINT GROUP JSON
        st.subheader("Groups")
        if db["groups"]:
            st.json(db["groups"], expanded=False)

        #PRINT ACTIVITIES JSON
        st.subheader("Activities")
        if db["activities"]:
            st.json(db["activities"], expanded=False)

        #PRINT SYLLABUS JSON
        st.subheader("Syllabus")
        if db["syllabus"]:
            st.json(db["syllabus"], expanded = False)

    st.write("")
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("AssignmentRoles (automatiska)")
        if db["assignmentroles"]:
            st.json(db["assignmentroles"], expanded=False)

        st.subheader("DutyAssignments (automatiska)")
        if db["dutyassignments"]:
            st.json(db["dutyassignments"], expanded=False)

    with col2:
        st.subheader("GroupAssignments (automatiska)")
        if db["groupassignments"]:
            st.json(db["groupassignments"], expanded=False)

def get_enum_values():
    return {
        "school_types": ["FS","FKLASS","FTH","OPPFTH","GR","GRS","TR","SP","SAM","GY","GYS","VUX","VUXSFI",
                         "VUXGR","VUXGY","VUXSARGR","VUXSARTR","VUXSARGY","SFI","SARVUX","SARVUXGR",
                         "SARVUXGY","KU","YH","FHS","STF","KKU","HS","ABU","AU"],
        "sex_types": ["Man","Kvinna","Okänt"],
        "duty_roles": ["Rektor","Lärare","Förskollärare","Barnskötare","Bibliotekarie","Lärarassistent",
                       "Fritidspedagog","Annan personal","Studie- och yrkesvägledare","Förstelärare","Kurator",
                       "Skolsköterska","Skolläkare","Skolpsykolog","Speciallärare/specialpedagog",
                       "Skoladministratör","Övrig arbetsledning","Övrig pedagogisk personal","Förskolechef"],
        "person_relation_types": ["Vårdnadshavare","Annan ansvarig","God man","Utsedd behörig"],
        "group_types": ["Undervisning","Klass","Mentor","Provgrupp","Schema","Avdelning","Personalgrupp","Övrigt"],
        "assignment_roles": ["Mentor","Förskollärare","Barnskötare","Fritidspedagog","Specialpedagog",
                             "Elevhälsopersonal","Pedagogisk ledare","Schemaläggare","Lärarassistent","Administrativ personal"],
        "activity_types": ["Undervisning","Elevaktivitet","Provaktivitet","Läraraktivitet","Övrigt"]
    }

def show_db_map():
    st.subheader("SS12000 Databasstruktur")

    dot = Digraph(comment='SS12000 Database', format='png')
    dot.attr(rankdir='LR', bgcolor='#222222', fontcolor='white')
    dot.attr('node', shape='record', style='filled', fillcolor='#1f78b4', fontcolor='white', fontsize='12')
    dot.attr('edge', color='white', fontsize='10')

    # Definiera tabeller med kolumner
    dot.node('Organisations', '{Organisations|OrganisationId\\lDisplayName\\lSchoolTypes\\lSchoolUnitCode\\l}')
    dot.node('Persons', '{Persons|PersonId\\lGivenName\\lFamilyName\\lSex\\l}')
    dot.node('Enrolments', '{Enrolments|EnrolmentId\\lOrganisationId\\lPersonId\\lSchoolYear\\l}')
    dot.node('Duties', '{Duties|DutyId\\lPersonId\\lOrganisationId\\lDutyRole\\l}')
    dot.node('AssignmentRoles', '{AssignmentRoles|AssignmentRoleId\\lDutyId\\lGroupId\\lAssignmentRole\\l}')
    dot.node('Groups', '{Groups|GroupId\\lDisplayName\\lGroupType\\lSchoolType\\l}')
    dot.node('GroupMemberships', '{GroupMemberships|GroupMembershipId\\lPersonId\\lGroupId\\l}')
    dot.node('Activities', '{Activities|ActivityId\\lDisplayName\\lActivityType\\lOrganisationId\\l}')
    dot.node('DutyAssignments', '{DutyAssignments|DutyAssignmentId\\lDutyId\\lActivityId\\l}')
    dot.node('GroupAssignments', '{GroupAssignments|GroupAssignmentId\\lGroupId\\lActivityId\\l}')

    # Relationspilar
    dot.edge('Organisations', 'Enrolments', label='OrganisationId')
    dot.edge('Persons', 'Enrolments', label='PersonId')

    dot.edge('Organisations', 'Duties', label='OrganisationId')
    dot.edge('Persons', 'Duties', label='PersonId')

    dot.edge('Duties', 'AssignmentRoles', label='DutyId')
    dot.edge('Groups', 'AssignmentRoles', label='GroupId')

    dot.edge('Activities', 'DutyAssignments', label='ActivityId')
    dot.edge('Duties', 'DutyAssignments', label='DutyId')

    dot.edge('Groups', 'GroupMemberships', label='GroupId')
    dot.edge('Persons', 'GroupMemberships', label='PersonId')

    dot.edge('Groups', 'GroupAssignments', label='GroupId')
    dot.edge('Activities', 'GroupAssignments', label='ActivityId')

    # Rendera i Streamlit
    st.graphviz_chart(dot)

def show_db_view(db):
    st.subheader("SS12000 Datavy")

    tabs = st.tabs(["Organisationer","Personer","Enrolments","Duties","Groups","Activities","Kopplingar"])

    with tabs[0]:  # Organisationer
        st.write("Lista över alla skolor/organisationer med ID, namn, typ och start/slutdatum.")
        df = pd.DataFrame(db["organisations"].values())
        st.dataframe(df)

    with tabs[1]:  # Personer
        st.write("Alla personer i systemet – elever och personal med namn, personnummer, e-post etc.")
        df = pd.DataFrame(db["persons"].values())
        st.dataframe(df)

    with tabs[2]:  # Enrolments
        st.write("Elevplaceringar i organisationer, med skolår och start-/slutdatum.")
        df = pd.DataFrame(db["enrolments"].values())
        st.dataframe(df)

    with tabs[3]:  # Duties
        st.write("Personalens uppdrag/roller på organisationer, t.ex. Lärare eller Rektor.")
        df = pd.DataFrame(db["duties"].values())
        st.dataframe(df)

    with tabs[4]:  # Groups
        st.write("Organisationens grupper, t.ex. klasser, mentorgrupper eller undervisningsgrupper.")
        df = pd.DataFrame(db["groups"].values())
        st.dataframe(df)

    with tabs[5]:  # Activities
        st.write("Aktiviteter som undervisning eller andra uppdrag kopplade till grupper och lärare.")
        df = pd.DataFrame(db["activities"].values())
        st.dataframe(df)

    with tabs[6]:  # Kopplingar
        st.write("Kopplingar mellan personer, grupper och aktiviteter:")
        
        st.subheader("GroupMemberships")
        st.write("Elevmedlemskap i grupper (klass/undervisning).")
        df = pd.DataFrame(db["groupmemberships"].values())
        st.dataframe(df)

        st.subheader("AssignmentRoles")
        st.write("Personalroller i organisatoriska grupper, t.ex.klass, mentorsgrupp.")
        df = pd.DataFrame(db["assignmentroles"].values())
        st.dataframe(df)

        st.subheader("DutyAssignments")
        st.write("Koppling mellan personal och aktiviteter de ansvarar för i aktivitetsgrupper (t.ex. undervisning).")
        df = pd.DataFrame(db["dutyassignments"].values())
        st.dataframe(df)

        st.subheader("GroupAssignments")
        st.write("Koppling mellan grupper och aktiviteter.")
        df = pd.DataFrame(db["groupassignments"].values())
        st.dataframe(df)

def initiate():
    st.set_page_config(layout="wide") 

    # Init session_state
    if "page" not in st.session_state:
        st.session_state.page = "Hem"
    
    if "db" not in st.session_state:
        st.session_state["db"] = {k:{} for k in ["organisations","persons","enrolments","duties","personrelations",
                        "groups","groupmemberships","assignmentroles","activities","groupassignments","dutyassignments","syllabus"]}
        db = st.session_state.db

    db = st.session_state.db
    return db

def load_ui_sidebar_menu():
    # --- Sidebar meny ---
    with st.sidebar:
        st.markdown("")
        selected = option_menu(
            menu_title=None,
            options=["Hem", "Organisation", "Personer", "Inskrivningar", "Anställningar", "Grupper","Föräldrar","Generera data","JSON", "Export", "Import"],
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

def load_ui_dashboard_counters(db):
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



