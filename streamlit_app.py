import streamlit as st
from openai_request import make_call_to_openai
from previous_date_time import calculate_previous_date_range
from prompt_generator import get_prompt
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
      prompt,metabase_title_data = get_prompt(current_start_date, current_end_date, ou_id)
      if len(prompt) > 0:
        openai_output = make_call_to_openai(prompt)
        st.write(openai_output)
        metabase_dashboard_url = get_metabase_dashboard_url(
            current_start_date, current_end_date, ou_id)
        st.link_button("Open Dashboard in Metabase", metabase_dashboard_url)
      for title, value in metabase_title_data.items():
        img_url=chart_generator(title,value)
        for i in img_url:
          st.image(i, caption='Chart Image', use_column_width=True)
main()
