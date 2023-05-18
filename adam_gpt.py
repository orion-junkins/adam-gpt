#%%
import openai
import sys
openai.api_key = # SOME API KEY HERE

messages = []

def get_information(initial_context, max_message_count=5):
    """
    Given an initial context, ask the user questions until they provide an answer that matches the exit condition. Assumes that the exit condition is a single message containing four pound signs, the answer, and then another four pound signs (####[some answer]####). This exit condition should be hard coded in initial_context.

    Args:
        initial_context (str): The initial context to start the conversation. Should explicitly state the exit condition.

    Returns:
        str: The answer to the question.
    """

    # Add the initial context to the messages
    messages.append({"role": "user", "content": initial_context})
    message_count = 0
    exit_condition_met = False

    # Keep asking questions until we reach the max number of messages
    
    # ----- Where in here is the message being put out to console, so I can print it to the user in the disc chat
    while message_count < max_message_count:
        message_count += 1
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        completion_text = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": completion_text})
        
        # Check if the exit condition is met, return the answer if it is
        if ("####" in completion_text):
            return completion_text.strip('#')
        else:  
            print(completion_text)

            # ----  user_input = await client.wait_for("message", check=check)

            user_input = input("Your input: ")
            messages.append({"role": "user", "content": user_input})

    # If we reach the max number of messages, return an empty string
    return ""
    

# Find out what state the user lives in
get_state_context = "Ask me what state I live in. Continue to ask me until I tell you. Once you know what state I live in, reply with a single message containing four pound signs, the state I live in, and then another four pound signs (####[some state]####).)"

state = get_information(get_state_context)
if (state == ""):
    print("I could not figure out what state you live in. Please try again.")
    sys.exit()


# Find out what type of business the user wants to form
get_business_type_context = "I am trying to form a business. I am not sure if I should form an SCorp, an LLC, a nonprofit, etc. Ask me questions one at a time to find out which option is best. Once you know what type of business I should form, reply with a single message containing four pound signs, the type of business I should form, and then another four pound signs (####[some business type]####). For example, if I should form an LLC, reply with ####LLC####."

business_type = get_information(get_business_type_context)
if (business_type == ""):
    print("I could not figure out what state you live in. Please try again.")
    sys.exit()


# Ask the final question based on the gathered information
final_query = "Given that I live in " +  state + " what are the steps I should take to form a " + business_type + "?"

messages.append({"role": "user", "content": final_query})

completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

completion_text = completion.choices[0].message.content

print(completion_text)