from openai import OpenAI
client = OpenAI()

## INPUTS
vector_store_id = "vs_d0ike1EX32cAMLx4CjABa2r1"

## SCRIPT
deleted_vector_store = client.beta.vector_stores.delete(
  vector_store_id=vector_store_id
)

print(deleted_vector_store)
