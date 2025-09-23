import uuid
import csv
import random
from datetime import date, timedelta

# ---------------------
# Hjälpfunktioner
# ---------------------
def gen_id():
    return str(uuid.uuid4())

def today():
    return date.today().isoformat()

def random_birthdate(start_year, end_year):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).isoformat()

def write_csv(filename,header,rows):
    with open(filename,"w",newline="",encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

def load_generated_data_to_db(db,
    organisations, persons, duties, enrolments, groups, groupmemberships,
    syllabus, activities, dutyassignments, groupassignments, assignmentroles
):
    # Säkerställ att alla nycklar finns
    for key in ["organisations","persons","duties","enrolments","groups","groupmemberships",
                "syllabus","activities","dutyassignments","groupassignments","assignmentroles"]:
        if key not in db:
            db[key] = {}

    for org in organisations:
        org_id, displayname, schooltype, start, end, unitcode, shortname = org
        db["organisations"][org_id] = {
            "OrganisationId": org_id,
            "DisplayName": displayname,
            "SchoolTypes": [schooltype],
            "StartDate": start,
            "EndDate": end,
            "SchoolUnitCode": unitcode,
            "ShortName": shortname
        }

    for p in persons:
        pid, fname, lname, middle, civic, bdate, sex, student_email, staff_email, personal_email, edu_student, edu_staff = p
        db["persons"][pid] = {
            "PersonId": pid,
            "GivenName": fname,
            "FamilyName": lname,
            "MiddleName": middle,
            "CivicNo": civic,
            "BirthDate": bdate,
            "Sex": sex,
            "StudentEmail": student_email,
            "StaffEmail": staff_email,
            "PersonalEmail": personal_email,
            "StudentEduPersonPrincipalName": edu_student,
            "StaffEduPersonPrincipalName": edu_staff
        }

    for d in duties:
        duty_id, person_id, org_id, start, end, role, sig = d
        db["duties"][duty_id] = {
            "DutyId": duty_id,
            "PersonId": person_id,
            "OrganisationId": org_id,
            "StartDate": start,
            "EndDate": end,
            "DutyRole": role,
            "Signature": sig
        }

    for e in enrolments:
        eid, org_id, pid, stype, start, end, year = e
        db["enrolments"][eid] = {
            "EnrolmentId": eid,
            "OrganisationId": org_id,
            "PersonId": pid,
            "SchoolType": stype,
            "StartDate": start,
            "EndDate": end,
            "SchoolYear": year
        }

    for g in groups:
        gid, org_id, display, gtype, stype, start, end = g
        db["groups"][gid] = {
            "GroupId": gid,
            "OrganisationId": org_id,
            "DisplayName": display,
            "GroupType": gtype,
            "SchoolType": stype,
            "StartDate": start,
            "EndDate": end
        }

    for gm in groupmemberships:
        gmid, pid, gid, start, end = gm
        db["groupmemberships"][gmid] = {
            "GroupMembershipId": gmid,
            "PersonId": pid,
            "GroupId": gid,
            "StartDate": start,
            "EndDate": end
        }

    for s in syllabus:
        sid, display, stype, subj, code, cname, course, start, end = s
        db["syllabus"][sid] = {
            "SyllabusId": sid,
            "DisplayName": display,
            "SyllabusSchoolType": stype,
            "SyllabusSubjectName": subj,
            "SyllabusSubjectDesignation": code,
            "SyllabusCourseCode": cname,
            "SyllabusCourseName": course,
            "StartDate": start,
            "EndDate": end
        }

    for a in activities:
        act_id, display, atype, org_id, sid, stype, subj, start, end, des, code = a
        db["activities"][act_id] = {
            "ActivityId": act_id,
            "DisplayName": display,
            "ActivityType": atype,
            "OrganisationId": org_id,
            "SyllabusId": sid,
            "SyllabusSchoolType": stype,
            "SyllabusSubjectName": subj,
            "StartDate": start,
            "EndDate": end,
            "SyllabusSubjectDesignation": des,
            "SyllabusCourseCode": code,
            "SyllabusCourseName": ""
        }

    for da in dutyassignments:
        da_id, duty_id, act_id, start, end = da
        db["dutyassignments"][da_id] = {
            "DutyAssignmentId": da_id,
            "DutyId": duty_id,
            "ActivityId": act_id,
            "StartDate": start,
            "EndDate": end
        }

    for ga in groupassignments:
        ga_id, gid, act_id, start, end = ga
        db["groupassignments"][ga_id] = {
            "GroupAssignmentId": ga_id,
            "GroupId": gid,
            "ActivityId": act_id,
            "StartDate": start,
            "EndDate": end
        }

    for ar in assignmentroles:
        ar_id, duty_id, gid, role, start, end = ar
        db["assignmentroles"][ar_id] = {
            "AssignmentRoleId": ar_id,
            "DutyId": duty_id,
            "GroupId": gid,
            "AssignmentRole": role,
            "StartDate": start,
            "EndDate": end
        }   

def print_to_csv(organisations, persons, duties, enrolments, groups, groupmemberships, syllabus, activities, dutyassignments, groupassignments, assignmentroles):
    # ---------------------
    # Export
    # ---------------------
    write_csv("organisations.csv",["OrganisationId","DisplayName","SchoolTypes","StartDate","EndDate","SchoolUnitCode","ShortName"],organisations)
    write_csv("persons.csv",["PersonId","GivenName","FamilyName","MiddleName","CivicNo","BirthDate","Sex",
                            "StudentEmail","StaffEmail","PersonalEmail","StudentEduPersonPrincipalName","StaffEduPersonPrincipalName"],persons)
    write_csv("duties.csv",["DutyId","PersonId","OrganisationId","StartDate","EndDate","DutyRole","Signature"],duties)
    write_csv("enrolments.csv",["EnrolmentId","OrganisationId","PersonId","SchoolType","StartDate","EndDate","SchoolYear"],enrolments)
    write_csv("groups.csv",["GroupId","OrganisationId","DisplayName","GroupType","SchoolType","StartDate","EndDate"],groups)
    write_csv("groupmemberships.csv",["GroupMembershipId","PersonId","GroupId","StartDate","EndDate"],groupmemberships)
    write_csv("syllabus.csv",["SyllabusId","DisplayName","SyllabusSchoolType","SyllabusSubjectName","SyllabusSubjectDesignation","SyllabusCourseCode","SyllabusCourseName","StartDate","EndDate"],syllabus)
    write_csv("activities.csv",["ActivityId","DisplayName","ActivityType","OrganisationId","SyllabusId","SyllabusSchoolType","SyllabusSubjectName","StartDate","EndDate","SyllabusSubjectDesignation","SyllabusCourseCode","SyllabusCourseName"],activities)
    write_csv("dutyassignments.csv",["DutyAssignmentId","DutyId","ActivityId","StartDate","EndDate"],dutyassignments)
    write_csv("groupassignments.csv",["GroupAssignmentId","GroupId","ActivityId","StartDate","EndDate"],groupassignments)
    write_csv("assignmentroles.csv",["AssignmentRoleId","DutyId","GroupId","AssignmentRole","StartDate","EndDate"],assignmentroles)

first_names_female = [
    "Anna", "Carina", "Eva", "Maria", "Sara", "Lina", "Maja", "Karin", "Nina", "Elin",
    "Ida", "Johanna", "Lovisa", "Frida", "Camilla", "Malin", "Ulrika", "Helena", "Agnes", "Emelie",
    "Tove", "Sofia", "Matilda", "Josefin", "Mona", "Hanna", "Ebba", "Stina", "Elsa", "Felicia",
    "Gunilla", "Anette", "Susanne", "Therese", "Isabelle", "Jessica", "Amanda", "Paulina", "Rebecka", "Cecilia",
    "Ylva", "Astrid", "Ingrid", "Greta", "Saga", "Marta", "Lotta", "Annika", "Kristina", "Annelie",
    "Birgitta", "Caroline", "Clara", "Charlotta", "Linnea", "Alva", "Majken", "Sigrid", "Wilma", "Emilia",
    "Mira", "Alice", "Stella", "Tilda", "Ellen", "Filippa", "Vera", "Amelie", "Ronja", "Selma",
    "Moa", "Siv", "Rut", "Gunvor", "Helmi", "Lykke", "Inga", "Anja", "Lovina", "Malva",
    "Tuva", "Hedda", "Alma", "Freja", "Tyra", "Märta", "Hilde", "Irma", "Maj", "Britta"
]

first_names_male = [
    "Björn", "David", "Erik", "Lars", "Oskar", "Johan", "Karl", "Per", "Henrik", "Anders",
    "Magnus", "Fredrik", "Mattias", "Niklas", "Daniel", "Patrik", "Tomas", "Stefan", "Mikael", "Joakim",
    "Linus", "Pontus", "Marcus", "Simon", "Viktor", "Sebastian", "Alexander", "Christian", "Andreas", "Peter",
    "Göran", "Robert", "Jonas", "Rikard", "Thomas", "Håkan", "Arvid", "Filip", "Emil", "Oscar",
    "Gabriel", "Noah", "Isak", "Elias", "Theo", "Malte", "Albin", "Adam", "William", "Ludvig",
    "Rasmus", "Oliver", "Hugo", "Leon", "Ville", "Kevin", "Kalle", "Edvin", "Jonathan", "Melvin",
    "Samuel", "Joel", "Tobias", "Dennis", "Robin", "Olle", "Nils", "Sixten", "Alfred", "Benjamin",
    "Aron", "Vidar", "Jack", "Casper", "Milton", "Love", "Douglas", "Frank", "Ebbe", "Wilhelm",
    "Stig", "Tor", "Rune", "Bo", "Bernt", "Kent", "Rickard", "Urban", "Evert", "Bertil"
]

last_names = [
    "Andersson", "Berg", "Carlsson", "Dahl", "Ekström", "Forsberg", "Gustafsson", "Holm", "Isaksson", "Johansson",
    "Lind", "Magnusson", "Nyström", "Olofsson", "Pettersson", "Qvist", "Rydberg", "Sjöberg", "Törnqvist", "Uddén",
    "Viklund", "Wahlberg", "Åkesson", "Öberg", "Björk", "Claesson", "Dahlberg", "Eklund", "Falk", "Granlund",
    "Hellström", "Ivarsson", "Jansson", "Kron", "Lundgren", "Moberg", "Norberg", "Olsson", "Persson", "Sundberg",
    "Nyberg", "Boström", "Eliasson", "Hermansson", "Lindström", "Palm", "Sandberg", "Wallin", "Axelsson", "Holmqvist",
    "Backman", "Ek", "Fors", "Grönberg", "Hallberg", "Ingelsson", "Jernberg", "Kjellberg", "Lundin", "Marklund",
    "Norström", "Pålsson", "Rosén", "Strömberg", "Tideman", "Vestman", "Westin", "Åström", "Östlund", "Bäck",
    "Ahlgren", "Bergqvist", "Ceder", "Dufva", "Engström", "Flodin", "Gillberg", "Hammar", "Jonsson", "Kallin",
    "Lehmann", "Molander", "Nordling", "Oscarsson", "Petersson", "Quist", "Runesson", "Stenberg", "Tunberg", "Vesterlund"
]

syllabus_list = [
    ("Matematik 7", "MA001", "Matematik"),
    ("Engelska 7", "ENG001", "Engelska"),
    ("Svenska 7", "SV001", "Svenska"),
    ("Biologi 7", "BI001", "Biologi"),
    ("Kemi 7", "KE001", "Kemi"),
    ("Fysik 7", "FY001", "Fysik"),
    ("Historia 7", "HI001", "Historia"),
    ("Geografi 7", "GE001", "Geografi"),
    ("Musik 7", "MU001", "Musik"),
    ("Idrott 7", "ID001", "Idrott")
]

school_names = [
    "Solrosens Skola", "Granens Skola", "Björkens Skola", "Eklundsskolan", "Lindskolan",
    "Havsskolan", "Stjärnskolan", "Fjällskolan", "Ängsskolan", "Tallskolan",
    "Rosengårdsskolan", "Almgården", "Skogsskolan", "Sjöstjärnans Skola", "Bäckängsskolan",
    "Vasaskolan", "Södra Ängby", "Nordstjärnans Skola", "Frostskolan", "Solgläntan",
    "Lärkvägens Skola", "Blåsippan", "Månstrålen", "Stenskolan", "Ekenäs Skola",
    "Gläntan", "Vitsippan", "Änglamarksskolan", "Björkbacken", "Tallbo", 
    "Sjöängen", "Furuhäll", "Grönskolan", "Skogsgläntan", "Höjdens Skola",
    "Vårgläntan", "Sommarängen", "Höstlunden", "Vinterskolan", "Fjädermolnsskolan",
    "Ljusdalsskolan", "Kustskolan", "Bergskolan", "Älvskolan", "Stensjöskolan",
    "Solsidan Skola", "Nordviks Skola", "Sjöviksskolan", "Granliden", "Ekbacken",
    "Tallmon", "Fjällgläntan", "Ängsbacken", "Rosendalsskolan", "Skogslyckan",
    "Blåklintsskolan", "Solglimten", "Nordstigen", "Frostgläntan", "Lindbacken",
    "Myrängen", "Sjöstugan", "Hasselgården", "Vitsippan", "Granängen",
    "Ekliden", "Björkgården", "Tallängen", "Skogsstigen", "Sjölyckan",
    "Höjdängsskolan", "Solhöjden", "Stjärnbacken", "Fjällängen", "Ängsvägen",
    "Lärkängen", "Blåbärsskolan", "Månängen", "Rosenvägen", "Skogsbrynet",
    "Sjöängen", "Furugården", "Grönbacken", "Tallgläntan", "Ekängen",
    "Björkängen", "Solstrålen", "Nordgläntan", "Ängsbrynet", "Stjärnglansen"
]

def generate_demo_data(num_orgs, num_persons_per_org, num_enrolments_per_org, num_duties_per_org, num_classes_per_org, num_teaching_groups_per_org, students_per_group, teachers_per_group):


    # ---------------------
    # Initiera listor
    # ---------------------
    organisations = []
    persons = []
    duties = []
    enrolments = []
    groups = []
    groupmemberships = []
    syllabus = []
    activities = []
    dutyassignments = []
    groupassignments = []
    assignmentroles = []

    # ---------------------
    # Generera organisationer, personer och allt
    # ---------------------
    organisations = []
    selected_schools = random.sample(school_names, num_orgs)
    for i, name in enumerate(selected_schools, start=1):
        org_id = gen_id()
        organisations.append([org_id, name, "GR", today(), "", f"DS{i:02}", f"DS{i}"])
        
        org_students = []
        org_staff = []

        # --- Personer ---
        for i in range(num_persons_per_org):
            pid = gen_id()
            if i < num_enrolments_per_org:  # elever
                sex = random.choice(["Kvinna","Man"])
                fname = random.choice(first_names_female if sex=="Kvinna" else first_names_male)
                lname = random.choice(last_names)
                bdate = random_birthdate(2005,2015)
                persons.append([pid,fname,lname,"",f"2010{i:04}",bdate,sex,"","","",f"{fname.lower()}.{lname.lower()}@student.demo.se",""])
                org_students.append(pid)
            else:  # personal
                sex = random.choice(["Kvinna","Man"])
                fname = random.choice(first_names_female if sex=="Kvinna" else first_names_male)
                lname = random.choice(last_names)
                bdate = random_birthdate(1970,1990)
                persons.append([pid,fname,lname,"",f"1980{i:04}",bdate,sex,"",f"{fname.lower()}.{lname.lower()}@demo.se","","",f"{fname.lower()}.{lname.lower()}@edu.demo.se"])
                org_staff.append(pid)

        # --- Enrolments ---
        for sid in org_students[:num_enrolments_per_org]:
            eid = gen_id()
            enrolments.append([eid,org_id,sid,"GR",today(),"",str(random.randint(7,9))])

        # --- Duties ---
        for sid in org_staff[:num_duties_per_org]:
            did = gen_id()
            duties.append([did, sid, org_id, today(), "", "Lärare", "auto-sign"])
            
        # --- Syllabus ---
        syllabus = []
        for name, code, subj in syllabus_list:
            s_id = gen_id()
            syllabus.append([s_id, name, "GR", subj, code, "", "", today(), ""])


        # --- Klasser (Organisatoriska grupper) ---
        for k in range(1,num_classes_per_org+1):
            gid = gen_id()
            groups.append([gid,org_id,f"Klass {k}A","Klass","GR",today(),""])
            selected_students = random.sample(org_students,students_per_group)
            for sid in selected_students:
                gmid = gen_id()
                groupmemberships.append([gmid,sid,gid,today(),""])
            # Lärare som mentor
            mentor_id = random.choice([d[1] for d in duties if d[2] == org_id])
            duty_id = next(d[0] for d in duties if d[1] == mentor_id)
            ar_id = gen_id()
            assignmentroles.append([ar_id,duty_id,gid,"Mentor",today(),""])

        # --- När du skapar undervisningsgrupper ---
        for u in range(1, num_teaching_groups_per_org + 1):
            gid = gen_id()
            groups.append([gid, org_id, f"Undervisning {u}", "Undervisning", "GR", today(), ""])
            
            # Elever
            selected_students = random.sample(org_students, students_per_group)
            for sid in selected_students:
                gmid = gen_id()
                groupmemberships.append([gmid, sid, gid, today(), ""])
            
            # Slumpmässig syllabus
            s_id, name, _, subj, code, _, _, _, _ = random.choice(syllabus)
            
            # Aktivitet kopplat till syllabus
            act_id = gen_id()
            activities.append([act_id, name, "Undervisning", org_id, s_id, "GR", subj, today(), "", "", ""])
            
            # Lärare
            eligible_teachers = [d[1] for d in duties if d[2] == org_id]
            teacher = random.choice(eligible_teachers)
            t_duty_id = next(d[0] for d in duties if d[1] == teacher and d[2] == org_id)
            da_id = gen_id()
            dutyassignments.append([da_id, t_duty_id, act_id, today(), ""])
            
            # Koppla grupp till aktivitet
            ga_id = gen_id()
            groupassignments.append([ga_id, gid, act_id, today(), ""])


    return (organisations, persons, duties, enrolments, groups, groupmemberships, syllabus, activities, dutyassignments, groupassignments, assignmentroles)

def main(db,num_orgs,num_persons_per_org,num_enrolments_per_org,num_duties_per_org,num_classes_per_org,num_teaching_groups_per_org,students_per_group,teachers_per_group):
    organisations, persons, duties, enrolments, groups, groupmemberships, syllabus, activities, dutyassignments, groupassignments, assignmentroles = generate_demo_data(num_orgs,num_persons_per_org,num_enrolments_per_org,num_duties_per_org,num_classes_per_org,num_teaching_groups_per_org,students_per_group,teachers_per_group)
    
    load_generated_data_to_db(db,
        organisations, persons, duties, enrolments, groups, groupmemberships,
        syllabus, activities, dutyassignments, groupassignments, assignmentroles
    )

    #return db