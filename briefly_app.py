import streamlit as st
import json
import os
from datetime import date
from huggingface_hub import InferenceClient
import uuid

# Button style
st.markdown(
    """
    <style>
    /* Style all Streamlit buttons */
    div.stButton > button {
        background-color: purple;
        color: orange;
        border: 2px orange;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        padding: 8px 20px;
        transition: 0.3s;
    }

    /* Hover effect for all buttons */
    div.stButton > button:hover {
        background-color: orange;
        color: purple;
        border: 2px solid purple;
    }

    </style>
    """,
    unsafe_allow_html=True
)

#Setup the HuggingFace API
@st.cache_resource(show_spinner=True)
def get_hf_client():
    return InferenceClient(
        provider="fireworks-ai",         
        api_key=os.environ["HF_TOKEN"],    # make sure HF_TOKEN is set
    )

hf_client = get_hf_client()

# File to save briefs
DATA_FILE = "briefs.json"
UPLOAD_DIR = "uploads"

# Ensure uploads folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load existing briefs
def load_briefs():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save briefs
def save_briefs(briefs):
    with open(DATA_FILE, "w") as f:
        json.dump(briefs, f, indent=4)

# Clear all briefs
def clear_briefs():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    # Optionally remove all uploaded files
    for file in os.listdir(UPLOAD_DIR):
        os.remove(os.path.join(UPLOAD_DIR, file))


def generate_tagline(project_name):
    prompt = (
        f"Create a catchy tagline for a project named '{project_name}'. "
        "It must be a single sentence, under 140 characters, and suitable for marketing."
        "Output only the tagline."
    )
    
    try:
        result = hf_client.chat.completions.create(
            model="meta-llama/Llama-3.1-70B-Instruct",
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        tagline = result.choices[0].message.content.strip()

        if not tagline:
            tagline = "(AI returned empty tagline — try a different model or prompt)"

        return tagline

    except Exception as e:
        return f"(AI error: {e})"


# App title
st.markdown(
    """
    <h1 style='text-align: center; 
               color: purple; 
               -webkit-text-stroke: 0.2px Orange; 
                font-size: 80px; 
               font-family: Georgia;'>
        Briefly
    </h1>
    """,
    unsafe_allow_html=True
)


st.header("How the Briefly App Works")
st.markdown("""
1. **Submit a New Project Brief**
- Enter your project name, deadline, any relevant links and upload supporting files (PDF, DOCX, images, etc.).
- Click **Submit Brief**.

2. **AI Tagline Generation**
- After submitting, the app generates a catchy tagline for your project using AI.

3. **View Submitted Briefs**
- All submitted briefs are stored and can be accessed under the **Submitted Briefs** tab.
- You can download uploaded files for each brief.
- The AI-generated tagline is shown for each project.
""")

st.markdown(
    """
    <p><span style ='color: orange; font-weight: bold;'> **PS: Ensure your project name is unique for better tagline suggestions.**</span></p>
    """,
    unsafe_allow_html=True
)

# Tabs: Submit | Submitted
tab1, tab2 = st.tabs(["Submit Brief", "Submitted Briefs"])
st.markdown(
    """
    <style>
    /* Make tab labels purple */
    button[data-baseweb="tab"] > div {
        color: purple !important;
        font-weight: bold;
    }

    /* Optional: highlight selected tab */
    button[data-baseweb="tab"][aria-selected="true"] > div {
        color: orange !important;
        background-color: purple !important;
        border-radius: 5px;
        padding: 5px 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

saved_files = []

# Submit form
# --- Tab 1: Submit Brief ---
with tab1:
    project_name = st.text_input("Project Name", key="project_name_input")
    deadline = st.date_input("Deadline", min_value=date.today(), key="deadline_input")
    links = st.text_area("Links (paste URLs here)", key="links_input")

    uploaded_files = st.file_uploader(
        "Upload Files (PDF, DOCX, images, etc.)",
        type=None,
        accept_multiple_files=True,
        key="file_uploader"
    )

    if st.button("Submit Brief", key="submit_brief_btn"):
        if not project_name.strip():
            st.error("Project Name is required.")
        else:
            # Save uploaded files
            if (uploaded_files):
                for file in uploaded_files:
                    file_path = os.path.join(UPLOAD_DIR, file.name)
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())
                    saved_files.append(file.name)
            else: 
                saved_files = []
            
            tagline = generate_tagline(project_name)

            new_brief = {
                "project_name": project_name,
                "deadline": str(deadline),
                "links": links,
                "files": saved_files,
                "tagline": tagline
            }

            briefs = load_briefs()
            briefs.append(new_brief)
            save_briefs(briefs)

            st.success("✅ Brief submitted successfully!")
            st.info(f"✨ AI-generated tagline: {tagline}")


#------Tab 2: Submitted Briefs-------
with tab2:
    briefs = load_briefs()

   
    # Clear the saved briefs
    if st.button("Clear Submitted Briefs"):
        clear_briefs()
        st.success("All briefs cleared.")
        briefs = load_briefs()  # will now be empty
        
    if not briefs:
        st.info("No briefs submitted yet.")
    else:
        for i, brief in enumerate(briefs, start=1):
            with st.expander(f"{i}. {brief['project_name']}"):
                st.write(f"**Deadline:** {brief['deadline']}")
                st.write(f"**Links:** {brief['links'] or 'No links provided'}")
                st.write("**Uploaded Files:**")
                files = brief.get("files", [])
                if files: 
                    for idx, filename in enumerate(files):
                        file_path = os.path.join(UPLOAD_DIR, filename)
                        if os.path.exists(file_path):
                            with open(file_path, "rb") as f:
                                st.download_button(
                                    label=f"⬇️ Download {filename}",
                                    data=f,
                                    file_name=filename,
                                    key=f"download_{brief['project_name']}_{idx}_{uuid.uuid4()}"  # unique key per file
                                )
                        else:
                            st.write(f"- {filename} (missing)")
                else:
                    st.write("No files uploaded.")

                st.write(f"**Tagline:** {brief.get('tagline', '(none)')}")
