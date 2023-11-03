import PyPDF2
import streamlit as st
st.set_page_config(layout="wide")
import os
os.environ["OPENAI_API_KEY"] =st.secrets['API_KEY']
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
st.markdown("<h1 style='text-align: center;'>AI Startup Summarize BOT</h1>", unsafe_allow_html=True)
st.write(' ')

# converts the pdf file to list of paragraphs
def pdf_to_paragraphs_list(file):
    topics_list=[]
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        topics_list.append(text)
    return " ".join(topics_list)

# openai to generate summary
def get_startup_summary(context):
    large_language_model = OpenAI(temperature=0.9)  # model_name="text-davinci-003"
    text = '''  step 1: I have provided you a business data, first understand it clearly
                step 2: generate introduction, benificts, risks with less than 200 words
                step 3: Your answer should help investors 
                content is :  '''+context
    summary_generated=large_language_model(text)
    return summary_generated

def get_answers(context):
    large_language_model1 = OpenAI(temperature=0.9)  # model_name="text-davinci-003"
    text = '''  Answer only related to the above content the question is:'''+context
    answer_generated=large_language_model1(text)
    return answer_generated
# display the bot interface
col1,col,col2= st.columns([5,1,5])
with col1:
    st.markdown("<h4 style='text-align: center;'>Upload the PDF of any Startup Application</h4>", unsafe_allow_html=True)
    pdf_file = st.file_uploader("Upload Startup PDF file", type=["pdf"])
    if pdf_file:
        b1=st.button('Generate Summary')
        if b1:
            paragraphs_list = pdf_to_paragraphs_list(pdf_file) 
            startup_Summary=get_startup_summary(paragraphs_list)
            st.write(startup_Summary)
    st.markdown("<h4 style='text-align: center;'>-------or------</h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Past the Content of any startup Application</h4>", unsafe_allow_html=True)
        # Create a text input field
    user_input = st.text_input("Copy and Past Startup Content Here")
    if user_input:
        b2=st.button("generate summary")
        if b2:
            startup_Summary=get_startup_summary(user_input)
            st.write(startup_Summary)

with col2:
    st.markdown("<h4 style='text-align: center;'>Queries for startup Application</h4>", unsafe_allow_html=True)
    user_input = st.text_input("Do you have any questions related to above startup, we are here to help, ask anything")
    if user_input:
        answer= get_answers(user_input)
        st.write(answer)


