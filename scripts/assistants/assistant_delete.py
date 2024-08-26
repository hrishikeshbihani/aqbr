from openai import OpenAI

## Input
assistant_id = "asst_USxp7eiZ9q9guh1Z4sNazMIk"

## Script
client = OpenAI()

response = client.beta.assistants.delete(assistant_id)
print(response)
