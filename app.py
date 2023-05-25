import openai
import streamlit as st
from streamlit_chat import message
import os
from dotenv import load_dotenv
from copy import deepcopy

from user_data_template import user_data_template

st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

st.header("Streamlit Chat - Demo")
st.subheader("This is a pretotype of an AI based startup advisor")
st.markdown("[Github](https://github.com/ai-yash/st-chat)")

if st.button('Reset'):
    st.session_state['gpt_messages'] = []
    st.session_state['user_facing_messages'] = []
    st.session_state['message_count'] = 0
    st.session_state['user_data'] = deepcopy(user_data_template)
    st.session_state['visited_data_fields'] = []

if 'gpt_messages' not in st.session_state:
    st.session_state['gpt_messages'] = []

if 'user_facing_messages' not in st.session_state:
    st.session_state['user_facing_messages'] = []

if 'input_text' not in st.session_state:
    st.session_state['input_text'] = ''

if 'message_count' not in st.session_state:
    st.session_state['message_count'] = 0

if 'user_data' not in st.session_state:
    st.session_state['user_data'] = deepcopy(user_data_template)

if 'visited_data_fields' not in st.session_state:
    st.session_state['visited_data_fields'] = []

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


if st.session_state['message_count'] < max_messages:
    # Cap conversation length (# of re-renders) to max_messages
    st.session_state['message_count'] += 1

    # Identify the current information we are trying to gather
    next_ungathered = get_next_ungathered_information()

    # Exit if all data has been gathered
    if next_ungathered == None:
        st.title("All done gathering data!")
        # Print the fanal data here...
        st.stop()

    # Assume we have more to gather
    # Key will be the name of the data field we are trying to gather
    # Information to gather will be the dictionary of information we need to gather with keys "Context" and "Response"
    user_data_key, information_to_gather = next_ungathered

    # If we haven't visited this data field as a topic with the user yet, prime the GPT model with the relevant context
    if user_data_key not in st.session_state.visited_data_fields:
        # Visit the current field
        st.session_state.visited_data_fields.append(user_data_key)

        # Add the initial context for this topic to the messages log
        st.session_state.gpt_messages.append({"role": "user", "content": information_to_gather["Context"]})
    
    # Query the GPT model for a response
    completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= st.session_state.gpt_messages,
        )
    completion_text = completion.choices[0].message.content
    if ("####" in completion_text):
        answer = completion_text.strip('#')
        st.session_state['user_data'][user_data_key]['Response'] = answer
    else:
        st.session_state.user_facing_messages.append((completion_text, False))
    st.session_state.gpt_messages.append({"role": "assistant", "content": completion_text})

    # Get input from the user
    user_input = st.session_state.input_text
    st.session_state.gpt_messages.append({"role": "user", "content": user_input})
    st.session_state.user_facing_messages.append((user_input, True))


for i, user_message in enumerate(st.session_state.user_facing_messages):
    message_text, is_user = user_message
    message(message_text, is_user=is_user, key=i)
    
st.text_input("", "", key='widget', on_change=submit)

if all_information_gathered():
    st.write("DONE")