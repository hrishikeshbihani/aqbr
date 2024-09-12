from aqbr.data_fetcher import get_data
from libs.customizable_rules import render_customizable_rules
from aqbr.prompt_generator import get_storyline_prompt
import streamlit as st
import datetime
from services.openai_request import make_call_to_openai

def get_metabase_dashboard_name(product):
    if product == "VS":
        return "1099-business-review-dashboard"
    if product == "EVE":
        return "1123-eve-aqbr"


def get_url_package_ids(package_ids):
    if (len(package_ids) > 0):
        package_ids_list = package_ids.split(",")
        package_ids_params = map(
            lambda x: "packageid={x}".format(x=x), package_ids_list)
        return "&".join(list(package_ids_params))
    return None


def get_metabase_dashboard_url(product, current_date_range, previous_date_range, ou_id, package_ids=None):
    metabase_dashboard_name = get_metabase_dashboard_name(product)
    (current_start_date, current_end_date) = current_date_range
    (previous_start_date, previous_end_date) = previous_date_range
    package_ids_in_url = get_url_package_ids(package_ids)
    url_without_package_id = "https://metabase.idfy.com/dashboard/{metabase_dashboard_name}?start_date={current_start_date}&end_date={current_end_date}&ouid={ou_id}&timezone=Asia%2FKolkata&previous_start_date={previous_start_date}&previous_end_date={previous_end_date}".format(
        metabase_dashboard_name=metabase_dashboard_name, current_start_date=current_start_date, current_end_date=current_end_date, ou_id=ou_id, previous_start_date=previous_start_date, previous_end_date=previous_end_date)
    if (package_ids_in_url):
        return "{url_without_package_id}&{package_ids_in_url}".format(url_without_package_id=url_without_package_id, package_ids_in_url=package_ids_in_url)
    return url_without_package_id


def get_inputs():
    product = st.selectbox(
        "Select Product from the list",
        ("VS", "EVE"))
    current_date_range = st.date_input(
        'Select current time period',
        value=(datetime.datetime.now(), datetime.datetime.now())
    )
    previous_date_range = st.date_input(
        'Select previous time period',
        value=(datetime.datetime.now(), datetime.datetime.now())
    )
    ou_id = st.text_input("OU ID")
    package_ids = ""
    if (product == "VS"):
        package_ids = st.text_input("Package Ids", "")
    custom_prompt_inputs = []
    with st.expander("Customization Options"):
        custom_prompt_inputs = render_customizable_rules(product)
    return (product, current_date_range, previous_date_range, ou_id, package_ids, custom_prompt_inputs)


def render_developer_app():
    (product, current_date_range, previous_date_range,
     ou_id, package_ids, custom_prompt_inputs) = get_inputs()
    if (current_date_range and previous_date_range and ou_id):
        is_generate = st.button('Let\'s put AI to work !!')
        if (is_generate):
            data_body = get_data(product, ou_id, current_date_range,
                                 previous_date_range, package_ids)
            prompt = get_storyline_prompt(
                product, data_body, custom_prompt_inputs)

            if len(prompt) > 0:
                openai_output = make_call_to_openai(prompt)
                st.write(openai_output)
                metabase_dashboard_url = get_metabase_dashboard_url(product,
                                                                    current_date_range, previous_date_range, ou_id, package_ids)
                st.link_button("Open Dashboard in Metabase",
                               metabase_dashboard_url)


def main():
    st.title("AQBR Demo")
    render_developer_app()


main()
