from jsonl_file_utils import write_jsonl_file
import streamlit as st
import pandas as pd
import json
import requests
import os

from previous_date_time import calculate_previous_date_range


def get_file_name(file_object):
  return file_object.name


def capitalize(input):
  return input.capitalize()


def get_prompt_injection_header(file):
  file_name_without_extension = file.split("/")[-1].split(".")[0]
  file_name_split = file_name_without_extension.split("_")
  file_name_split_capitalized = map(capitalize, file_name_split)
  file_name_capitalized = " ".join(file_name_split_capitalized)
  return file_name_capitalized


def get_prompt_injection_body(file):
  file_object = open(file)
  return file_object.read()


def get_prompt_injection_for_file(file):
  prompt_injection_header = get_prompt_injection_header(file)
  prompt_injection_body = get_prompt_injection_body(file)
  return "\n{prompt_header}\n{prompt_body}\n".format(prompt_header=prompt_injection_header, prompt_body=prompt_injection_body)


def get_prompt_from_uploaded_files(generated_files):
  with open('prompt.txt', 'r') as file:
    prompt_header = file.read()
    file_data_injected_in_prompt = map(
        get_prompt_injection_for_file, generated_files)
    prompt_footer = "Using the above raw data about the metrics, write a story which I can share with my clients. The story should highlight how we are preventing potential fraud. Back your claims by data."
    file_data_injected_in_prompt_stringified = "".join(
        [prompt_header] + list(file_data_injected_in_prompt) + [prompt_footer])

  complete_prompt = file_data_injected_in_prompt_stringified
  return complete_prompt


def make_call_to_openai(prompt):
  url = "https://api.openai.com/v1/chat/completions"
  payload = json.dumps({
      "model": "gpt-4o",
      "messages": [
          {
              "role": "user",
              "content": [
                  {
                      "type": "text",
                      "text": prompt
                  }
              ]
          }
      ],
      "max_tokens": 1500
  })
  headers = {
      'Content-Type': 'application/json',
      'Authorization': "Bearer {openai_api_key}".format(openai_api_key=os.getenv("OPENAI_API_KEY")),
      'Cookie': '__cf_bm=rXD8QGnnR.3ZwpE6cVLmRIUiisK7OLOXcLJdP4Oj2pU-1717140354-1.0.1.1-8tPW2Gba2FJZtuL0Uumj7y8keMT2sv61psMFn32tbTZtYQeKpcHVYwHFdiAuv9VazjVM4Eb6uZ3GpJbMHqwVcg; _cfuvid=1pG74ojeUhECcNrA1pepiKG0BhN31hokp4w6e4Tul1k-1717136312953-0.0.1.1-604800000'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  return response.json()['choices'][0]['message']['content']


def get_data_from_metabase(start_date, end_date):
  return {}


def generate_jsonl_files(current_start_date, current_end_date, ou_id, previous_start_date, previous_end_date):
  jsonl_files = []
  jsonl_files.append(write_jsonl_file("Count of customers doing video calls",
                                      start_date=current_start_date, end_date=current_end_date, ou_id=ou_id, card_number=1513, previous_start_date=previous_start_date, previous_end_date=previous_end_date))
  jsonl_files.append(write_jsonl_file("Count of Results of Video Calls",
                                      start_date=current_start_date, end_date=current_end_date, ou_id=ou_id, card_number=1514, previous_start_date=previous_start_date, previous_end_date=previous_end_date))
  jsonl_files.append(write_jsonl_file("Average Handling Time",
                                      start_date=current_start_date, end_date=current_end_date, ou_id=ou_id, card_number=1515, previous_start_date=previous_start_date, previous_end_date=previous_end_date))
  jsonl_files.append(write_jsonl_file("Average Wait Time",
                                      start_date=current_start_date, end_date=current_end_date, ou_id=ou_id, card_number=1516, previous_start_date=previous_start_date, previous_end_date=previous_end_date))
  jsonl_files.append(write_jsonl_file("Top 10 Rejection Reasons",
                                      start_date=current_start_date, end_date=current_end_date, ou_id=ou_id, card_number=1517, previous_start_date=previous_start_date, previous_end_date=previous_end_date))
  jsonl_files.append(write_jsonl_file("Top 10 UTV Reasons",
                                      start_date=current_start_date, end_date=current_end_date, ou_id=ou_id, card_number=1518, previous_start_date=previous_start_date, previous_end_date=previous_end_date))
  jsonl_files.append(write_jsonl_file("Checker Approved and Rejected Count",
                                      start_date=current_start_date, end_date=current_end_date, ou_id=ou_id, card_number=1518, previous_start_date=previous_start_date, previous_end_date=previous_end_date))
  return jsonl_files


def get_metabase_dashboard_url(current_start_date, current_end_date, ou_id, previous_start_date, previous_end_date):
  return "https://metabase.idfystaging.com/dashboard/275-mv?start_date={current_start_date}&end_date={current_end_date}&ouid={ou_id}&timezone=Asia%2FKolkata&previous_start_date={previous_start_date}&previous_end_date={previous_end_date}".format(current_start_date=current_start_date, current_end_date=current_end_date, ou_id=ou_id, previous_start_date=previous_start_date, previous_end_date=previous_end_date)


def main():
  st.title("AQBR Demo")
  current_start_date = st.date_input("Start Date")
  current_end_date = st.date_input("End Date")
  ou_id = st.text_input("OU ID")
  if (current_start_date and current_end_date and ou_id):
    previous_start_date, previous_end_date = calculate_previous_date_range(
        current_start_date.strftime('%Y-%m-%d'), current_end_date.strftime('%Y-%m-%d'))
    is_generate = st.button('Let\'s put AI to work !!')
    if (is_generate):
      generated_files = generate_jsonl_files(
          current_start_date, current_end_date, ou_id, previous_start_date, previous_end_date)

      if len(generated_files) > 0:
        complete_prompt = get_prompt_from_uploaded_files(generated_files)
        openai_output = make_call_to_openai(complete_prompt)
        st.write(openai_output)
        metabase_dashboard_url = get_metabase_dashboard_url(
            current_start_date, current_end_date, ou_id, previous_start_date, previous_end_date)
        st.link_button("Open Dashboard in Metabase", metabase_dashboard_url)


main()
