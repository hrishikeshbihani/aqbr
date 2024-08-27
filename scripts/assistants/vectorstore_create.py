from openai import OpenAI

## Inputs
vector_store_name = "Video Solutions Aggregate Table queries - July 29th 2024 v2"
file_paths = ["./data/vs_queries_xml.txt"]

## Script
client = OpenAI()
vector_store = client.beta.vector_stores.create(name=vector_store_name)
file_streams = [open(path, "rb") for path in file_paths]

file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
)

print("Vector Store ID: {vid}".format(vid = vector_store.id))
print("File Batch Status: {fbs}".format(fbs = file_batch.status))
print("File counts: {fbc}".format(fbc = file_batch.file_counts))

