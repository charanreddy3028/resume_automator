from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

template = """
You are an expert resume writer.

Given the resume and job description, do the following:

1. Keep the Skills section as-is if manual skills are provided; otherwise, add relevant skills from the job description.
2. Rewrite the Work Experience section to highlight achievements and responsibilities aligned with the job description.
3. Include projects if provided manually; otherwise generate 3-4 relevant projects.
4. Update the Summary slightly to align with the job.
5. Use bullet points for experience and projects.
6. Label sections as "Professional Summary", "Skills", "Work Experience", and "Projects".
7. Keep formatting clean and professional.

Resume:
{resume}

Job Description:
{jd}

Additional Instructions:
{extra_instructions}

Return the updated resume text.
"""

prompt = PromptTemplate(
    input_variables=["resume", "jd", "extra_instructions"],
    template=template
)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, max_tokens=1500)
generate_chain = LLMChain(llm=llm, prompt=prompt)
