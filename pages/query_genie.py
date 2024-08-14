import streamlit as st
import time, json
from services.chat_completion import get_query
from services.nlq import get_query_nlq, update_user_messages

st.set_page_config(layout="wide")
st.title("Query Genie 🧞")
st.text("This tool is Lengend....wait for ary... Lengendary !!!")
st.divider()

ou_id = st.text_input("Enter OU ID", value="e7252c77ff4c")
user_query = st.text_input("Enter Delulu")
button = st.button("Get solulu")

if button:
    query_genie, nlq = st.columns(2)
    with query_genie:
        start_time = time.time()
        st.subheader("Query Genie")
        query_generated = get_query(user_query, ou_id)
        end_time = time.time()
        st.code(query_generated)
        st.info("Time elapsed in seconds {:.2f}s".format(end_time - start_time))
    with nlq:
        start_time = time.time()
        st.subheader("NLQ")
        user_id = "idfy_user"
        generated_query_nlq, updated_messages = get_query_nlq(user_query,ou_id)
        update_user_messages(user_id, updated_messages)
        end_time = time.time()
        st.code(generated_query_nlq["query"])
        st.info("Time elapsed in seconds {:.2f}s".format(end_time - start_time))
