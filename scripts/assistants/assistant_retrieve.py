from openai import OpenAI

client = OpenAI()

vs_assistant_id = "asst_iRDFDugQ6DV9gUgpsVhg8ztS"
rai_assistant_id = "asst_oQvx4gTXFeLmiFxz1nZfFNRX"
eve_assistant_id = "asst_pU29DNUdBMRwrGD13ZN9kmVZ"

my_assistant = client.beta.assistants.retrieve(vs_assistant_id)
print("Instruction: ")
print(my_assistant.instructions)
