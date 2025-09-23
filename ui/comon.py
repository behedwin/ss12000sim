import streamlit as st
from graphviz import Digraph
import pandas as pd
from util import today, gen_id
from streamlit_option_menu import option_menu

def load_ui_title():
    st.title("SS12000 Simulering")

def load_ui_button_loadExampledata(db):
    if st.button("Fyll med exempeldata"):
        load_data(db)

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

def load_data_OLD(db):
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
        db["groups"][klass_id] = {
            "GroupId":klass_id,
            "OrganisationId":org1,
            "DisplayName":"Klass 7A",
            "GroupType":"Klass",
            "SchoolType":"GR",
            "StartDate":today(),
            "EndDate":None
            }
        for p in [p1,p2]:
            gm_id = gen_id()
            db["groupmemberships"][gm_id] = {
                "GroupMembershipId":gm_id,
                "PersonId":p,
                "GroupId":klass_id,
                "StartDate":today(),
                "EndDate":None
            }

        # ----- Syllabus -----
        # ----- Syllabus 1 -----
        syllabus1_id = gen_id()
        db["syllabus"][syllabus1_id] = {
            "SyllabusId": syllabus1_id,
            "DisplayName": "Matematik 7A",
            "SyllabusSchoolType": "GR",
            "SyllabusSubjectName": "Matematik",
            "SyllabusSubjectDesignation": "MA",
            "SyllabusCourseCode": "",
            "SyllabusCourseName": "",
            "StartDate": today(),
            "EndDate": None
        }

        # ----- Syllabus 2 -----
        syllabus2_id = gen_id()
        db["syllabus"][syllabus2_id] = {
            "SyllabusId": syllabus2_id,
            "DisplayName": "Engelska 7A",
            "SyllabusSchoolType": "GR",
            "SyllabusSubjectName": "Engelska A",
            "SyllabusSubjectDesignation": "",
            "SyllabusCourseCode": "ENGENG001",
            "SyllabusCourseName": "Engelska A",
            "StartDate": today(),
            "EndDate": None
        }


        # ----- Undervisningsgrupper -----
        ug1 = gen_id(); ug2 = gen_id()
        db["groups"][ug1] = {"GroupId":ug1,"OrganisationId":org1,"DisplayName":"Matematik 7A","GroupType":"Undervisning","SchoolType":"GR","StartDate":today(),"EndDate":None}
        db["groups"][ug2] = {"GroupId":ug2,"OrganisationId":org1,"DisplayName":"Engelska 7A","GroupType":"Undervisning","SchoolType":"GR","StartDate":today(),"EndDate":None}

        syllabus_map = {
            "Matematik 7A": syllabus1_id,
            "Engelska 7A": syllabus2_id
        }

        for ug in [ug1, ug2]:
            for p in [p1, p2]:
                gm_id = gen_id()
                db["groupmemberships"][gm_id] = {"GroupMembershipId":gm_id,"PersonId":p,"GroupId":ug,"StartDate":today(),"EndDate":None}

            # Skapa aktivitet kopplad till syllabus
            group = db["groups"][ug]
            syllabus_id = syllabus_map[group["DisplayName"]]
            syllabus_data = db["syllabus"][syllabus_id]

            act_id = gen_id()
            db["activities"][act_id] = {
                "ActivityId": act_id,
                "DisplayName": group["DisplayName"],
                "ActivityType": group["GroupType"],
                "OrganisationId": org1,
                "SyllabusId": syllabus_id,
                "SyllabusSchoolType": syllabus_data["SyllabusSchoolType"],
                "SyllabusSubjectName": syllabus_data["SyllabusSubjectName"],
                "StartDate": today(),
                "EndDate": None,
                "SyllabusSubjectDesignation": syllabus_data.get("SyllabusSubjectDesignation"),
                "SyllabusCourseCode": syllabus_data.get("SyllabusCourseCode"),
                "SyllabusCourseName": syllabus_data.get("SyllabusCourseName")
            }


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
        
            # ----- Personrelations -----
        for responsible, responsible_for in [(p1, p2), (p3, p4)]:
            rel_id = gen_id()
            db["personrelations"][rel_id] = {
                "Responsible": responsible,
                "ResponsibleFor": responsible_for,
                "RelationType": "Vårdnadshavare",
                "StartDate": today(),
                "EndDate": None
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

    # ----- Enrolments (elever) -----
    e1 = gen_id(); e2 = gen_id()
    db["enrolments"][e1] = {"EnrolmentId":e1,"OrganisationId":org1,"PersonId":p1,"SchoolType":"GR","StartDate":today(),"EndDate":None,"SchoolYear":"7"}
    db["enrolments"][e2] = {"EnrolmentId":e2,"OrganisationId":org1,"PersonId":p2,"SchoolType":"GR","StartDate":today(),"EndDate":None,"SchoolYear":"7"}

    # ----- Klass -----
    klass_id = gen_id()
    db["groups"][klass_id] = {
        "GroupId":klass_id,
        "OrganisationId":org1,
        "DisplayName":"Klass 7A",
        "GroupType":"Klass",
        "SchoolType":"GR",
        "StartDate":today(),
        "EndDate":None
    }
    for p in [p1, p2]:
        gm_id = gen_id()
        db["groupmemberships"][gm_id] = {
            "GroupMembershipId":gm_id,
            "PersonId":p,
            "GroupId":klass_id,
            "StartDate":today(),
            "EndDate":None
        }

    # ----- Syllabus -----
    syllabus1_id = gen_id()
    db["syllabus"][syllabus1_id] = {
        "SyllabusId": syllabus1_id,
        "DisplayName": "Matematik 7A",
        "SyllabusSchoolType": "GR",
        "SyllabusSubjectName": "Matematik",
        "SyllabusSubjectDesignation": "MA",
        "SyllabusCourseCode": "",
        "SyllabusCourseName": "",
        "StartDate": today(),
        "EndDate": None
    }

    syllabus2_id = gen_id()
    db["syllabus"][syllabus2_id] = {
        "SyllabusId": syllabus2_id,
        "DisplayName": "Engelska 7A",
        "SyllabusSchoolType": "GR",
        "SyllabusSubjectName": "Engelska A",
        "SyllabusSubjectDesignation": "",
        "SyllabusCourseCode": "ENGENG001",
        "SyllabusCourseName": "Engelska A",
        "StartDate": today(),
        "EndDate": None
    }

    # ----- Undervisningsgrupper -----
    ug1 = gen_id(); ug2 = gen_id()
    db["groups"][ug1] = {"GroupId":ug1,"OrganisationId":org1,"DisplayName":"Matematik 7A","GroupType":"Undervisning","SchoolType":"GR","StartDate":today(),"EndDate":None}
    db["groups"][ug2] = {"GroupId":ug2,"OrganisationId":org1,"DisplayName":"Engelska 7A","GroupType":"Undervisning","SchoolType":"GR","StartDate":today(),"EndDate":None}

    syllabus_map = {
        "Matematik 7A": syllabus1_id,
        "Engelska 7A": syllabus2_id
    }

    for ug in [ug1, ug2]:
        group = db["groups"][ug]

        # Koppla elever
        for p in [p1, p2]:
            gm_id = gen_id()
            db["groupmemberships"][gm_id] = {
                "GroupMembershipId": gm_id,
                "PersonId": p,
                "GroupId": ug,
                "StartDate": today(),
                "EndDate": None
            }

        # Skapa aktivitet kopplad till syllabus
        syllabus_id = syllabus_map[group["DisplayName"]]
        syllabus_data = db["syllabus"][syllabus_id]

        act_id = gen_id()
        db["activities"][act_id] = {
            "ActivityId": act_id,
            "DisplayName": group["DisplayName"],
            "ActivityType": "Undervisning",
            "OrganisationId": org1,
            "SyllabusId": syllabus_id,
            "SyllabusSchoolType": syllabus_data["SyllabusSchoolType"],
            "SyllabusSubjectName": syllabus_data["SyllabusSubjectName"],
            "StartDate": today(),
            "EndDate": None,
            "SyllabusSubjectDesignation": syllabus_data.get("SyllabusSubjectDesignation"),
            "SyllabusCourseCode": syllabus_data.get("SyllabusCourseCode"),
            "SyllabusCourseName": syllabus_data.get("SyllabusCourseName")
        }

        # Koppla lärare till aktiviteten
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
            "GroupId": ug,
            "ActivityId": act_id,
            "StartDate": today(),
            "EndDate": None
        }

    # ----- Personrelations -----
    for responsible, responsible_for in [(p1, p2), (p3, p4)]:
        rel_id = gen_id()
        db["personrelations"][rel_id] = {
            "Responsible": responsible,
            "ResponsibleFor": responsible_for,
            "RelationType": "Vårdnadshavare",
            "StartDate": today(),
            "EndDate": None
        }

    # ----- Klassgrupp: Lärare som Mentor -----
    for duty_person, role in [(p3,"Lärare"),(p4,"Lärare")]:
        duty_id = next(d["DutyId"] for d in db["duties"].values() if d["PersonId"] == duty_person)
        ar_id = gen_id()
        db["assignmentroles"][ar_id] = {
            "AssignmentRoleId": ar_id,
            "DutyId": duty_id,
            "GroupId": klass_id,
            "AssignmentRole": "Mentor",
            "StartDate": today(),
            "EndDate": None
        }

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



