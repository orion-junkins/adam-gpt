#%%
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

messages = []

def get_information(initial_context, max_message_count=5):

    messages.append({"role": "user", "content": initial_context})
    message_count = 0
    exit_condition_met = False

    while message_count < max_message_count and not exit_condition_met:
        message_count += 1
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        completion_text = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": completion_text})
        
        if ("####" in completion_text):
            # print(completion_text.strip('#'))
            print("Exit condition met!")
            exit_condition_met = True
            return completion_text.strip('#')
        else:  
            print(completion_text)
            user_input = input("Your input: ")
            messages.append({"role": "user", "content": user_input})

    return ""
    

get_state_context = "Ask me what state I live in. Continue to ask me until I tell you. Once you know what state I live in, reply with a single message containing four pound signs, the state I live in, and then another four pound signs (####[some state]####).)"

state = get_information(get_state_context)

get_business_type_context = "I am trying to form a business. I am not sure if I should form an SCorp, an LLC, a nonprofit, etc. Ask me questions one at a time to find out which option is best. Once you know what type of business I should form, reply with a single message containing four pound signs, the type of business I should form, and then another four pound signs (####[some business type]####). For example, if I should form an LLC, reply with ####LLC####."
business_type = get_information(get_business_type_context)
# %%

final_query = "Given that I live in " +  state + " what are the steps I should take to form a " + business_type + "?"

messages.append({"role": "user", "content": final_query})

completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

completion_text = completion.choices[0].message.content
print(completion_text)

messages.append({"role": "assistant", "content": completion_text})
