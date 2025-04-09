import streamlit as st
import json
import os

# Load JSON Data
def load_data():
    json_file_path = r"D:\Service portal\knowledge portal\Mybell_Resolutions.json"
    if not os.path.exists(json_file_path):
        st.error("JSON file not found.")
        return []
    with open(json_file_path, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

# Set page config
st.set_page_config(layout="wide")

# --- Top Left Search ---
st.markdown("### 🔍 Search Issue")
query = st.text_input("Search", placeholder="Type keyword...", label_visibility="collapsed")
st.markdown("---")

if query:
    query = query.strip().lower()
    matched_issues = [issue for issue in data if query in issue["IssueName"].lower()]

    if matched_issues:
        for issue in matched_issues:
            col1, col2, col3 = st.columns([3, 4, 3])  # Adjust widths as needed

            with col1:
                st.markdown("### 📄 Result")
                st.markdown(f"`Issue:` {issue['IssueName']}")
                st.markdown(f"`Functionality:` {issue.get('Functionality', '')}")
                st.markdown(f"`Area:` {issue.get('Area', '')}")
                st.markdown(f"`LOB:` {issue.get('LOB', '')}")

            with col2:
                st.markdown("### 🎫 Related Tickets")
                for idx, res in enumerate(issue.get("Resolutions", [])):
                    st.markdown(f"- `INC-{1000 + idx}`: {res.get('DueTo', '')}")

            with col3:
                st.markdown("### ✅ Resolution")
                for res in issue.get("Resolutions", []):
                    st.markdown(f"`Due To:` {res['DueTo']}")
                    st.markdown("**Steps:**")
                    for step in res.get("TriagingSteps", []):
                        st.markdown(f"- {step}")
    else:
        st.warning("No matching issues found.")
