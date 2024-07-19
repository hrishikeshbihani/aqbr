import csv
from io import StringIO
import json
import os
from libs.utils import calculate_previous_date_range, get_data_from_json_file
import requests


def convert_csv_to_jsonl(csv_content):
    # Use StringIO to treat the CSV string as a file object
    csv_file = StringIO(csv_content)
    # Read the CSV content
    reader = csv.DictReader(csv_file)
    # Convert each row to a JSON object and accumulate them in a list
    jsonl_content = "\n".join([json.dumps(row) for row in reader])
    return jsonl_content


def get_url(card_number, start_date, end_date, ou_id, previous_start_date, previous_end_date):
    url = (
        "https://metabase.idfy.com/api/card/{card_number}/query/csv?format_rows=true&parameters="
        "["
        "{{\"type\": \"date/single\", \"value\": \"{start_date}\", \"target\": [\"variable\", [\"template-tag\", \"start_date\"]]}},"
        "{{\"type\": \"date/single\", \"value\": \"{end_date}\", \"target\": [\"variable\", [\"template-tag\", \"end_date\"]]}},"
        "{{\"type\": \"string/=\", \"value\": [\"{ou_id}\"], \"target\": [\"variable\", [\"template-tag\", \"ou_id\"]]}},"
        "{{\"type\": \"date/single\", \"value\": \"{previous_start_date}\", \"target\": [\"variable\", [\"template-tag\", \"previous_start_date\"]]}},"
        "{{\"type\": \"date/single\", \"value\": \"{previous_end_date}\", \"target\": [\"variable\", [\"template-tag\", \"previous_end_date\"]]}}"
        "]"
    ).format(card_number=card_number, start_date=start_date, end_date=end_date, ou_id=ou_id, previous_start_date=previous_start_date, previous_end_date=previous_end_date)
    return url


def call_url(url):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'x-api-key': os.getenv("METABASE_API_KEY"),
        'priority': 'u=1, i',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    response = requests.request("POST", url, headers=headers)
    return response


def get_data_from_metabase(**kwargs):
    card_number = kwargs["card_number"]
    start_date = kwargs["start_date"]
    end_date = kwargs["end_date"]
    ou_id = kwargs["ou_id"]
    previous_start_date = kwargs["previous_start_date"]
    previous_end_date = kwargs["previous_end_date"]
    url = get_url(card_number, start_date, end_date, ou_id,
                  previous_start_date, previous_end_date)
    response = call_url(url)
    response_text = response.text
    return response_text


def get_metabase_json_file_name_by_product(product):
    if (product == "VS"):
        return "./config/vs_metabase_cards.json"
    if (product == "EVE"):
        return "./config/eve_metabase_cards.json"


def get_title_and_card_id(product):
    file_name = get_metabase_json_file_name_by_product(product)
    data = get_data_from_json_file(file_name)
    data_parsed = list(
        map(lambda dt: (dt['title'], dt['card_number']), data))
    return data_parsed


def get_jsonl_data_from_card(card_id, **kwargs):
    current_date_range = kwargs['current_date_range']
    previous_date_range = kwargs['previous_date_range']
    ou_id = kwargs['ou_id']
    (current_start_date, current_end_date) = current_date_range
    (previous_start_date, previous_end_date) = previous_date_range
    csv_data = get_data_from_metabase(card_number=card_id, start_date=current_start_date, end_date=current_end_date,
                                      ou_id=ou_id, previous_start_date=previous_start_date, previous_end_date=previous_end_date)
    jsonl_data = convert_csv_to_jsonl(csv_data)
    return jsonl_data


def get_prompt_body(product, current_date_range, previous_date_range, ou_id):
    title_and_card_id_list = get_title_and_card_id(product)
    prompt_body = """
"""
    for title_and_card in title_and_card_id_list:
        (title, card_id) = title_and_card
        data = get_jsonl_data_from_card(
            card_id, current_date_range=current_date_range, previous_date_range=previous_date_range, ou_id=ou_id)
        prompt_body = """{prompt_body}

{title}\n
{data}""".format(prompt_body=prompt_body, title=title, data=data)
    return prompt_body

########


def get_prompt_header_file_name(product):
    if (product == "VS"):
        return "./prompts/vs_prompt.txt"
    if (product == "EVE"):
        return "./prompts/eve_prompt.txt"


def get_sample_email_file_name(product):
    if (product == "VS"):
        return "./prompts/vs_sample_email.txt"
    if (product == "EVE"):
        return "./prompts/eve_sample_email_v2.txt"


def get_customization_prompt(custom_prompt_inputs):
    if (len(custom_prompt_inputs) > 0):
        custom_prompt_input_generated = ""
        for i in range(0, len(custom_prompt_inputs)):
            custom_prompt_input_generated = custom_prompt_input_generated + "\n" + \
                "{index}. {prompt}".format(index=i+1,
                                           prompt=custom_prompt_inputs[i])
        return """
        The above example that is given to you needs to updated with following rules.
        {custom_prompt_input_generated}
        
    """.format(custom_prompt_input_generated=custom_prompt_input_generated)
    return ""


def get_storyline_prompt(product, current_date_range, previous_date_range, ou_id, custom_prompt_inputs):
    prompt_header_file = get_prompt_header_file_name(product)
    prompt_header = open(prompt_header_file).read()
    prompt_body = get_prompt_body(product, current_date_range, previous_date_range,
                                  ou_id)
    custom_prompt = get_customization_prompt(custom_prompt_inputs)
    prompt_tail = """Write an Email to my clients using the above data to explain them how they have improved/impaired in this period as compared to previous. Ensure you include every item of a metric even if you do not see any notable change in the metric. Wherever you are comparing the data, include the percentage increase/decrease.
    
    """
    sample_email_file_name = get_sample_email_file_name(product)
    sample_email = open(sample_email_file_name).read()
    return """{prompt_header}
{prompt_body}


{prompt_tail}

I am including a sample Email below for you to refer. This is only for reference, you can alter the email structure if need be.

{sample_email}

{custom_prompt}

Keep the Email concise and give lesser explanations. Output me the final Email that I can send to my client without editting. Keep the indentation of the contents of the email correct.
""".format(prompt_body=prompt_body, prompt_header=prompt_header, prompt_tail=prompt_tail, sample_email=sample_email, custom_prompt=custom_prompt)
