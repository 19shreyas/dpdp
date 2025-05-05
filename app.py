# app.py

import streamlit as st
import openai
import pandas as pd
import json
from io import BytesIO

# ---- UI Layout ----
st.set_page_config(page_title="DPDPA Compliance Tool", layout="wide")
st.title("🔐 DPDPA Section-wise Compliance Checker")

# ---- OpenAI API Key ----
st.sidebar.header("🔑 OpenAI API Key")
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")

if not api_key:
    st.warning("Please enter your OpenAI API key to begin.")
    st.stop()

client = openai.OpenAI(api_key=api_key)

# ---- Input Texts ----
st.sidebar.header("📄 Paste Inputs")
dpdpa_chapter_text = st.sidebar.text_area("Paste full DPDPA Chapter II text:", height=300)
privacy_policy_text = st.sidebar.text_area("Paste Privacy Policy text:", height=300)

# ---- Define DPDPA Sections ----
dpdpa_sections = [
    "Section 4 — Grounds for Processing Personal Data",
    "Section 5 — Notice",
    "Section 6 — Consent",
    "Section 7 — Certain Legitimate Uses",
    "Section 8 — General Obligations of Data Fiduciary",
    "Section 9 — Processing of Personal Data of Children",
    "Section 10 — Additional Obligations of Significant Data Fiduciaries"
]

# ---- GPT Classification Function ----
def analyze_section(section_text, policy_text):
    prompt = f"""
You are a DPDPA compliance expert.

Analyze the company's full Privacy Policy text given below:
"""{policy_text}"""

Cross-reference it ONLY against the following DPDPA Section:
"""{section_text}"""

Instructions:
- Find all matching sentences/phrases that are contextually aligned with this Section.
- If NO match is found, clearly state "No matching text found."
- If matches are found:
    - Quote ALL matched policy sentences (not just the first one).
- Classify:
    - Match Level: Fully Compliant / Partially Compliant / Non-Compliant
    - If Partially Compliant, classify Severity:
        - Minor = Small, non-critical missing point
        - Medium = Important but fixable gap
        - Major = Critical missing requirement
- Assign Compliance Points:
    - Fully Compliant = 1.0
    - Partially Compliant:
        - Minor = 0.75
        - Medium = 0.5
        - Major = 0.25
    - Non-Compliant = 0.0
- Provide a short Justification and Suggested Rewrite.

Output strictly in JSON format:
{{
  "DPDPA Section": "...",
  "Matched Policy Snippets": "...",
  "Match Level": "...",
  "Severity": "...",
  "Compliance Points": "...",
  "Justification": "...",
  "Suggested Rewrite": "..."
}}
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content

# ---- Run Analysis ----
if st.button("🚀 Run Compliance Check"):
    if not dpdpa_chapter_text or not privacy_policy_text:
        st.error("Please paste both the DPDPA and policy texts.")
        st.stop()

    results = []
    for section in dpdpa_sections:
        with st.spinner(f"Checking {section}..."):
            try:
                result_json = analyze_section(section, privacy_policy_text)
                parsed = json.loads(result_json)
                results.append(parsed)
            except Exception as e:
                st.error(f"Error processing {section}: {e}")

    if results:
        df = pd.DataFrame(results)
        st.success("✅ Analysis complete!")

        st.subheader("📋 Compliance Results")
        st.dataframe(df, use_container_width=True)

        # Score Calculation
        scored_points = df['Compliance Points'].astype(float).sum()
        total_possible = len(df)
        compliance_percent = (scored_points / total_possible) * 100

        st.metric(label="🎯 Compliance Score", value=f"{compliance_percent:.2f}%")

        # Excel download
        towrite = BytesIO()
        df.to_excel(towrite, index=False, engine='openpyxl')
        towrite.seek(0)

        st.download_button(
            label="📥 Download Excel Report",
            data=towrite,
            file_name="DPDPA_Compliance_Results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )