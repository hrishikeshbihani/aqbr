import streamlit as st
from libs.utils import get_data_from_json_file


def get_configurable_options_filename(product):
    if (product == "EVE"):
        return "./aqbr/config/eve_configurable_options.json"
    if (product == "VS"):
        return "./aqbr/config/vs_configurable_options.json"


def render_customizable_rules(product):
    config_file_name = get_configurable_options_filename(product)
    options_json = get_data_from_json_file(config_file_name)

    option_check_boxes = list(map(lambda item: st.checkbox(
        item["text"], value=False), options_json))
    customized_rules = []
    for i in range(len(option_check_boxes)):
        if option_check_boxes[i]:
            customized_rules.append(options_json[i]["prompt"])
        elif "antiPrompt" in options_json[i]:
            customized_rules.append(options_json[i]["antiPrompt"])
    return customized_rules
