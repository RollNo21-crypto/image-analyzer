import streamlit as st
import sqlite3

def load_data():
    conn = sqlite3.connect("data.db")
    df = conn.execute("SELECT * FROM entries ORDER BY uploaded_at DESC").fetchall()
    conn.close()
    return df

st.title("📊 Uploaded Entries Dashboard")

data = load_data()
if data:
    for row in data:
        st.markdown("---")
        st.markdown(f"**Filename**: {row[1]}")
        st.markdown(f"**Description**: {row[2]}")
        st.markdown(f"**Image Caption**: {row[3]}")
        st.markdown(f"**Link**: {row[4]}")
        st.markdown(f"**Link Summary**: {row[5]}")
        st.markdown(f"**Categories**: {row[6]}")
        st.markdown(f"**Uploaded At**: {row[7]}")
else:
    st.info("No entries yet.")
