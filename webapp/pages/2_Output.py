import openai
import streamlit as st
from streamlit_chat import message
import os
import json
from dotenv import load_dotenv
from copy import deepcopy

from user_data_template import user_data_template

st.sidebar.header("Output")

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

st.header("Example Output")
st.write("This is a minimalist output example to show the data that has been collected. In practice, this data could be sent to a database or used to generate a document/email.")


# Open the JSON file
with open('output.json') as file:
    # Load the JSON data
    data = json.load(file)

# Iterate over each key-value pair and print them
for key, value in data.items():
    st.header(key + ": ")
    st.subheader(value["Response"])
