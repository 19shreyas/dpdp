# streamlit_app.py

import streamlit as st
import openai
import pandas as pd
import json

# STEP 1: Setup OpenAI API Key
openai.api_key = st.secrets["openai_api_key"]
client = openai.OpenAI(api_key=openai.api_key)

# STEP 2: UI
st.title("DPDPA Compliance Checker")
st.markdown("This tool checks your Privacy Policy against DPDPA Chapter II sections.")

# STEP 3: Input Texts (Pre-filled for now)
dpdpa_chapter_text = """CHAPTER II
OBLIGATIONS OF DATA FIDUCIARY

4. Grounds for processing personal data.
(1) A person may process the personal data of a Data Principal only in accordance with the provisions of this Act and for a lawful purpose—
  (a) for which the Data Principal has given her consent; or
  (b) for certain legitimate uses.

(2) For the purposes of this section, the expression “lawful purpose” means any purpose which is not expressly forbidden by law.

5. Notice.
(1) Every request made to a Data Principal under section 6 for consent shall be accompanied or preceded by a notice given by the Data Fiduciary to the Data Principal, informing her—
  (i) the personal data and the purpose for which the same is proposed to be processed;
  (ii) the manner in which she may exercise her rights under sub-section (4) of section 6 and section 13; and
  (iii) the manner in which the Data Principal may make a complaint to the Board, in such manner and as may be prescribed.

(2) Where a Data Principal has given her consent for processing personal data before the commencement of this Act—
  (a) the Data Fiduciary shall, as soon as reasonably practicable, give the Data Principal a notice with the above information;
  (b) the Data Fiduciary may continue processing unless the Data Principal withdraws her consent.

(3) The Data Fiduciary shall provide the notice in English or any language under the Eighth Schedule of the Constitution.

6. Consent.
(1) Consent shall be free, specific, informed, unconditional, unambiguous, and signify agreement by clear affirmative action, limited to necessary personal data for the specified purpose.

(2) Any infringing part of consent shall be invalid to the extent of infringement.

(3) Every consent request must be in clear and plain language, accessible in English or Eighth Schedule languages, with Data Protection Officer contact where applicable.

(4) Data Principals can withdraw consent anytime, with ease comparable to giving consent.

(5) Withdrawal consequences must be borne by the Data Principal and do not affect prior lawful processing.

(6) After withdrawal, Data Fiduciaries and Processors must cease processing unless otherwise required by law.

(7) Consent can be managed through a Consent Manager registered with the Board.

(8) Consent Managers act on behalf of Data Principals and are accountable to them.

(9) Consent Managers must be registered as prescribed.

(10) Data Fiduciary must prove that notice was given and consent was valid, if challenged.

7. Certain legitimate uses.
Personal data may be processed without consent for:
  (a) Voluntarily provided personal data for specified purposes without expressed objection.
  (b) Subsidy, benefit, certificate, etc., provided by the State.
  (c) Performance of State functions or in the interest of sovereignty, integrity, or security.
  (d) Legal obligations to disclose information.
  (e) Compliance with court orders or judgments.
  (f) Medical emergencies.
  (g) Public health emergencies.
  (h) Disaster situations.
  (i) Employment purposes like corporate espionage prevention.

8. General obligations of Data Fiduciary.
(1) Data Fiduciary is responsible for compliance regardless of agreements with Processors.

(2) Data Fiduciary may engage Processors only under valid contracts.

(3) If personal data is used for decisions affecting Data Principals or disclosed, ensure completeness, accuracy, and consistency.

(4) Implement technical and organisational measures to ensure compliance.

(5) Protect personal data using reasonable security safeguards against breaches.

(6) Notify the Board and affected Data Principals in case of breaches, as prescribed.

(7) Erase personal data upon withdrawal of consent or when the specified purpose is no longer served, unless legally required to retain.

(8) "Specified purpose no longer served" deemed if Data Principal does not approach the Fiduciary within prescribed time.

(9) Publish business contact info of DPO or designated grievance redressal officer.

(10) Establish an effective grievance redressal mechanism.

(11) Clarification: lack of contact by Data Principal within time period implies specified purpose is no longer served.

9. Processing of personal data of children.
(1) Before processing, obtain verifiable parental or guardian consent.

(2) No detrimental processing that harms the child's well-being.

(3) No tracking, behavioural monitoring, or targeted advertising to children.

(4) Exemptions may be prescribed for certain Data Fiduciaries or purposes.

(5) Safe processing standards may allow higher age exemptions.

10. Additional obligations of Significant Data Fiduciaries.
(1) Significant Data Fiduciaries notified by Government based on volume, sensitivity, sovereignty impact, etc.

(2) Must:
  (a) Appoint a Data Protection Officer (DPO) based in India, responsible to the Board.
  (b) Appoint an independent Data Auditor.
  (c) Undertake:
    (i) Periodic Data Protection Impact Assessments,
    (ii) Periodic audits,
    (iii) Other prescribed compliance measures."""  # Same as before
