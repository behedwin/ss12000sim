import streamlit as st
from graphviz import Digraph
import pandas as pd
from util import today, gen_id

def load_ui_title():
    st.title("SS12000 Simulering")

def load_ui_button_loadExampledata(db):
    if st.button("Fyll med exempeldata"):
        load_data(db)

def load_ui_viewMode():
    view_mode = st.radio("Välj vy:", ["Redigera / Exempeldata", "Visa DB", "Visa DB-struktur"])
    return view_mode

def load_print_json_section(db):
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

    #PRINT GROUP JSON
    st.subheader("Groups")
    if db["groups"]:
        st.json(db["groups"], expanded=False)

    #PRINT ACTIVITIES JSON
    st.subheader("Activities")
    if db["activities"]:
        st.json(db["activities"], expanded=False)


    # ----------------------------
    # Visa automatiska kopplingar
    # ----------------------------
    st.subheader("AssignmentRoles (automatiska)")
    if db["assignmentroles"]:
        st.json(db["assignmentroles"], expanded=False)

    st.subheader("DutyAssignments (automatiska)")
    if db["dutyassignments"]:
        st.json(db["dutyassignments"], expanded=False)

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

def load_data(db):
        # ----- Organisationer -----
        org1 = gen_id()
        org2 = gen_id()
        db["organisations"][org1] = {"OrganisationId":org1,"DisplayName":"Demo Skola 1","SchoolTypes":["GR"],"StartDate":today(),"EndDate":None,"SchoolUnitCode":"DS01","ShortName":"DS1"}
        db["organisations"][org2] = {"OrganisationId":org2,"DisplayName":"Demo Skola 2","SchoolTypes":["GR"],"StartDate":today(),"EndDate":None,"SchoolUnitCode":"DS02","ShortName":"DS2"}

        # ----- Personer -----
        p1 = gen_id(); p2 = gen_id(); p3 = gen_id(); p4 = gen_id()
        db["persons"][p1] = {"PersonId":p1,"GivenName":"Anna","FamilyName":"Andersson","MiddleName":"","CivicNo":"201001010001","BirthDate":"2010-01-01","Sex":"Kvinna","StudentEmail":"","StaffEmail":"","PersonalEmail":"","StudentEduPersonPrincipalName":"anna.a@student.demo.se","StaffEduPersonPrincipalName":""}
        db["persons"][p2] = {"PersonId":p2,"GivenName":"Björn","FamilyName":"Berg","MiddleName":"","CivicNo":"201001020002","BirthDate":"2010-01-02","Sex":"Man","StudentEmail":"","StaffEmail":"","PersonalEmail":"","StudentEduPersonPrincipalName":"bjorn.b@student.demo.se","StaffEduPersonPrincipalName":""}
        db["persons"][p3] = {"PersonId":p3,"GivenName":"Carina","FamilyName":"Carlsson","MiddleName":"","CivicNo":"198001010003","BirthDate":"1980-01-01","Sex":"Kvinna","StudentEmail":"","StaffEmail":"carina.c@demo.se","PersonalEmail":"","StudentEduPersonPrincipalName":"","StaffEduPersonPrincipalName":"carina.c@edu.demo.se"}
        db["persons"][p4] = {"PersonId":p4,"GivenName":"David","FamilyName":"Dahl","MiddleName":"","CivicNo":"198001020004","BirthDate":"1980-01-02","Sex":"Man","StudentEmail":"","StaffEmail":"david.d@demo.se","PersonalEmail":"","StudentEduPersonPrincipalName":"","StaffEduPersonPrincipalName":"david.d@edu.demo.se"}

        # ----- Enrolments (elever) -----
        e1 = gen_id(); e2 = gen_id()
        db["enrolments"][e1] = {"EnrolmentId":e1,"OrganisationId":org1,"PersonId":p1,"SchoolType":"GR","StartDate":today(),"EndDate":None,"SchoolYear":"7"}
        db["enrolments"][e2] = {"EnrolmentId":e2,"OrganisationId":org1,"PersonId":p2,"SchoolType":"GR","StartDate":today(),"EndDate":None,"SchoolYear":"7"}

        # ----- Klass -----
        klass_id = gen_id()
        db["groups"][klass_id] = {"GroupId":klass_id,"OrganisationId":org1,"DisplayName":"Klass 7A","GroupType":"Klass","SchoolType":"GR","StartDate":today(),"EndDate":None}
        for p in [p1,p2]:
            gm_id = gen_id()
            db["groupmemberships"][gm_id] = {"GroupMembershipId":gm_id,"PersonId":p,"GroupId":klass_id,"StartDate":today(),"EndDate":None}

        # ----- Undervisningsgrupper -----
        ug1 = gen_id(); ug2 = gen_id()
        db["groups"][ug1] = {"GroupId":ug1,"OrganisationId":org1,"DisplayName":"Matematik 7A","GroupType":"Undervisning","SchoolType":"GR","StartDate":today(),"EndDate":None}
        db["groups"][ug2] = {"GroupId":ug2,"OrganisationId":org1,"DisplayName":"Engelska 7A","GroupType":"Undervisning","SchoolType":"GR","StartDate":today(),"EndDate":None}
        for ug in [ug1,ug2]:
            for p in [p1,p2]:
                gm_id = gen_id()
                db["groupmemberships"][gm_id] = {"GroupMembershipId":gm_id,"PersonId":p,"GroupId":ug,"StartDate":today(),"EndDate":None}

        # ----- Duties (personal) -----
        for duty_person, role in [(p3,"Lärare"),(p4,"Lärare")]:
            duty_id = gen_id()
            db["duties"][duty_id] = {
                "DutyId": duty_id,
                "PersonId": duty_person,
                "OrganisationId": org1,
                "StartDate": today(),
                "EndDate": None,
                "DutyRole": role,
                "Signature": "auto-sign"
            }

        # ----- Klassgrupp: Lärare som Mentor -----
        klass_group_id = klass_id  # Klass 7A
        for duty_person, role in [(p3,"Lärare"),(p4,"Lärare")]:
            duty_id = next(d["DutyId"] for d in db["duties"].values() if d["PersonId"] == duty_person)
            ar_id = gen_id()
            db["assignmentroles"][ar_id] = {
                "AssignmentRoleId": ar_id,
                "DutyId": duty_id,
                "GroupId": klass_group_id,
                "AssignmentRole": "Mentor",
                "StartDate": today(),
                "EndDate": None
            }

        # ----- Undervisningsgrupper (rätt) -----
        for g_id in [ug1, ug2]:
            group = db["groups"][g_id]

            # Skapa EN aktivitet per grupp
            act_id = gen_id()
            db["activities"][act_id] = {
                "ActivityId": act_id,
                "DisplayName": f"Auto-{group['DisplayName']}",
                "ActivityType": "Undervisning",
                "OrganisationId": org1,
                "SyllabusId": "",
                "SyllabusSchoolType": "GR",
                "SyllabusSubjectName": group['DisplayName'],
                "StartDate": today(),
                "EndDate": None,
                "SyllabusSubjectDesignation": "",
                "SyllabusCourseCode": "",
                "SyllabusCourseName": ""
            }

            # Koppla alla lärare till aktiviteten
            for duty_person in [p3, p4]:
                duty_id = next(d["DutyId"] for d in db["duties"].values() if d["PersonId"] == duty_person)
                da_id = gen_id()
                db["dutyassignments"][da_id] = {
                    "DutyAssignmentId": da_id,
                    "DutyId": duty_id,
                    "ActivityId": act_id,
                    "StartDate": today(),
                    "EndDate": None
                }

            # Koppla gruppen till aktiviteten
            ga_id = gen_id()
            db["groupassignments"][ga_id] = {
                "GroupAssignmentId": ga_id,
                "GroupId": g_id,
                "ActivityId": act_id,
                "StartDate": today(),
                "EndDate": None
            }
