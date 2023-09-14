
import os
import streamlit as st
from PyPDF2 import PdfReader
import langchain
langchain.verbose = False
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv
load_dotenv()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')
def pdf_chat():
   
    
    
    st.header("Please upload your document in PDF format")

    pdf = st.file_uploader("Upload your PDF", type="pdf")

    if pdf is not None:
        pdf_reader =  PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()


        max_length = 1800
        original_string = text
        temp_string = ""
        strings_list = []

        for character in original_string:
            if len(temp_string) < max_length:
                temp_string += character
            else:
                strings_list.append(temp_string)
                temp_string = ""

        if temp_string:
            strings_list.append(temp_string)

        #split into chunks
        

        # create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(strings_list, embedding=embeddings)

        user_question = st.text_input("Ask your query related to the document")

        if user_question:
            docs = knowledge_base.similarity_search(user_question)
            
            llm = OpenAI(model_name="gpt-3.5-turbo-16k", temperature=0.9)

            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents = docs, question = user_question)
                print(cb)

            st.write(response)

if __name__ == '__main__':
    pdf_chat()

