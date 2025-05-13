
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        groq_api_key=os.getenv("GROQ_API_KEY")
        )

    def extract_jobs_details(self,cleaned_text):
    
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the 
            following keys: "role", "experience", "skills" and "description".
            Only return the valid JSON. NO PREAMBLE 
            Return the JSON in the following format:
            [
                {{
                    "role": "Software Engineer",
                    "experience": "3-5 years",
                    "skills": ["Python", "JavaScript"],
                    "description": "We are looking for a Software Engineer with experience in Python and JavaScript."
                }}
            ]
            """
        )
        print("Prompt template created.")
        prompt_extract = prompt_extract | self.llm # chain the prompt with the LLM
        print("Prompt template chained with LLM.")
        print("Invoking the LLM to extract job details...")
        response = prompt_extract.invoke(input={"page_data": cleaned_text})
        print("Response received from LLM.",response)

        try:
            json_parser = JsonOutputParser()
            print("Parsing JSON response..!!!!!!!!!!!!!!!!!!!!!!!!!!.")
            with open("response.json", "w") as f:
                f.write(response.content)
            parsed_response = json_parser.parse(response.content)
            print("JSON response parsed successfully.@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        except Exception as e:
            print("Error parsing JSON response:", e)
            # raise e("content is too big. unable to parse")
        return parsed_response if isinstance(parsed_response, list) else [parsed_response]

    def write_mail(self,job,links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Shahid, a business development executive at Konverge.AI. Konverge.AI is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the Hiring Manager of company who as posted job regarding the job mentioned above describing the capability of Konverge 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase Konverge portfolio: {link_list}
            Remember you are Shahid, BDE at Konverge.AI 
            Do not provide a preamble. 
            ### EMAIL (NO PREAMBLE) No placeholder in email:

            """)
        
        chain_email = prompt_email | self.llm # chain the prompt with the LLM
        res = chain_email.invoke({"job_description":str(job), "link_list":links})

        return res.content
     
if __name__ == "__main__":
    pass
    
