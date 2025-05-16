import streamlit as st
import openai
import json
import re
import fitz  # PyMuPDF

# --- Setup OpenAI client ---
api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=api_key)

# --- Checklist for Section 4 ---
section_4_checklist = [
    {"id": "4.1", "text": "The policy must state that personal data is processed only as per the provisions of the Digital Personal Data Protection Act, 2023."},
    {"id": "4.2", "text": "The policy must confirm that personal data is processed only for a lawful purpose."},
    {"id": "4.3", "text": "The policy must define lawful purpose as any purpose not expressly forbidden by law."},
    {"id": "4.4", "text": "The policy must include a statement that personal data is processed only with the consent of the Data Principal."}
]

# --- Split policy into blocks ---
def break_into_blocks(text):
    lines = text.splitlines()
    blocks, current_block = [], []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r'^([A-Z][A-Za-z\s]+|[0-9]+\.\s.*)$', stripped):
            if current_block:
                blocks.append(' '.join(current_block).strip())
                current_block = []
            current_block.append(stripped)
        else:
            current_block.append(stripped)
    if current_block:
        blocks.append(' '.join(current_block).strip())
    return blocks

# --- Extract text from PDF ---
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

# --- Create GPT prompt ---
def create_prompt(block_text, checklist):
    checklist_text = "\n".join(f"{item['id']}. {item['text']}" for item in checklist)
    return f"""
You are a legal compliance assistant evaluating a privacy policy block against Section 4 of the Digital Personal Data Protection Act (DPDPA), 2023.

Checklist:
{checklist_text}

Policy Block:
\"\"\"{block_text}\"\"\"

Instructions:
1. For each checklist item, determine whether it is:
   - Explicitly Mentioned (clearly and fully satisfied)
   - Partially Mentioned (some elements are present but not fully)
   - Missing (not mentioned at all)

2. In your JSON response, include:
   - The Checklist Item ID
   - Status: Explicitly Mentioned / Partially Mentioned / Missing
   - If status is Explicitly or Partially Mentioned, include a short Justification (1–2 sentences).
   - Do NOT include justification for Missing items.

3. Format your reply as valid JSON like this:

{{
  "Checklist Evaluation": [
    {{
      "Checklist Item ID": "4.1",
      "Status": "Explicitly Mentioned",
      "Justification": "..."
    }},
    {{
      "Checklist Item ID": "4.2",
      "Status": "Missing"
    }},
    ...
  ]
}}
"""

# --- Call GPT API ---
def call_gpt(prompt, client):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

# --- Compile summary from all blocks ---
def compile_summary(checklist, all_block_results):
    summary = {}

    for item in checklist:
        summary[item["id"]] = {
            "Checklist Item ID": item["id"],
            "Final Status": "Missing",
            "Matched Blocks": []
        }

    for block in all_block_results:
        block_id = block["block_id"]
        for item in block["Checklist Evaluation"]:
            item_id = item["Checklist Item ID"]
            status = item["Status"]

            if status != "Missing":
                justification = item.get("Justification", "")
                summary[item_id]["Matched Blocks"].append({
                    "Block ID": block_id,
                    "Status": status,
                    "Justification": justification
                })

    for item_id, info in summary.items():
        statuses = [b["Status"] for b in info["Matched Blocks"]]
        if "Explicitly Mentioned" in statuses:
            info["Final Status"] = "Explicitly Mentioned"
        elif "Partially Mentioned" in statuses:
            info["Final Status"] = "Partially Mentioned"

    return list(summary.values())

# --- Streamlit UI ---
st.title("📜 DPDPA Section 4 Compliance Checker")

upload_option = st.radio("Choose input method:", ["Paste policy text", "Upload PDF"])
policy_text = ""

if upload_option == "Paste policy text":
    policy_text = st.text_area("Paste your privacy policy below:", height=300)
else:
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file:
        policy_text = extract_text_from_pdf(uploaded_file)

if st.button("Run Compliance Check") and policy_text.strip():
    blocks = break_into_blocks(policy_text)
    all_block_results = []

    with st.spinner("Analyzing each block using GPT..."):
        for i, block in enumerate(blocks, start=1):
            prompt = create_prompt(block, section_4_checklist)
            gpt_response = call_gpt(prompt, client)

            try:
                parsed = json.loads(gpt_response)
                parsed["block_id"] = f"BLOCK{i}"
                all_block_results.append(parsed)

                with st.expander(f"🔍 Block {i} Result", expanded=False):
                    for item in parsed["Checklist Evaluation"]:
                        st.write(f"**{item['Checklist Item ID']}** — {item['Status']}")
                        if "Justification" in item:
                            st.write(f"Justification: {item['Justification']}")
            except Exception as e:
                st.error(f"Error in Block {i}: {e}")
                st.code(gpt_response)

    # --- Compile & Show Summary ---
    final_summary = compile_summary(section_4_checklist, all_block_results)

    st.markdown("---")
    st.subheader("📊 Final Checklist Summary Across All Blocks")

    for item in final_summary:
        st.markdown(f"**{item['Checklist Item ID']}** — :blue[{item['Final Status']}]")
        for match in item["Matched Blocks"]:
            st.write(f"  ⮑ **{match['Block ID']}** — {match['Status']}")
            st.write(f"     Justification: {match['Justification']}")