privacy_policy_text = """Information we collect
We collect information to provide better services to all of our users – from figuring out basic stuff like which language you speak,
to more complex things like which ads you’ll find most useful, the people who matter most to you online, or which
YouTube videos you might like.
We collect information in the following ways:
Information you give us. For example, many of our services require you to sign up for a Google Account. When you
do, we’ll ask for personal information, like your name, email address, telephone number or credit card to store with your
account. If you want to take full advantage of the sharing features we offer, we might also ask you to create a publicly
visible Google Profile, which may include your name and photo.
Information we get from your use of our services. We collect information about the services that you use and how
you use them, like when you watch a video on YouTube, visit a website that uses our advertising services, or view and
interact with our ads and content. This information includes:
Device information
We collect device-specific information (such as your hardware model, operating system version, unique device
identifiers, and mobile network information including phone number). Google may associate your device
identifiers or phone number with your Google Account.
Log information
When you use our services or view content provided by Google, we automatically collect and store certain
information in server logs. This includes:
details of how you used our service, such as your search queries.
telephony log information like your phone number, calling-party number, forwarding numbers, time and
date of calls, duration of calls, SMS routing information and types of calls.
Internet protocol address.
device event information such as crashes, system activity, hardware settings, browser type, browser
language, the date and time of your request and referral URL.
cookies that may uniquely identify your browser or your Google Account.
Location information
When you use Google services, we may collect and process information about your actual location. We use
various technologies to determine location, including IP address, GPS, and other sensors that may, for
example, provide Google with information on nearby devices, Wi-Fi access points and cell towers.
Unique application numbers
Certain services include a unique application number. This number and information about your installation (for
example, the operating system type and application version number) may be sent to Google when you install or
uninstall that service or when that service periodically contacts our servers, such as for automatic updates.
Local storage
We may collect and store information (including personal information) locally on your device using mechanisms
such as browser web storage (including HTML 5) and application data caches.
Cookies and similar technologies
We and our partners use various technologies to collect and store information when you visit a Google service,
and this may include using cookies or similar technologies to identify your browser or device. We also use these
technologies to collect and store information when you interact with services we offer to our partners, such as
advertising services or Google features that may appear on other sites. Our Google Analytics product helps
businesses and site owners analyze the traffic to their websites and apps. When used in conjunction with our
advertising services, such as those using the DoubleClick cookie, Google Analytics information is linked, by the
Google Analytics customer or by Google, using Google technology, with information about visits to
multiple sites.
Information we collect when you are signed in to Google, in addition to information we obtain about you from partners, may be
associated with your Google Account. When information is associated with your Google Account, we treat it as personal
information. For more information about how you can access, manage or delete information that is associated with your Google
Account, visit the Transparency and choice section of this policy.
How we use information we collect
We use the information we collect from all of our services to provide, maintain, protect and improve them, to develop new
ones, and to protect Google and our users. We also use this information to offer you tailored content – like giving you more
relevant search results and ads.
We may use the name you provide for your Google Profile across all of the services we offer that require a Google Account. In
addition, we may replace past names associated with your Google Account so that you are represented consistently across all
our services. If other users already have your email, or other information that identifies you, we may show them your publicly
visible Google Profile information, such as your name and photo.
If you have a Google Account, we may display your Profile name, Profile photo, and actions you take on Google or on third-
party applications connected to your Google Account (such as +1’s, reviews you write and comments you post) in our services,
including displaying in ads and other commercial contexts. We will respect the choices you make to limit sharing or visibility
settings in your Google Account.
When you contact Google, we keep a record of your communication to help solve any issues you might be facing. We may use
your email address to inform you about our services, such as letting you know about upcoming changes or improvements.
We use information collected from cookies and other technologies, like pixel tags, to improve your user experience and the
overall quality of our services. One of the products we use to do this on our own services is Google Analytics. For example, by
saving your language preferences, we’ll be able to have our services appear in the language you prefer. When showing you
tailored ads, we will not associate an identifier from cookies or similar technologies with sensitive categories, such as those
based on race, religion, sexual orientation or health.
Our automated systems analyze your content (including emails) to provide you personally relevant product features, such as
customized search results, tailored advertising, and spam and malware detection.
We may combine personal information from one service with information, including personal information, from other
Google services – for example to make it easier to share things with people you know. Depending on your account
settings, your activity on other sites and apps may be associated with your personal information in order to improve Google’s
services and the ads delivered by Google.
We will ask for your consent before using information for a purpose other than those that are set out in this Privacy Policy.
Google processes personal information on our servers in many countries around the world. We may process your personal
information on a server located outside the country where you live."""  # Same as before

