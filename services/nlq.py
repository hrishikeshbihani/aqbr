from helpers.openai_assistant.data_lib import get_table_list, get_table_schema
from ailet.select_table import select_table_value
from ailet.select_product import select_product
from ailet.check_valid_query import check_valid_query
from helpers.product_context import (
    system_message_EVE,
    system_message_GCP,
    system_message_VS,
    system_message_DC,
    system_message_DF,
    system_message_CC,
    system_message_RAI,
)
from libs.openai_libs import openai_text_completion_conversation, openai_text_completion
import json, os
from libs.redis_libs import set_value, get_value
from typing import List


def update_user_messages(user_id: str, updated_messages: List[str]):
    messages_json = json.dumps(updated_messages)
    set_value(user_id, messages_json, os.getenv("NLQ_REDIS_TTL"))


def get_user_messages(user_id: str):
    messages_json = get_value(user_id)
    if messages_json:
        return json.loads(messages_json)
    else:
        return []


def get_system_message_object(product):
    product_messages = {
        "VS": system_message_VS,
        "EVE": system_message_EVE,
        "GCP": system_message_GCP,
        "DF": system_message_DF,
        "DC": system_message_DC,
        "CC": system_message_CC,
        "RAI": system_message_RAI,
    }
    return [{"role": "system", "content": product_messages.get(product, "")}]


def get_user_message(user_text, table_schema):
    user_message = "The question is : {user_input} and the table schemas is  {table_xml_schema}, understand the table schema and question asked and generate the most optimal and useful query".format(
        user_input=user_text, table_xml_schema=table_schema
    )
    return user_message


def get_query_nlq(user_input,ou_id):
    system_text, user_text = check_valid_query(user_input)
    validation = openai_text_completion(system_text, user_text)
    valid = json.loads(validation)
    if valid["Valid"] == "True":
        messages, user_message = get_product_and_table(user_input)
        generated_query, updated_messages = openai_text_completion_conversation(
            messages, user_message,ou_id
        )
        generated_query = generated_query.replace("\n", "")
        generated_query = json.loads(generated_query)
    return generated_query, updated_messages


def get_product_and_table(user_input):
    system_text, user_text = select_product(user_input)
    product = openai_text_completion(system_text, user_text)
    product = json.loads(product)
    table_schema = get_table_list(product["Product"])
    system_text, user_text = select_table_value(user_input, table_schema)
    table_list = openai_text_completion(system_text, user_text)
    table_list = json.loads(table_list)
    table_schema = get_table_schema(table_list["tables"])
    user_message = get_user_message(user_input, table_schema)
    messages = get_system_message_object(product["Product"])
    return messages, user_message


def user_conversation(user_id, user_text):
    updated_messages = get_user_messages(user_id)
    generated_query, new_updated_messages = openai_text_completion_conversation(
        updated_messages, user_text
    )
    generated_query = json.loads(generated_query)
    update_user_messages(user_id, new_updated_messages)
    return generated_query
