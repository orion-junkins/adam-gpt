import openai
import streamlit as st
from streamlit_chat import message
import os
from dotenv import load_dotenv
from copy import deepcopy

from ...user_data_template import user_data_template


st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)
st.sidebar.header("Adam-GPT")


load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

st.header("Streamlit Chat - Demo")
st.subheader("This is a pretotype of an AI based startup advisor")
st.markdown("[Github](https://github.com/ai-yash/st-chat)")

if st.button('Reset'):
    st.session_state['generated'] = []
    st.session_state['messages'] = []
    st.session_state['past'] = []
    st.session_state['message_count'] = 0
    st.session_state['user_data'] = deepcopy(user_data_template)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'input_text' not in st.session_state:
    st.session_state['input_text'] = ''
if 'message_count' not in st.session_state:
    st.session_state['message_count'] = 0

if 'user_data' not in st.session_state:
    st.session_state['user_data'] = deepcopy(user_data_template)

max_messages = 5

def all_information_gathered():
    for key, value in st.session_state['user_data'].items():
        if value['Response'] == None:
            return False
    return True

def get_next_ungathered_information():
    for key, value in st.session_state['user_data'].items():
        if value['Response'] == None:
            return key, value
    return None

def submit():
    st.session_state.input_text = st.session_state.widget
    st.session_state.widget = ''

st.text_input("", "", key='widget', on_change=submit)
user_input = st.session_state.input_text

if user_input and st.session_state['message_count'] < max_messages and not all_information_gathered():
    user_data_key, information_to_gather = get_next_ungathered_information()

    st.session_state.messages.append({"role": "user", "content": information_to_gather["Context"]})

    st.session_state['message_count'] += 1

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.past.append(user_input)

    completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= st.session_state.messages,
        )
    completion_text = completion.choices[0].message.content

    if ("####" in completion_text):
        answer = completion_text.strip('#')
        st.session_state['user_data'][user_data_key]['Response'] = answer
    else:
        st.session_state.messages.append({"role": "assistant", "content": completion_text})
        
        st.session_state.generated.append(completion_text)


if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

if all_information_gathered():
    st.write("DONE")