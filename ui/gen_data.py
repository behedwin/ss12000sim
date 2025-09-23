import streamlit as st
from util import today, gen_id
from gen import main as gen_data_main

def load_ui_button_loadExampledata(db):
    if st.button("Fyll med exempeldata"):
        load_data(db)

def load_ui_button_loadExampledata_v2(db):
    if st.button("Fyll med exempeldata"):
        gen_data_main(db)
    
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

def load_ui_gendata(db):
    with st.expander("Generera exempeldata", expanded=True):
        st.write("Ange parametrar för demo-data")
        with st.form("gendata_form"):
            num_orgs = st.number_input("Antal organisationer", min_value=1, value=3, max_value=90)
            num_persons_per_org = st.number_input("Antal personer per organisation", min_value=1, value=20, max_value=3000)
            num_enrolments_per_org = st.number_input("Antal elever per organisation", min_value=1, value=10, max_value=3000)
            num_duties_per_org = st.number_input("Antal personal/duties per organisation", min_value=1, value=10, max_value=3000)
            num_classes_per_org = st.number_input("Antal klasser per organisation", min_value=1, value=5)
            num_teaching_groups_per_org = st.number_input("Antal undervisningsgrupper per organisation", min_value=1, value=5)
            students_per_group = st.number_input("Elever per grupp", min_value=1, value=5)
            teachers_per_group = st.number_input("Lärare per grupp", min_value=1, value=1)
            
            submitted = st.form_submit_button("Generera data")
            
            if submitted:
                st.session_state.gendata_params = {
                    "num_orgs": num_orgs,
                    "num_persons_per_org": num_persons_per_org,
                    "num_enrolments_per_org": num_enrolments_per_org,
                    "num_duties_per_org": num_duties_per_org,
                    "num_classes_per_org": num_classes_per_org,
                    "num_teaching_groups_per_org": num_teaching_groups_per_org,
                    "students_per_group": students_per_group,
                    "teachers_per_group": teachers_per_group
                }
                st.success("Parametrar sparade!")

                gen_data_main(db,num_orgs,num_persons_per_org,num_enrolments_per_org,num_duties_per_org,num_classes_per_org,num_teaching_groups_per_org,students_per_group,teachers_per_group)



