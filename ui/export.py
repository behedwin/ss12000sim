import json
from io import StringIO
import streamlit as st
from util import export_csv

def load_export_section(db):
    #st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Exportera data")

    # ----- CSV -----
    st.markdown("**CSV Export**")
    csv_dfs = export_csv(db)

    cols = st.columns(4)
    for idx, (name, df) in enumerate(csv_dfs.items()):
        col = cols[idx % 4]
        with col:
            buf = StringIO()
            df.to_csv(buf, sep=';', index=False, quoting=1)
            st.download_button(f"{name}.csv", buf.getvalue(), f"{name}.csv", "text/csv")

    # ----- JSON -----
    st.markdown("**JSON Export**")
    json_buf = json.dumps(db, indent=4)
    st.download_button("All data JSON", json_buf, "export.json", "application/json")