# For brevity in Streamlit demo, consider loading from files or text input boxes if needed

# STEP 4: Sections to Analyze
dpdpa_sections = [
    "Section 4 — Grounds for Processing Personal Data",
    "Section 5 — Notice",
    "Section 6 — Consent",
    "Section 7 — Certain Legitimate Uses",
    "Section 8 — General Obligations of Data Fiduciary",
    "Section 9 — Processing of Personal Data of Children",
    "Section 10 — Additional Obligations of Significant Data Fiduciaries"
]

# STEP 5: Define the GPT analysis function
def analyze_section(section_text, policy_text, full_chapter_text):
    prompt = f"""
You are a DPDPA compliance expert.

Analyze the company's full Privacy Policy text given below:
\"\"\"{policy_text}\"\"\"

Cross-reference it ONLY against the following DPDPA Section:
\"\"\"{section_text}\"\"\"

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
No explanation outside the JSON.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

# STEP 6: Run the analysis when button clicked
if st.button("Run Compliance Check"):
    results = []
    with st.spinner("Analyzing..."):
        for section in dpdpa_sections:
            try:
                st.text(f"🔎 Checking {section}...")
                section_response = analyze_section(section, privacy_policy_text, dpdpa_chapter_text)
                parsed = json.loads(section_response)
                results.append(parsed)
            except Exception as e:
                st.error(f"Error analyzing {section}: {e}")
                continue

    # Convert to DataFrame and display
    try:
        df = pd.DataFrame(results)
        st.success("✅ Completed analysis of all sections!")
        st.subheader("📋 Compliance Table")
        st.dataframe(df)

        # Calculate compliance score
        total_sections = df.shape[0]
        scored_points = df["Compliance Points"].astype(float).sum()
        compliance_percentage = (scored_points / total_sections) * 100

        st.subheader("🎯 Compliance Score Summary")
        st.write(f"**Total Sections Analyzed:** {total_sections}")
        st.write(f"**Total Points Scored:** {scored_points:.2f}")
        st.write(f"**Compliance Score:** {compliance_percentage:.2f}%")

        # Allow Excel download
        excel_filename = "DPDPA_Compliance_SectionWise_Final.xlsx"
        df.to_excel(excel_filename, index=False)
        with open(excel_filename, "rb") as f:
            st.download_button("📥 Download Excel", f, file_name=excel_filename)
    except Exception as e:
        st.error(f"Error generating output: {e}")