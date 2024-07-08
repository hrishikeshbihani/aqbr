from prompt_generator import get_jsonl_data_from_card, get_storyline_prompt, get_title_and_card_id
import streamlit as st
from chart_generator import chart_generator, check_chartio_url_response
from openai_request import make_call_to_openai
from previous_date_time import calculate_previous_date_range
from chart_generator import chart_generator


def get_metabase_dashboard_name(product):
  if product == "VS":
    return "1099-business-review-dashboard"
  if product == "EVE":
    return "1123-eve-aqbr"


def get_metabase_dashboard_url(product, current_start_date, current_end_date, ou_id):
  metabase_dashboard_name = get_metabase_dashboard_name(product)
  previous_start_date, previous_end_date = calculate_previous_date_range(
      current_start_date.strftime('%Y-%m-%d'), current_end_date.strftime('%Y-%m-%d'))
  return "https://metabase.idfy.com/dashboard/{metabase_dashboard_name}?start_date={current_start_date}&end_date={current_end_date}&ouid={ou_id}&timezone=Asia%2FKolkata&previous_start_date={previous_start_date}&previous_end_date={previous_end_date}".format(metabase_dashboard_name=metabase_dashboard_name, current_start_date=current_start_date, current_end_date=current_end_date, ou_id=ou_id, previous_start_date=previous_start_date, previous_end_date=previous_end_date)


def render_stable_app():
  current_start_date = st.date_input("Start Date")
  current_end_date = st.date_input("End Date")
  ou_id = st.text_input("OU ID")
  if (current_start_date and current_end_date and ou_id):
    is_generate = st.button('Let\'s put AI to work !!')
    if (is_generate):
      prompt = get_storyline_prompt(
          current_start_date, current_end_date, ou_id)
      if len(prompt) > 0:
          openai_output = make_call_to_openai(prompt)
          st.write(openai_output)
          metabase_dashboard_url = get_metabase_dashboard_url(
              current_start_date, current_end_date, ou_id)
          st.link_button("Open Dashboard in Metabase",
                         metabase_dashboard_url)


def render_developer_app():
  st.text('This is the beta mode and may have some issues. Feel free to test this feature and reach out to developers for any feedback but do not use this app feature for official purposes.')
  product = st.selectbox(
      "Select Product from the list",
      ("VS", "EVE"))
  current_start_date = st.date_input("Start Date")
  current_end_date = st.date_input("End Date")
  ou_id = st.text_input("OU ID")
  if (current_start_date and current_end_date and ou_id):
    is_generate = st.button('Let\'s put AI to work !!')
    if (is_generate):
      story_line, graphical_representations = st.tabs(
          ["Storyline", "Graphical Representation"])

      with story_line:
        prompt = get_storyline_prompt(product,
            current_start_date, current_end_date, ou_id)
        if len(prompt) > 0:
          openai_output = make_call_to_openai(prompt)
          st.write(openai_output)
          metabase_dashboard_url = get_metabase_dashboard_url(product,
              current_start_date, current_end_date, ou_id)
          st.link_button("Open Dashboard in Metabase",
                         metabase_dashboard_url)

      with graphical_representations:
        title_and_card_id_list = get_title_and_card_id(product)
        for title_and_card_id in title_and_card_id_list:
          (title, card_id) = title_and_card_id
          with st.expander(title):
            jsonl_data = get_jsonl_data_from_card(
                card_id, current_start_date=current_start_date, current_end_date=current_end_date, ou_id=ou_id)
            chart_generator_output = chart_generator(jsonl_data, title)
            corrected_url = check_chartio_url_response(chart_generator_output)
            if corrected_url is not None:
              st.image(corrected_url)
            else:
              st.write("Graph could not generated due to error from source.")

def main():
  st.title("AQBR Demo")
  render_developer_app()
main()
