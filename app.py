from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os, io, base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_res(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    respoce = model.generate_content([input, pdf_content[0], prompt])
    return respoce.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        #convert inot bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='jpeg')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_part = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() ## encode to base64
            }
        ]
        return pdf_part
    else:
        raise FileNotFoundError("NO FILE UPLOADED")

## Streamlit part
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS SYSTEM")
input_text = st.text_area("job desctiption: ", key="input")
uploaded_file = st.file_uploader("Upload your resume here (pdf)....", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

st1 = st.button("Tell me about my resume")
st2 = st.button("Percentage match")


inP1 = """
As a seasoned Human Resources professional specializing in the domains of Data Science, Computer Vision, Data Engineering, 
Machine Learning Engineering, Data Analysis, and Natural Language Processing (NLP), your responsibility involves assessing the 
given resume in light of the job description for these roles. Kindly provide your professional analysis, highlighting the candidate's strengths 
and weaknesses with respect to the specified job requirements
"""

inP2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and deep ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if st1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        respoce = get_gemini_res(inP1, pdf_content, input_text)

        st.subheader("The responce is: ")
        st.write(respoce)
    else:
        st.write("Please upload the resume")

elif st2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        respoce = get_gemini_res(inP2, pdf_content, input_text)

        st.subheader("The responce is: ")
        st.write(respoce)
    else:
        st.write("Please upload the resume")