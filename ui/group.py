import streamlit as st
from util import gen_id
from util import today
import pandas as pd

def load_ui_groupManagement_form(db, group_types, school_types,activity_types):
    # Organisatoriska grupper → Klass
    klass_types = ["Klass", "Mentor", "Avdelning", "Personalgrupp", "Övrigt"]

    # Aktivitetsgrupper → Undervisning
    undervisning_types = ["Undervisning", "Provgrupp", "Schema", "ExtraAktivitet"]

    # ----------------------------
    # Groups
    # ----------------------------
    org_list = list(db["organisations"].keys())

    st.subheader("Groups")
    with st.expander("Skapa grupp"):
        if not org_list:
            st.info("Ingen organisation tillgänglig")
        else:
            g_org = st.selectbox(
                "Organisation",
                list(db["organisations"].keys()),
                format_func=lambda x: db["organisations"][x]["DisplayName"],
                key="g_org"
            )
            g_name = st.text_input("DisplayName", key="g_name")
            g_type = st.selectbox("GroupType", group_types, key="g_type")
            g_school = st.selectbox("SchoolType", school_types, key="g_school")
            g_start = st.date_input("StartDate", key="g_start")
            g_end = st.date_input("EndDate", key="g_end")

            selected_syllabus_id = None
            selected_activity_type = None
            if g_type in undervisning_types:
                syllabus_list = list(db["syllabus"].keys())
                if syllabus_list:
                    def syllabus_label(sid):
                        s = db["syllabus"][sid]
                        if s.get("SyllabusSubjectDesignation"):
                            return f"Ämne: {s['DisplayName']}"
                        else:
                            return f"Kurs: {s['DisplayName']}"
                    
                    selected_syllabus_id = st.selectbox(
                        "Välj syllabus",
                        syllabus_list,
                        format_func=syllabus_label,
                        key="g_syllabus"
                    )

                    selected_activity_type = st.selectbox(
                        "Välj aktivitetstyp",
                        activity_types,
                        #format_func=activity_types,
                        key="a_activity_type"
                    )

                else:
                    st.info("Ingen syllabus definierad")

            if st.button("Lägg till grupp", key="btn_add_group"):
                new_id = gen_id()
                db["groups"][new_id] = {
                    "GroupId": new_id,
                    "OrganisationId": g_org,
                    "DisplayName": g_name,
                    "GroupType": g_type,
                    "SchoolType": g_school,
                    "StartDate": g_start.isoformat(),
                    "EndDate": g_end.isoformat() if g_end else None
                }

                syllabus_data = db["syllabus"].get(selected_syllabus_id, {}) if selected_syllabus_id else {}

                # Skapa aktivitet direkt om det är en undervisningsgrupp
                if g_type in undervisning_types:
                    act_id = gen_id()
                    db["activities"][act_id] = {
                        "ActivityId": act_id,
                        "DisplayName": g_name,
                        "ActivityType": selected_activity_type,
                        "OrganisationId": g_org,
                        "SyllabusId": selected_syllabus_id,
                        "SyllabusSchoolType": syllabus_data.get("SyllabusSchoolType", g_school),
                        "SyllabusSubjectName": syllabus_data.get("SyllabusSubjectName", g_name),
                        "StartDate": g_start.isoformat(),
                        "EndDate": g_end.isoformat() if g_end else None,
                        "SyllabusSubjectDesignation": syllabus_data.get("SyllabusSubjectDesignation"),
                        "SyllabusCourseCode": syllabus_data.get("SyllabusCourseCode"),
                        "SyllabusCourseName": syllabus_data.get("SyllabusCourseName")
                    }

                st.success(
                    "Grupp skapad" +
                    (" och aktivitet skapad" if g_type in undervisning_types else "")
                )

    # ----------------------------
    # Koppla person till Organisatorisk grupp (klass etc.)
    # ----------------------------
    group_list = list(db["groups"].keys())

    #st.subheader("Koppla person till organisatorisk grupp (Klass etc.)")
    with st.expander("Skapa organisatorisk grupps koppling"):
        if not group_list:
            st.info("Ingen grupp tillgänglig")
        else:
            klass_groups = [g for g in db["groups"].values() if g["GroupType"] in klass_types]
            if klass_groups:
                sel_group = st.selectbox(
                    "Välj klass",
                    [g["GroupId"] for g in klass_groups],
                    format_func=lambda x: db["groups"][x]["DisplayName"],
                    key="sel_class_group"
                )

                students = [e["PersonId"] for e in db["enrolments"].values()]
                staff = [d["PersonId"] for d in db["duties"].values()]
                selectable_persons = list(dict.fromkeys(students + staff))

                sel_person = st.selectbox(
                    "Välj person",
                    selectable_persons,
                    format_func=lambda x: f"{'Elev' if x in students else 'Personal'}: {db['persons'][x]['GivenName']} {db['persons'][x]['FamilyName']}",
                    key="sel_class_person"
                )

            # Förhandsvisning Klass
            preview_msgs = []
            sel_group = st.session_state.get("sel_class_group", None)
            sel_person = st.session_state.get("sel_class_person", None)
            if sel_group:  # eller if 'sel_group' in locals():
                group = db["groups"][sel_group]
                preview_msgs = []
                if sel_person in students:
                    preview_msgs.append(f"Elev → kopplas till GroupMembership i {group['DisplayName']}")
                if sel_person in staff:
                    if group["GroupType"] in klass_types:
                        preview_msgs.append(f"Personal → kopplas som AssignmentRole i {group['DisplayName']}")
                    elif group["GroupType"] in undervisning_types:
                        preview_msgs.append(f"Personal → kopplas som DutyAssignment i {group['DisplayName']}")


            if preview_msgs:
                st.info("\n".join(preview_msgs))

                if st.button("Koppla person till Klass", key=f"btn_class_{sel_person}_{sel_group}"):
                    if sel_person in students:
                        gm_exists = any(
                            gm for gm in db["groupmemberships"].values()
                            if gm["PersonId"] == sel_person and gm["GroupId"] == sel_group
                        )
                        if not gm_exists:
                            gm_id = gen_id()
                            db["groupmemberships"][gm_id] = {
                                "GroupMembershipId": gm_id,
                                "PersonId": sel_person,
                                "GroupId": sel_group,
                                "Role": "Elev",
                                "Status": "Aktiv",
                                "StartDate": today(),
                                "EndDate": None
                            }
                    if sel_person in staff:
                        duty_id = next((d["DutyId"] for d in db["duties"].values()
                                        if d["PersonId"] == sel_person and d["OrganisationId"] == db["groups"][sel_group]["OrganisationId"]), None)
                        if duty_id:
                            ar_exists = any(
                                ar for ar in db["assignmentroles"].values()
                                if ar["DutyId"] == duty_id and ar["GroupId"] == sel_group
                            )
                            if not ar_exists:
                                ar_id = gen_id()
                                db["assignmentroles"][ar_id] = {
                                    "AssignmentRoleId": ar_id,
                                    "DutyId": duty_id,
                                    "GroupId": sel_group,
                                    "AssignmentRole": "Mentor",
                                    "StartDate": today(),
                                    "EndDate": None
                                }
                    st.success("Person kopplad till Klass")

    # ----------------------------
    # Koppla person till aktivitetsgrupp (undervisningsgrupp etc.)
    # ----------------------------
    group_list = list(db["groups"].keys())

    #st.subheader("Koppla person till aktivitetsgrupp (Undervisning etc.)")
    with st.expander("Skapa aktivitetsgrupps koppling"):
        if not group_list:
            st.info("Ingen grupp tillgänglig")
        else:
            ug_groups = [g for g in db["groups"].values() if g["GroupType"] in undervisning_types]
            if ug_groups:
                sel_group = st.selectbox(
                    "Välj undervisningsgrupp",
                    [g["GroupId"] for g in ug_groups],
                    format_func=lambda x: db["groups"][x]["DisplayName"],
                    key="sel_ug_group"
                )

                sel_person = st.selectbox(
                    "Välj person",
                    selectable_persons,
                    format_func=lambda x: f"{'Elev' if x in students else 'Personal'}: {db['persons'][x]['GivenName']} {db['persons'][x]['FamilyName']}",
                    key="sel_ug_person"
                )

            # Förhandsvisning Undervisning
            preview_msgs = []  # alltid definierad
            sel_group = st.session_state.get("sel_ug_group", None)
            sel_person = st.session_state.get("sel_ug_person", None)
            if sel_group:  # eller if 'sel_group' in locals():
                group = db["groups"][sel_group]
                preview_msgs = []
                if sel_person in students:
                    preview_msgs.append(f"Elev → kopplas till GroupMembership i {group['DisplayName']}")
                if sel_person in staff:
                    if group["GroupType"] in klass_types:
                        preview_msgs.append(f"Personal → kopplas som AssignmentRole i {group['DisplayName']}")
                    elif group["GroupType"] in undervisning_types:
                        preview_msgs.append(f"Personal → kopplas som DutyAssignment i {group['DisplayName']}")


            if preview_msgs:
                st.info("\n".join(preview_msgs))


                if st.button("Koppla person till Undervisningsgrupp", key=f"btn_ug_{sel_person}_{sel_group}"):
                    if sel_person in students:
                        gm_exists = any(
                            gm for gm in db["groupmemberships"].values()
                            if gm["PersonId"] == sel_person and gm["GroupId"] == sel_group
                        )
                        if not gm_exists:
                            gm_id = gen_id()
                            db["groupmemberships"][gm_id] = {
                                "GroupMembershipId": gm_id,
                                "PersonId": sel_person,
                                "GroupId": sel_group,
                                "Role": "Elev",
                                "Status": "Aktiv",
                                "StartDate": today(),
                                "EndDate": None
                            }
                    if sel_person in staff:
                        duty_id = next((d["DutyId"] for d in db["duties"].values()
                                        if d["PersonId"] == sel_person and d["OrganisationId"] == db["groups"][sel_group]["OrganisationId"]), None)
                        if duty_id:
                            act_id = next((a["ActivityId"] for a in db["activities"].values()
                                        if a["SyllabusSubjectName"] == db["groups"][sel_group]["DisplayName"]), None)
                            if act_id:
                                da_exists = any(
                                    da for da in db["dutyassignments"].values()
                                    if da["DutyId"] == duty_id and da["ActivityId"] == act_id
                                )
                                if not da_exists:
                                    da_id = gen_id()
                                    db["dutyassignments"][da_id] = {
                                        "DutyAssignmentId": da_id,
                                        "DutyId": duty_id,
                                        "ActivityId": act_id,
                                        "StartDate": today(),
                                        "EndDate": None
                                    }
                    st.success("Person kopplad till Undervisningsgrupp")

