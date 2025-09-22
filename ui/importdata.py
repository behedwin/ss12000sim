import streamlit as st
import pandas as pd
from util import gen_id



def print_import_txt(table_columns):
    st.subheader("Krav för lyckad CSV-import")
    
    st.markdown("""
    **1. Alla filer måste finnas**  
    Du måste ladda upp **alla 12 CSV-filer** motsvarande dessa tabeller:  
    `organisations`, `persons`, `enrolments`, `duties`, `personrelations`, `groups`,  
    `groupmemberships`, `assignmentroles`, `activities`, `groupassignments`, `dutyassignments`
    """)
    
    st.markdown("**2. Obligatoriska kolumner per tabell**")
    for table, cols in table_columns.items():
        st.markdown(f"**{table}**: {', '.join(cols)}")

    st.markdown("""
    **3. Unika ID:n**  
    Följande kolumner måste ha unika värden:  
    - organisations -> OrganisationId  
    - persons -> PersonId  
    - enrolments -> EnrolmentId  
    - duties -> DutyId  
    - groups -> GroupId  
    - groupmemberships -> GroupMembershipId  
    - assignmentroles -> AssignmentRoleId  
    - activities -> ActivityId  
    - groupassignments -> GroupAssignmentId  
    - dutyassignments -> DutyAssignmentId  
    - personrelations har inget krav på unikt värde
    """)

    st.markdown("""
    **4. Tomma ID:n ej tillåtna**  
    Om en unik-ID kolumn saknar värde avbryts importen.
    
    **5. Ingen dubblett i unika ID:n**  
    Om samma ID förekommer mer än en gång i en fil stoppas importen.
    
    **6. CSV-format**  
    - Semikolon (`;`) som separator  
    - Textfält trimmas automatiskt (whitespace tas bort)
    """)

def load_import_section(db):

    # Alla obligatoriska kolumner per tabell
    required_columns = {
        "organisations": ["OrganisationId","DisplayName","SchoolTypes","StartDate","EndDate","SchoolUnitCode","ShortName"],
        "persons": ["PersonId","GivenName","FamilyName","MiddleName","CivicNo","BirthDate","Sex","StudentEmail","StaffEmail","PersonalEmail","StudentEduPersonPrincipalName","StaffEduPersonPrincipalName"],
        "enrolments": ["EnrolmentId","OrganisationId","PersonId","SchoolType","StartDate","EndDate","SchoolYear"],
        "duties": ["DutyId","PersonId","OrganisationId","StartDate","EndDate","DutyRole","Signature"],
        "personrelations": ["Responsible","ResponsibleFor","RelationType","StartDate","EndDate"],
        "groups": ["GroupId","OrganisationId","DisplayName","GroupType","SchoolType","StartDate","EndDate"],
        "groupmemberships": ["GroupMembershipId","PersonId","GroupId","StartDate","EndDate"],
        "assignmentroles": ["AssignmentRoleId","DutyId","GroupId","AssignmentRole","StartDate","EndDate"],
        "activities": ["ActivityId","DisplayName","ActivityType","OrganisationId","SyllabusId","SyllabusSchoolType","SyllabusSubjectName","StartDate","EndDate","SyllabusSubjectDesignation","SyllabusCourseCode","SyllabusCourseName"],
        "groupassignments": ["GroupAssignmentId","GroupId","ActivityId","StartDate","EndDate"],
        "dutyassignments": ["DutyAssignmentId","DutyId","ActivityId","StartDate","EndDate"]
    }

    # Kolumner som måste ha unikt värde
    req_unique_value = {
        "organisations": "OrganisationId",
        "persons": "PersonId",
        "enrolments": "EnrolmentId",
        "duties": "DutyId",
        "personrelations": None,  # Inga krav på unikt värde
        "groups": "GroupId",
        "groupmemberships": "GroupMembershipId",
        "assignmentroles": "AssignmentRoleId",
        "activities": "ActivityId",
        "groupassignments": "GroupAssignmentId",
        "dutyassignments": "DutyAssignmentId"
    }

    csv_tables = list(required_columns.keys())




    st.subheader("Importera CSV (strikt)")

    # --- Steg 1: Ladda upp filer ---
    files = st.file_uploader("Ladda upp alla CSV-filer", type="csv", accept_multiple_files=True)

    if st.button("Importera alla filer"):

        # --- Steg 2: Kontrollera att alla filer finns ---
        uploaded_table_names = [f.name.split(".")[0].lower() for f in files]
        missing_files = [t for t in csv_tables if t not in uploaded_table_names]
        if missing_files:
            st.error(f"Följande filer saknas: {', '.join(missing_files)}. Import avbruten!")
            return

        # --- Steg 3: Initiera ny DB som fylls ---
        new_db = {table: {} for table in csv_tables}

        # --- Steg 4: Gå igenom varje uppladdad fil ---
        for file in files:
            table_name = file.name.split(".")[0].lower()
            df = pd.read_csv(file, sep=";", dtype=str)

            # --- Steg 5: Kontrollera obligatoriska kolumner ---
            missing_cols = [col for col in required_columns[table_name] if col not in df.columns]
            if missing_cols:
                st.error(f"Filen {file.name} saknar kolumner: {', '.join(missing_cols)}. Import avbruten!")
                return

            # --- Steg 6: Gå igenom varje rad i filen ---
            for idx, row in df.iterrows():

                # --- Ta bort whitespace ---
                row = row.apply(lambda x: x.strip() if isinstance(x, str) else x)

                # --- Steg 6a: Kontrollera att ID-kolumn har värde ---
                id_col = req_unique_value.get(table_name)
                if id_col and (pd.isna(row[id_col]) or row[id_col] == ""):
                    st.error(f"Filen {file.name} har tomt värde i unik ID-kolumn '{id_col}' (rad {idx+2}). Import avbruten!")
                    return

                # --- Steg 6b: Kontrollera unikt ID om definierat ---
                id_col = req_unique_value[table_name]
                if id_col:
                    obj_id = row[id_col]
                    if obj_id in new_db[table_name]:
                        st.error(f"Filen {file.name} har icke-unikt värde i '{id_col}' ({obj_id}). Import avbruten!")
                        return
                else:
                    # Ingen unik ID-kolumn, skapa intern nyckel (påverkar ej datan)
                    obj_id = f"row_{idx}"

                # --- Steg 6c: Fyll ny DB ---
                new_db[table_name][obj_id] = row.to_dict()

        # --- Steg 7: Uppdatera session_state med ny DB ---
        st.session_state["db"] = new_db
        st.success("Alla filer importerade korrekt!")

    print_import_txt(required_columns)