import json
import os
from openai import OpenAI

open_ai_client = OpenAI()


def openai_text_completion(system_text, user_text):
    try:
        completion = open_ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_text},
                {"role": "user", "content": user_text},
            ],
            temperature=0.5,
        )
        if (
            completion
            and completion.choices[0]
            and completion.choices[0].message
            and completion.choices[0].message.content
        ):
            return completion.choices[0].message.content
        raise Exception(
            f"Exception in openai_text_completion. Response: {json.dumps(completion)}"
        )

    except Exception as err:
        raise Exception("Error in openai text completion. Error: {err}".format(err=err))


def openai_text_completion_conversation(message_history, new_message,ou_id="",response_format=""):
    try:
        message_history.append({"role": "user", "content": new_message + ",OUID:" +ou_id})
        print(message_history)
        completion = open_ai_client.chat.completions.create(
            model=os.getenv("OPENAI_CHAT_CONVERSTATION_MODEL"),
            messages=message_history,
            temperature=0.5,
            response_format=response_format
        )
        if (
            completion
            and completion.choices[0]
            and completion.choices[0].message
            and completion.choices[0].message.content
        ):
            generated_ouput = completion.choices[0].message.content
            message_history.append({"role": "assistant", "content": generated_ouput})
            return generated_ouput, message_history
        raise Exception(
            f"Exception in openai_text_completion. Response: {json.dumps(completion)}"
        )
    except Exception as err:
        raise Exception("Error in openai text completion. Error: {err}".format(err=err))


def openai_text_completion_conversation_structured(message_history, new_message, ou_id,response_format):
    try:
        message_history.append(
            {"role": "user", "content": new_message + ",OUID:" + ou_id}
        )
        completion = open_ai_client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=message_history,
            temperature=0.5,
            response_format=response_format
                            )
        if (
            completion
            and completion.choices[0]
            and completion.choices[0].message
            and completion.choices[0].message.content
        ):
            generated_ouput = completion.choices[0].message.content
            message_history.append({"role": "assistant", "content": generated_ouput})
            return generated_ouput, message_history
        raise Exception(
            f"Exception in openai_text_completion. Response: {json.dumps(completion)}"
        )
    except Exception as err:
        raise Exception("Error in openai text completion. Error:")

def openai_text_completion_structured(system_text, user_text,response_format):
    try:
        completion = open_ai_client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system_text},
                {"role": "user", "content": user_text},
            ],
            temperature=0.5,
            response_format=response_format
        )
        if (
            completion
            and completion.choices[0]
            and completion.choices[0].message
            and completion.choices[0].message.content
        ):
            generated_ouput = completion.choices[0].message.content
            return generated_ouput
        raise Exception(
            f"Exception in openai_text_completion. Response: {json.dumps(completion)}"
        )
    except Exception as err:
        raise Exception("Error in openai text completion. Error:",err)