def load_ui_groupManagment_table(db):
    with st.expander("Visa grupper"):
        st.write("Lista över alla grupper")
        df = pd.DataFrame(db["groups"].values())
        if "OrganisationId" in df.columns:
            df["OrganisationName"] = df["OrganisationId"].map(lambda oid: db["organisations"][oid]["DisplayName"] if oid in db["organisations"] else "")
        search = st.text_input("Sök grupp",key="searchgroups")
        if search:
            mask = df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)
            df = df[mask]
        st.dataframe(df)
    with st.expander("Visa aktiviteter"):
        st.write("Lista över aktiviteter")
        df = pd.DataFrame(db["activities"].values())
        if "OrganisationId" in df.columns:
            df["OrganisationName"] = df["OrganisationId"].map(lambda oid: db["organisations"][oid]["DisplayName"] if oid in db["organisations"] else "")
        search = st.text_input("Sök aktivitet",key="searchactivities")
        if search:
            mask = df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)
            df = df[mask]
        st.dataframe(df)
    with st.expander("Visa grupps koppling till aktivitet"):
        st.write("Lista över gruppers koppling till aktiviteter")
        df = pd.DataFrame(db["groupassignments"].values())
        if "GroupId" in df.columns:
            df["GroupName"] = df["GroupId"].map(lambda gid: db["groups"][gid]["DisplayName"] if gid in db["groups"] else "")
        if "ActivityId" in df.columns:
            df["ActivityName"] = df["ActivityId"].map(lambda aid: db["activities"][aid]["DisplayName"] if aid in db["activities"] else "")
        search = st.text_input("Sök groupassignments (grupp och aktivitets koppling)",key="groupassignments")
        if search:
            mask = df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)
            df = df[mask]
        st.dataframe(df)
    with st.expander("Visa elevers gruppkopplingar"):
        st.write("Lista över elever i grupper")
        df = pd.DataFrame(db["groupmemberships"].values())
        if "PersonId" in df.columns:
            df["PersonName"] = df["PersonId"].map(lambda pid: f"{db['persons'][pid]['GivenName']} {db['persons'][pid]['FamilyName']}" if pid in db["persons"] else "")
        if "GroupId" in df.columns:
            df["GroupName"] = df["GroupId"].map(lambda gid: db["groups"][gid]["DisplayName"] if gid in db["groups"] else "")
        search = st.text_input("Sök gruppmedlemskap (elever)",key="groupmemberships")
        if search:
            mask = df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)
            df = df[mask]
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
        search = st.text_input("Sök assignmentroles (personal i org-grupp)",key="searchassignmentroles")
        if search:
            mask = df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)
            df = df[mask]
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
        search = st.text_input("Sök dutyassignments (personal i aktivitetsgrupp)",key="searchdutyassignments")
        if search:
            mask = df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)
            df = df[mask]
        st.dataframe(df)










