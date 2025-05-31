import streamlit as st
from pdfminer.pdfparser import PDFSyntaxError
from resume_match_chain import match_chain
from resume_generation_chain import generate_chain
from utils.pdf_parser import extract_text_from_pdf
import tempfile

st.set_page_config(page_title="AI Resume Consultant", layout="centered")

st.title("🧠 AI Resume Tailor")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
jd_input = st.text_area("Paste Job Description")

edit_manual = st.checkbox("Edit Skills & Projects manually?")

if edit_manual:
    manual_skills = st.text_area("Enter Skills (comma separated)")
    manual_projects = st.text_area("Enter Projects (one per line, leave blank for auto generation)")
else:
    manual_skills = None
    manual_projects = None

if uploaded_file and jd_input:
    if uploaded_file.type != "application/pdf":
        st.error("Please upload a valid PDF file.")
    else:
        uploaded_file.seek(0)
        header = uploaded_file.read(5)
        uploaded_file.seek(0)
        if header != b'%PDF-':
            st.error("The uploaded file does not appear to be a valid PDF.")
        else:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file.flush()
                    resume_text = extract_text_from_pdf(tmp_file.name)

                if st.button("📝 Match & Generate Resume"):
                    with st.spinner("Analyzing..."):
                        # Match original resume with JD
                        original_match_result = match_chain.run({"resume": resume_text, "jd": jd_input})

                        # Prepare extra context for generation
                        extra_context = ""
                        if edit_manual:
                            if manual_skills and manual_skills.strip():
                                extra_context += f"\nUpdate Skills section to: {manual_skills.strip()}\n"
                            if manual_projects and manual_projects.strip():
                                extra_context += f"\nInclude these projects:\n{manual_projects.strip()}\n"
                            else:
                                extra_context += "\nGenerate 3-4 relevant impactful projects automatically.\n"
                        else:
                            extra_context += "\nGenerate 3-4 relevant impactful projects automatically.\n"

                        # Generate updated resume
                        updated_resume = generate_chain.run({
                            "resume": resume_text,
                            "jd": jd_input,
                            "extra_instructions": extra_context
                        })

                        # Match updated resume with JD
                        updated_match_result = match_chain.run({"resume": updated_resume, "jd": jd_input})

                    st.subheader("🔍 Original Resume Match Results")
                    st.text(original_match_result)

                    st.subheader("📄 Updated Resume")
                    st.text_area("Generated Resume:", updated_resume, height=400)

                    st.subheader("🔍 Updated Resume Match Results")
                    st.text(updated_match_result)

            except PDFSyntaxError:
                st.error("The uploaded PDF file is corrupted or invalid. Please upload a different PDF.")
            except Exception as e:
                st.error(f"An unexpected error occurred while processing the PDF: {e}")
