import openai
import streamlit as st
from streamlit_chat import message
import os
from dotenv import load_dotenv


st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

st.header("Streamlit Chat - Demo")
st.subheader("This is a pretotype of an AI based startup advisor")
st.markdown("[Github](https://github.com/ai-yash/st-chat)")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'input_text' not in st.session_state:
    st.session_state['input_text'] = ''


def submit():
    st.session_state.input_text = st.session_state.widget
    st.session_state.widget = ''

st.text_input("", "", key='widget', on_change=submit)
user_input = st.session_state.input_text

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= st.session_state.messages,
        )
    completion_text = completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": completion_text})
    st.session_state.past.append(user_input)
    st.session_state.generated.append(completion_text)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')