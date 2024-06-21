import streamlit as st
import pandas as pd
import json
import requests
import os

from previous_date_time import calculate_previous_date_range
from prompt_generator import get_prompt

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


def get_metabase_dashboard_url(current_start_date, current_end_date, ou_id):
  previous_start_date, previous_end_date = calculate_previous_date_range(
      current_start_date.strftime('%Y-%m-%d'), current_end_date.strftime('%Y-%m-%d'))
  return "https://metabase.idfystaging.com/dashboard/275-mv?start_date={current_start_date}&end_date={current_end_date}&ouid={ou_id}&timezone=Asia%2FKolkata&previous_start_date={previous_start_date}&previous_end_date={previous_end_date}".format(current_start_date=current_start_date, current_end_date=current_end_date, ou_id=ou_id, previous_start_date=previous_start_date, previous_end_date=previous_end_date)


def main():
  st.title("AQBR Demo")
  current_start_date = st.date_input("Start Date")
  current_end_date = st.date_input("End Date")
  ou_id = st.text_input("OU ID")
  if (current_start_date and current_end_date and ou_id):
    is_generate = st.button('Let\'s put AI to work !!')
    if (is_generate):
      prompt = get_prompt(current_start_date, current_end_date, ou_id)
      if len(prompt) > 0:
        openai_output = make_call_to_openai(prompt)
        st.write(openai_output)
        metabase_dashboard_url = get_metabase_dashboard_url(
            current_start_date, current_end_date, ou_id)
        st.link_button("Open Dashboard in Metabase", metabase_dashboard_url)


main()
