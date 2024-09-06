import streamlit as st
import time, json
import base64
import os
from services.chat_completion import get_query
from services.nlq import get_query_nlq, update_user_messages

st.set_page_config(layout="wide")
st.title("Query Genie 🧞")
st.text("This tool is Lengend....wait for ary... Lengendary !!!")
st.divider()

ou_id = st.text_input("Enter OU ID", value="e7252c77ff4c")
user_query = st.text_input("Enter Delulu")
button = st.button("Get solulu")

def add_execute_button(query):
    payload = {
        "dataset_query": {
            "database": os.getenv("METABASE_DATABASE_ID"),
            "native": { "query": query, },
            "type": "native"
        },
        "display": "table",
        "parameters": [],
        "visualization_settings": {}
    }
    question_raw = json.dumps(payload).encode("ascii")
    question = base64.b64encode(question_raw).decode("ascii")
    base_url = os.getenv("METABASE_BASE_URL")
    st.link_button("Get Output", f"{base_url}/question?#{question}")

if button:
    start_time = time.time()
    st.subheader("NLQ")
    user_id = "idfy_user"
    product,selected_table,selected_dimension,selected_metric,valid_question,generated_query = get_query_nlq(user_query,ou_id)
    # update_user_messages(user_id, updated_messages)
    end_time = time.time()
    if valid_question:
        st.text(f"Selected Product: {product}")
        st.text(f"Selected Table: {selected_table}")
        st.text(f"Selected Metric: {selected_metric}")
        st.text(f"Question Valid: {valid_question}")
        st.text(f"Selected Dimension: {selected_dimension}")
        st.code(generated_query)
        add_execute_button(generated_query)
        st.info("Time elapsed in seconds {:.2f}s".format(end_time - start_time))
    else:
        st.text("Query Gen not possible,Please Enter a more specific Question")