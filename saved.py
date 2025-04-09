import streamlit as st
import json
import os

# Page settings
st.set_page_config(layout="wide", page_title="My Bell Issue Analyzer")

# Load JSON data from file
def load_data():
    json_file_path = "knowledge portal/Mybell_Resolutions.json"
    if not os.path.exists(json_file_path):
        st.error(f"File not found: {json_file_path}")
        return []
    with open(json_file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Check if query matches anywhere in the issue (exact or partial)
def matches_query(issue, query):
    query = query.lower()
    # Collect all searchable strings from the issue
    searchable_text = " ".join([
        str(issue.get('IssueName', '')),
        str(issue.get('Functionality', '')),
        str(issue.get('Area', '')),
        str(issue.get('LOB', ''))
    ])

    for resolution in issue.get('Resolutions', []):
        searchable_text += " " + resolution.get('DueTo', '')
        searchable_text += " " + " ".join(resolution.get('TriagingSteps', []))

    # Convert all to lowercase
    searchable_text = searchable_text.lower()

    # Check for full sentence or keyword match
    return query in searchable_text

# Load data
data = load_data()

# Header
st.markdown("## 🔍 My Bell Issue Analyzer")

# Search bar
query = st.text_input("Search Issue", "", label_visibility="collapsed", placeholder="Type keyword or sentence here...")

# Display results
if query:
    results = [issue for issue in data if matches_query(issue, query)]

    if results:
        for idx, issue in enumerate(results, start=1):
            st.markdown("---")
            col1, col_div1, col2, col_div2, col3 = st.columns([2.8, 0.2, 3.5, 0.2, 6])

            with col1:
                st.markdown(f"### 📄 Result ---- {idx}")
                st.markdown(f"**Issue:** {issue['IssueName']}")
                st.markdown(f"**Functionality:** {issue.get('Functionality', '')}")
                st.markdown(f"**Area:** {issue.get('Area', '')}")
                st.markdown(f"**LOB:** {issue.get('LOB', '')}")

            with col_div1:
                st.divider()

            with col2:
                st.markdown("### 🎫 Related Tickets")
                for i, res in enumerate(issue.get("Resolutions", [])):
                    st.markdown(f"- INC-{1000 + i}: {res.get('DueTo', '')}")

            with col_div2:
                st.divider()

            with col3:
                st.subheader("🛠️ Resolution")
                for resolution in issue.get("Resolutions", []):
                    with st.expander(f"Due To: {resolution.get('DueTo', '')}"):
                        st.markdown("**Triaging Steps:**")
                        for step in resolution.get("TriagingSteps", []):
                            st.write(f"- {step}")
            st.markdown("---")
    else:
        st.warning("No matching issues found.")
else:
    st.info("Type an issue name, keyword, or full sentence in the search bar to begin.")
