import streamlit as st
import os
from app import pdf_chat
from main import chat

def main():
    st.markdown("# **VIDHAN: To Help You With Legal Queries**")

    # Create a selectbox for user selection
    choice = st.selectbox('Select an option', ['Review Legal Document', 'Chat'])

    if choice == 'Review Legal Document':
        pdf_chat()  # Call the pdf_chat function
    else:
        chat()  # Call the chat function

if __name__ == '__main__':
    main()
