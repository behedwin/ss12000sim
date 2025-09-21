import streamlit as st
from ui.comon import show_db_map,show_db_view,get_enum_values,load_ui_title, load_ui_button_loadExampledata, load_ui_viewMode, load_print_json_section
from ui.org import load_ui_organisation_form
from ui.person import load_ui_person_form
from ui.duty import load_ui_duty_form
from ui.enrolment import load_ui_enrolment_form
from ui.group import load_ui_groupManagement_form
from ui.export import load_export_section

def gui_main(db):
    enums = get_enum_values()
    school_types = enums["school_types"]
    sex_types = enums["sex_types"]
    duty_roles = enums["duty_roles"]
    person_relation_types = enums["person_relation_types"]
    group_types = enums["group_types"]
    assignment_roles = enums["assignment_roles"]
    activity_types = enums["activity_types"]

    load_ui_title()
    load_ui_button_loadExampledata(db)
    view_mode = load_ui_viewMode()

    if view_mode == "Visa DB":
        show_db_view(db)
    elif view_mode == "Visa DB-struktur":
        show_db_map()
    else:
        col1, col2 = st.columns([1,1])
        with col1:
            load_ui_organisation_form(db, school_types)
            load_ui_person_form(db, sex_types)
            load_ui_duty_form(db, duty_roles)
            load_ui_enrolment_form(db, school_types)
            load_ui_groupManagement_form(db, group_types, school_types)
        with col2:
            load_print_json_section(db)
        
        load_export_section(db)


