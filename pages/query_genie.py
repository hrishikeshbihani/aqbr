import streamlit as st
import time
from services.chat_completion import get_query

st.set_page_config(layout="wide")
st.title("Query Genie 🧞")
st.text("This tool is Lengend....wait for ary... Lengendary !!!")
st.divider()

ou_id = st.text_input("Enter OU ID", value="e7252c77ff4c")
user_query = st.text_input("Enter Delulu")
button = st.button("Get solulu")

if (button):
  start_time = time.time()
  query_generated = get_query(user_query, ou_id)
  end_time = time.time()
  st.text(query_generated)
  st.info("Time elapsed in seconds {time}s".format(
      time=end_time - start_time))
