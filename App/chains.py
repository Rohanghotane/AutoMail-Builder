import os
from langchain_groq import ChatGroq
# from langchain.document_loaders import WebBaseLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
load_dotenv()
os.getenv("API_KEY")



class Chain:
  def __init__(self):
    self.llm = ChatGroq(temperature=0,
                        groq_api_key=os.getenv("API_KEY"),
                        model_name="llama-3.3-70b-versatile")

  def extract_job(self, cleaned_text):
    prompt_extract = PromptTemplate.from_template("""
              ###SCRAPED TEXT FROM WEBSITE:
              {page_data}
              ####INSTRUCTION:
              The scrape text is from the career's page of a website.
              Your job is to extract the job posting and return in JSON format containing the
              following keys: 'role','experience','skills' and 'discription'.
              only return the valid JSON
              ###VALID JSON (NO PREAMBLE):
              """
  )

    chain_extract = prompt_extract  | self.llm
    res = chain_extract.invoke(input = {"page_data":cleaned_text})
    try:
      json_parser = JsonOutputParser()
      res = json_parser.parse(res.content)
    except OutputParserException:
      raise OutputParserException("Context too large. Unable to parse jobs.")
    return res if isinstance(res, list) else [res]

  def write_mail(self,job,links):
    prompt_mail = PromptTemplate.from_template("""
    {job_description}

      Imagine you are sandeep, a business development executive at infotact solution. infotact solution is a AI and software consulting company the
      seamless integration of business through automated tools.
      Over our experience, we empowered numerous enterprises with fostering solution, process optimazation, cost reduction and highleted overall efficiency.
      Your job is write a cold email to the client regarding the job mentioned above discribing the capability in fulfilling there needs.
      Aso add the most relevent ones from the following links to showcase infotact solution portfolio: {links_list}
      (NO PREAMBLE):

      """
  )

    chain_email = prompt_mail  | self.llm
    res = chain_email.invoke({'job_description': str(jobs), 'links_list': links})
    return res.content
