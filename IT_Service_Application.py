import streamlit as st
import json
import os

# Page settings
st.set_page_config(layout="wide", page_title="My Bell Issue Analyzer")

# Load JSON data
@st.cache_data
def load_json():
    file_path = os.path.join("knowledge portal", "Mybell_Resolutions.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Failed to load JSON: {e}")
        return []

data = load_json()

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
