from openai import OpenAI
client = OpenAI()

assistant_instruction = open("./data/vs_assistant_instruction.txt", "r").read()

def create_assistant(index):
  assistant = client.beta.assistants.create(
      name="Video Solutions query genie",
      instructions="""
        {assistant_instruction}
        """.format(assistant_instruction=assistant_instruction),
      model="gpt-4o",
      tools=[{"type": "file_search"}],
  )

  

  assistant = client.beta.assistants.update(
      assistant_id=assistant.id,
      tool_resources={"file_search": {
          "vector_store_ids": ["vs_sY1IQGHopg9N4K6FvW6o4We6"]}},
  )

  
  
  return assistant.id

list_of_assistants = list(map(create_assistant, range(0,10)))
  