import streamlit as st
import json
import os

# Page settings
st.set_page_config(layout="wide", page_title="My Bell Issue Analyzer")

# Load JSON data
def load_data():
    json_file_path = r"Mybell_Resolutions.json"
    if not os.path.exists(json_file_path):
        st.error(f"File not found: {json_file_path}")
        return []
    with open(json_file_path, "r", encoding="utf-8") as file:
        return json.load(file)

data = load_data()

# Header
st.markdown("## 🔍 My Bell Issue Analyzer")

# Search bar aligned to left
query = st.text_input("Search Issue", "", label_visibility="collapsed", placeholder="Type issue name here...")

# Display results if any
if query:
    query = query.strip().lower()
    results = [issue for issue in data if query in issue['IssueName'].lower()]

    if results:
        for idx, issue in enumerate(results, start=1):
            with st.container():

                st.markdown("---")

            # Columns layout: Related Ticket | Divider | Details
            col1, col_div1, col2, col_div2, col3 = st.columns([2.8, 0.2, 3.5, 0.2, 6])

            with col1:
                # st.markdown(f"## 🔹 Result {idx}")
                st.markdown(f"### 📄 Result ---- {idx}")
                st.markdown(f"`Issue:` {issue['IssueName']}")
                st.markdown(f"`Functionality:` {issue.get('Functionality', '')}")
                st.markdown(f"`Area:` {issue.get('Area', '')}")
                st.markdown(f"`LOB:` {issue.get('LOB', '')}")

            with col_div1:
                st.divider()

            with col2:
                st.markdown("### 🎫 Related Tickets")
                for idx, res in enumerate(issue.get("Resolutions", [])):
                    st.markdown(f"- `INC-{1000 + idx}`: {res.get('DueTo', '')}")

            with col_div2:
                st.divider()

            with col3:
                st.subheader("🛠️ Resolution")
                for resolution in issue['Resolutions']:
                    with st.expander(f"`Due To:` {resolution['DueTo']}"):
                        st.markdown("**Triaging Steps:**")
                        for step in resolution['TriagingSteps']:
                            st.write(f"- {step}")

            # Divider between issues
            st.markdown("---")
    else:
        st.warning("No matching issues found.")
else:
    st.info("Type an issue name in the search bar to begin.")
