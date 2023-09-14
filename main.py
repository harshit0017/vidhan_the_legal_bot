import streamlit as st
import pandas as pd
import numpy as np
import openai 
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

message_history = []  # Initialize message history as an empty list

def is_valid_query(text):
    message = [
        {"role": "system", "content": " decide whether the given query is related to law or not.  "},
        {"role": "system", "content": " return only True or False"},
        {"role": "user", "content": "i have become victim to a theft and all of my money is being stolen what should i do"},
        {"role": "assistant", "content": "True"},
        {"role": "user", "content": "tell me what is the sum of 2 and 3"},
        {"role": "assistant", "content": "False"},
        {"role": "user", "content": text}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        temperature=0.8,
        messages=message,
        max_tokens=5
    )
    return response["choices"][0]["message"]["content"]

def get_reply(text):
    global message_history

    if len(message_history) >= 10:
        message_history.pop(0) 
    x = is_valid_query(text)
    print(x)

    if x == "False":
        message = [{"role": "system", "content": "Tell the user that the purpose of this bot is to help the user with legal queries and ask them to ask questions related to those only"}]
    else:
        message = [
            
            {"role": "system", "content": "You are an Indian lawyer practicing law in India. You have knowledge about all the laws and fundamental rights and you have to help people "},
            {"role": "system", "content": " Understand the given situation and guide the person  accurately on how to proceed further "},
            {"role": "system", "content": " Generate response in points giving guidance to the user on how to proceed further"}, 
            {"role": "system", "content": " Give precise points to the user on how to proceed further"},          
            {"role": "user", "content": "i have become victim to a theft and all of my money is being stolen what should i do"},
            {"role": "assistant", "content": " you should visit the nearest police station and report the stolen money to the police and under the section of theft and law, the police will take action and report back to you "},
            {"role": "user", "content": text}
        ]

    message_history.extend(message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=message_history,
        temperature=0.8,
        max_tokens=400
    )

    reply = response["choices"][0]["message"]["content"]
    message_history.append({"role": "assistant", "content": reply})

    return reply

def chat():
    st.title('Legal Chatbot')
    
    user_input = st.text_input('You:', '')   
    if st.button('Ask'):
        chatbot_reply = get_reply(user_input)
        st.markdown(f"**Chatbot:** {chatbot_reply}") 

if __name__ == '__main__':
    chat()
