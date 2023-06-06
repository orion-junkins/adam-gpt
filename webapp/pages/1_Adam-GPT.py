import re
import openai
import streamlit as st
from streamlit_chat import message
import os
import json
from dotenv import load_dotenv
from copy import deepcopy

from user_data_template import user_data_template

st.sidebar.header("Adam-GPT")

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

st.header("Adam GPT - Demo")
st.subheader("Your friendly neighborhood startup advising AI")
st.write("Adam's job is to gather the basic facts about your business. Once he has gathered all the information needed, he will forward your case human lawyers to review your case and they will be in touch with you shortly with next steps.")
st.write("Adam is going to try to find out the name of your business, the tagline, and the best structure. If you don't know these things, that's okay! Adam will help you figure it out.")
st.write("Join the chat below to get started...")

st.markdown("[Github](https://github.com/ai-yash/st-chat)")

if st.button('Reset'):
    st.session_state['gpt_messages'] = []
    st.session_state['user_facing_messages'] = []
    st.session_state['message_count'] = 0
    st.session_state['user_data'] = deepcopy(user_data_template)
    st.session_state['visited_data_fields'] = []
    st.session_state['primed'] = False

    seed_message = "Hello! I'm Adam :) Let's get started."
    st.session_state.user_facing_messages.append((seed_message, False))

if 'gpt_messages' not in st.session_state:
    st.session_state['gpt_messages'] = []

if 'user_facing_messages' not in st.session_state:
    st.session_state['user_facing_messages'] = []
    seed_message = "Hello! I'm Adam :) Let's get started."
    st.session_state.user_facing_messages.append((seed_message, False))

if 'input_text' not in st.session_state:
    st.session_state['input_text'] = ''

if 'message_count' not in st.session_state:
    st.session_state['message_count'] = 0

if 'user_data' not in st.session_state:
    st.session_state['user_data'] = deepcopy(user_data_template)

if 'visited_data_fields' not in st.session_state:
    st.session_state['visited_data_fields'] = []

if 'primed' not in st.session_state:
    st.session_state['primed'] = False

if 'current_field' not in st.session_state:
    st.session_state['current_field'] = None

max_messages = 10

def get_next_ungathered_information():
    for key, value in st.session_state['user_data'].items():
        if value['Response'] == None:
            return key, value
    return None

if not st.session_state.primed:
    st.session_state.primed = True
    next_ungathered = get_next_ungathered_information()
    if next_ungathered == None:
        st.title("All done gathering data!")
        st.write("The AI agent has gathered all of the information it needs. Your case has been forwarded to our team of human lawyers. They will be in touch with you shortly with next steps!")
        with open("output.json", "w") as json_file:
            json.dump(st.session_state['user_data'], json_file)
        st.stop()

    user_data_key, information_to_gather = next_ungathered
    st.session_state.current_field = user_data_key

    st.session_state.gpt_messages.append({"role": "user", "content": information_to_gather["Context"]})
    st.session_state.message_count = 0

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= st.session_state.gpt_messages,
    )
    completion_text = completion.choices[0].message.content
    st.session_state.gpt_messages.append({"role": "assistant", "content": completion_text})
    st.session_state.user_facing_messages.append((completion_text, False))
    st.session_state.message_count += 1


def submit():
    user_input = st.session_state.widget
    st.session_state.widget = ''
    st.session_state.gpt_messages.append({"role": "user", "content": user_input})
    st.session_state.user_facing_messages.append((user_input, True))

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= st.session_state.gpt_messages,
    )
    completion_text = completion.choices[0].message.content
    st.session_state.gpt_messages.append({"role": "assistant", "content": completion_text})
    
    st.session_state.message_count += 1

    if ("####" in completion_text):
        st.session_state['message_count'] = 0

        pattern = r'####(.*?)####'  # Regular expression pattern to match text between ####
        matches = re.findall(pattern, completion_text)  # Find all matches of the pattern in the text
        
        if matches:
            answer = matches[0]  # Return the first match found
        else:
            answer = completion_text.strip('#')

        st.session_state['user_data'][st.session_state.current_field]['Response'] = answer
        
        next_ungathered = get_next_ungathered_information()
        if next_ungathered == None:
            st.title("All done gathering data!")
            st.write("The AI agent has gathered all of the information it needs. Your case has been forwarded to our team of human lawyers. They will be in touch with you shortly with next steps!")
            with open("output.json", "w") as json_file:
                json.dump(st.session_state['user_data'], json_file)
            st.stop()

        user_data_key, information_to_gather = next_ungathered
        st.session_state.current_field = user_data_key

        st.session_state.gpt_messages.append({"role": "user", "content": information_to_gather["Context"]})
        st.session_state.message_count = 0

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= st.session_state.gpt_messages,
        )
        completion_text = completion.choices[0].message.content
        st.session_state.gpt_messages.append({"role": "assistant", "content": completion_text})
        st.session_state.message_count += 1
    
    st.session_state.user_facing_messages.append((completion_text, False))


for i, user_message in enumerate(st.session_state.user_facing_messages):
    message_text, is_user = user_message
    message(message_text, is_user=is_user, key=i)
    
st.text_input("", "", key='widget', on_change=submit)