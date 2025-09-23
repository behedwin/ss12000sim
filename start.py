import streamlit as st
from ui.comon import initiate,load_ui_sidebar_menu ,show_db_map,show_db_view,get_enum_values, load_ui_viewMode, load_print_json_section,load_ui_dashboard_counters
from ui.org import load_ui_organisation_form, load_ui_organisation_table
from ui.person import load_ui_person_form,load_ui_person_table
from ui.duty import load_ui_duty_form,load_ui_duty_table
from ui.enrolment import load_ui_enrolment_form, load_ui_enrolment_table
from ui.group import load_ui_groupManagement_form,load_ui_groupManagment_table
from ui.export import load_export_section
from ui.personrelation import load_ui_personrelation_form,load_ui_personrelation_table
from ui.importdata import load_import_section
from ui.gen_data import load_ui_gendata

def main():
    db = initiate()
    enums = get_enum_values()
    school_types = enums["school_types"]
    sex_types = enums["sex_types"]
    duty_roles = enums["duty_roles"]
    person_relation_types = enums["person_relation_types"]
    group_types = enums["group_types"]
    assignment_roles = enums["assignment_roles"]
    activity_types = enums["activity_types"]
    load_ui_sidebar_menu()  

    # --- Innehåll per sida ---
    if st.session_state.page == "Hem":
        st.title("Hem")
        load_ui_dashboard_counters(db)

    elif st.session_state.page == "Organisation":
        load_ui_organisation_form(db, school_types)
        load_ui_organisation_table(db)

    elif st.session_state.page == "Personer":
        load_ui_person_form(db, sex_types)
        load_ui_person_table(db)
    
    elif st.session_state.page == "Föräldrar":
        load_ui_personrelation_form(db, person_relation_types)
        load_ui_personrelation_table(db)

    elif st.session_state.page == "Inskrivningar":
        load_ui_enrolment_form(db, school_types)
        load_ui_enrolment_table(db)
    
    elif st.session_state.page == "Anställningar":
        load_ui_duty_form(db, duty_roles)
        load_ui_duty_table(db)

    elif st.session_state.page == "Grupper":
        load_ui_groupManagement_form(db, group_types,school_types,activity_types)
        st.write("")
        load_ui_groupManagment_table(db)


    elif st.session_state.page == "Export":
        load_export_section(db)

    elif st.session_state.page == "Import":
        load_import_section(db)

    elif st.session_state.page == "JSON":
        load_print_json_section(db)

    elif st.session_state.page == "Generera data":
        load_ui_gendata(db)


if __name__ == "__main__":
    main()
