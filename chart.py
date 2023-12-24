import torch
from diffusers import DiffusionPipeline

from dotenv import load_dotenv
load_dotenv()  ## loading all the environment variables

from PIL import Image
import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

# Load the Stable Diffusion pipeline (adjust model name as needed)
pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16)

## function to load gemini pro model
model = genai.GenerativeModel("gemini-pro-vision")

def get_responce(questions, img):
    if input != "":
        responce = model.generate_content([questions, img])
    else:
        responce = model.generate_content(img)
    return responce.text

st.set_page_config(page_title = "Gemini Image demo")
st.header("Gemini LLM Application")

input = st.text_input("Input: ", key = "input")

uploaded_file = st.file_uploader("Choose an image...", type = ["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption = "Uploaded Image.", use_column_width = True)

submit = st.button("Tell me about the image")

if submit:
    responce = get_responce(input, image)
    st.subheader("The responce is: ")
    st.write(responce)

    # Generate the image
    gen_image = pipe(responce).images[0]

    image = ""
    if gen_image is not None:
        image = Image.open(gen_image)
        st.image(image, caption = "Generated Image.", use_column_width = True)