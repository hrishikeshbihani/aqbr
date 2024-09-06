from ailet.select_product import select_product
from ailet.check_valid_query import check_valid_query
from ailet.select_table_n_metric import select_table_n_metric
from ailet.select_dimension import select_dimension
from helpers.product_context import (system_message_EVE,system_message_GCP,system_message_VS,system_message_DC,system_message_DF,system_message_CC,system_message_RAI,)
from helpers.product_context_only import (message_EVE,message_GCP,message_VS,message_DC,message_DF,message_CC,
message_RAI,)
from libs.openai_libs import openai_text_completion_conversation_structured,openai_text_completion_structured
import json, os
from libs.redis_libs import set_value, get_value
from typing import List
from pydantic import BaseModel

class generated_query_format(BaseModel):
    query: str
class product_format(BaseModel):
    product: str
class check_valid_format(BaseModel):
    valid: bool
class table_n_metric_format(BaseModel):
    table: str
    metric: str
    valid_question: bool
class filter_groupby_format(BaseModel):
    filter: list[str]
    groupby: list[str]
class dimension_format(BaseModel):
    dimension: filter_groupby_format

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

def get_product_description(product):
    product_messages = {
        "VS": message_VS,
        "EVE": message_EVE,
        "GCP": message_GCP,
        "DF": message_DF,
        "DC": message_DC,
        "CC": message_CC,
        "RAI": message_RAI,
    }
    return product_messages.get(product, "")

def get_user_message(user_input, selected_table_xml,selected_metric,selected_dimension):
    user_message = "The question is : {user_input} and the table schemas is  {table_xml_schema} and metric : {selected_metric} and dimension : {selected_dimension}, understand the table schema, metric, dimension and question asked and always use metrics and dimension(Filters and Groupby) give to generate the most optimal and useful query".format(
        user_input=user_input, table_xml_schema=selected_table_xml,selected_metric=selected_metric,selected_dimension=selected_dimension
    )
    return user_message


def get_query_nlq(user_input,ou_id):
    system_text, user_text = check_valid_query(user_input)
    validation = openai_text_completion_structured(system_text, user_text,check_valid_format)
    valid = json.loads(validation)
    if valid["valid"]:
        product_description,product = get_product(user_input)
        if product =="VS":
            selected_table, selected_metric,valid_question = get_table_n_metric(user_input,product_description)
            if valid_question:
                selected_dimension,selected_table_xml= get_dimension(selected_table,selected_metric,user_input,product_description)
                generated_query, updated_messages = get_gen_query(product,selected_table_xml,user_input,selected_metric,selected_dimension,ou_id)
                return product,selected_table,selected_dimension,selected_metric,valid_question,generated_query
        else: 
            return  None, None, None, None, valid["valid"], None
        return  None, None, None, None, valid_question, None
    return  None, None, None, None, valid["valid"], None

def get_product(user_input):
    system_text, user_text = select_product(user_input)
    product = openai_text_completion_structured(system_text, user_text,product_format)
    product = json.loads(product)
    product_description = get_product_description(product["product"])
    return product_description,product["product"]

def get_table_n_metric(user_input,product_description):
    system_text, user_text = select_table_n_metric(user_input,product_description)
    table_n_metric= openai_text_completion_structured(system_text, user_text,table_n_metric_format)
    table_n_metric = json.loads(table_n_metric)
    selected_table= table_n_metric["table"]
    select_metric = table_n_metric["metric"]
    valid_question = table_n_metric["valid_question"]
    return selected_table, select_metric,valid_question

def get_dimension(selected_table, selected_metric,user_input,product_description):
    system_text, user_text,selected_table_xml= select_dimension(user_input,selected_metric,selected_table,product_description)
    selected_dimension= openai_text_completion_structured(system_text, user_text,dimension_format)
    selected_dimension = json.loads(selected_dimension)
    return selected_dimension["dimension"],selected_table_xml

def get_gen_query(product,selected_table_xml,user_input,selected_metric,selected_dimension,ou_id):
    messages = get_system_message_object(product)
    user_message = get_user_message(user_input,selected_table_xml,selected_metric,selected_dimension)
    generated_query, updated_messages = openai_text_completion_conversation_structured(
            messages, user_message,ou_id,generated_query_format
    )
    generated_query = generated_query.replace("\n", "")
    generated_query = json.loads(generated_query)
    return generated_query["query"],updated_messages

#For making it conversational requires redis
# def user_conversation(user_id, user_text):
#     updated_messages = get_user_messages(user_id)
#     generated_query, new_updated_messages = openai_text_completion_conversation_structured(
#         updated_messages, user_text
#     )
#     generated_query = json.loads(generated_query)
#     update_user_messages(user_id, new_updated_messages)
#     return generated_query

# def update_user_messages(user_id: str, updated_messages: List[str]):
#     messages_json = json.dumps(updated_messages)
#     set_value(user_id, messages_json, os.getenv("NLQ_REDIS_TTL"))