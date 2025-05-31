from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

template = """
Compare the following resume with the job description and give a match score and reasoning.

Resume:
{resume}

Job Description:
{jd}

Return a score out of 100 and a brief analysis.
"""

prompt = PromptTemplate(input_variables=["resume", "jd"], template=template)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=300)
match_chain = LLMChain(llm=llm, prompt=prompt)
