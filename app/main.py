import os
os.environ["USER_AGENT"] = "Mozilla/5.0 (compatible; MyBot/1.0; +https://example.com/bot)"

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from utils import clean_text
from portfolio import Portfolio
from chains import Chain
import logging
logging.basicConfig(level=logging.INFO)

import os


def create_streamlit_app(llm,portfolio,clean_text):

    st.title("COLD EMAIL GENERATOR")
    # Set User-Agent
    os.environ["USER_AGENT"] = "Mozilla/5.0 (compatible; MyBot/1.0; +https://example.com/bot)"

    url_input = st.text_input("Paste URL of job posting:", value="https://careers.jameshardie.com/job/Albany%2C-NY-Regional-Account-Manager-Albany-NY-12201/1223646400/")
    print("Streamlit app started. URL input:", url_input)
    submit_button = st.button("Submit")

    if submit_button:
        try:

            loader = WebBaseLoader([url_input]) # it will do web scrapping
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs_details(data)
            for job in jobs:
                skills = job.get('skills',[])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job,links)
                st.code(email,language='markdown')
        except Exception as e:
            st.error(f"An error occurred: {e}")
            

if __name__ == "__main__":
    # Initialize the LLM and Portfolio classes
    portfolio = Portfolio()
    logging.info("Portfolio initialized")
    chain = Chain()  # Assuming you have a Chains class defined elsewhere
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
    print("Streamlit app created.")
