from dotenv import load_dotenv
load_dotenv()  ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

## function to load gemini pro model
model = genai.GenerativeModel("gemini-pro")

def get_responce(questions):
    responce = model.generate_content(questions)
    return responce.text

st.set_page_config(page_title = "Q & A demo")
st.header("Gemini LLM Application")

input = st.text_input("Input: ", key = "input")
submit = st.button("Ask the question")

if submit:
    responce = get_responce(input)
    st.subheader("The responce is: ")
    st.write(responce)