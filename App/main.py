import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    # Set custom CSS for background color
    st.markdown(
        """
        <style>
        .main {
            background-color: #f0f2f5;  /* Change this color to your desired background color */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Use a larger title
    st.markdown("<h1 style='font-size: 40px;'>📧 Cold Mail Generator</h1>", unsafe_allow_html=True)
    
    # Increase the font size for the input label
    st.markdown("<h2 style='font-size: 30px;'>Enter a URL:</h2>", unsafe_allow_html=True)
    url_input = st.text_input("", placeholder="https://link-to-your-job-description")
    
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                
                # Increase the size of the displayed email code
                st.markdown("<h3 style='font-size: 28px;'>Generated Email:</h3>", unsafe_allow_html=True)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")
            
if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    # Set the page configuration first
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
