from prompt_generator import get_jsonl_data_from_card, get_storyline_prompt, get_title_and_card_id
import streamlit as st
from chart_generator import chart_generator
from openai_request import make_call_to_openai
from previous_date_time import calculate_previous_date_range
from chart_generator import chart_generator



def get_metabase_dashboard_url(current_start_date, current_end_date, ou_id):
  previous_start_date, previous_end_date = calculate_previous_date_range(
      current_start_date.strftime('%Y-%m-%d'), current_end_date.strftime('%Y-%m-%d'))
  return "https://metabase.idfy.com/dashboard/1099-business-review-dashboard?start_date={current_start_date}&end_date={current_end_date}&ouid={ou_id}&timezone=Asia%2FKolkata&previous_start_date={previous_start_date}&previous_end_date={previous_end_date}".format(current_start_date=current_start_date, current_end_date=current_end_date, ou_id=ou_id, previous_start_date=previous_start_date, previous_end_date=previous_end_date)


def main():
  st.title("AQBR Demo")
  current_start_date = st.date_input("Start Date")
  current_end_date = st.date_input("End Date")
  ou_id = st.text_input("OU ID")
  if (current_start_date and current_end_date and ou_id):
    is_generate = st.button('Let\'s put AI to work !!')
    if (is_generate):
      prompt = get_storyline_prompt(
          current_start_date, current_end_date, ou_id)

      story_line, graphical_representations = st.tabs(
          ["Storyline", "Graphical Representation"])

      with story_line:
        prompt = get_storyline_prompt(
            current_start_date, current_end_date, ou_id)
        if len(prompt) > 0:
          openai_output = make_call_to_openai(prompt)
          st.write(openai_output)
          metabase_dashboard_url = get_metabase_dashboard_url(
              current_start_date, current_end_date, ou_id)
          st.link_button("Open Dashboard in Metabase",
                         metabase_dashboard_url)

      with graphical_representations:
        title_and_card_id_list = get_title_and_card_id()
        for title_and_card_id in title_and_card_id_list:
          (title, card_id) = title_and_card_id
          with st.expander(title):
            jsonl_data = get_jsonl_data_from_card(
                card_id, current_start_date=current_start_date, current_end_date=current_end_date, ou_id=ou_id)
            chart_generator_output = chart_generator(jsonl_data, title)
            for url in chart_generator_output:
              st.image(url)

main()
