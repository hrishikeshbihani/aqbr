import csv
from io import StringIO
import json
import os
from previous_date_time import calculate_previous_date_range
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
        "https://metabase.idfystaging.com/api/card/{card_number}/query/csv?format_rows=true&parameters="
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
        'origin': 'https://metabase.idfystaging.com',
        'priority': 'u=1, i',
        'referer': 'https://metabase.idfystaging.com/dashboard/258-top-reject-and-utv-reasons-maker-checker?tab=33-reject-reasons-by-maker-and-checker&start_date=2024-06-02&end_date=2024-06-06&ouid=&timezone=Asia%2FKolkata&ouname=',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Cookie': 'metabase.DEVICE=51300c22-528e-4ff6-973a-5de6408b36a4; metabase.TIMEOUT=alive'
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


def get_title_and_card_id():
    return [("Count of customers doing video calls", 1513), ("Count of Results of Video Calls", 1514), ("Average Handling Time", 1515), ("Average Wait Time", 1516), ("Top 10 Rejection Reasons", 1517), ("Top 10 UTV Reasons", 1518), ("Checker Approved and Rejected Count", 1518)]


def get_prompt_body(current_start_date, current_end_date, ou_id, previous_start_date, previous_end_date):
    title_and_card_id_list = get_title_and_card_id()
    prompt_body = """
"""
    for title_and_card in title_and_card_id_list:
        (title, card_id) = title_and_card
        csv_data = get_data_from_metabase(card_number=card_id, start_date=current_start_date, end_date=current_end_date,
                                          ou_id=ou_id, previous_start_date=previous_start_date, previous_end_date=previous_end_date)
        jsonl_data = convert_csv_to_jsonl(csv_data)
        prompt_body = """{prompt_body}

{title}
{jsonl_data}""".format(prompt_body=prompt_body, title=title, jsonl_data=jsonl_data)
    return prompt_body

########


def get_prompt(current_start_date, current_end_date, ou_id):
    previous_start_date, previous_end_date = calculate_previous_date_range(
        current_start_date.strftime('%Y-%m-%d'), current_end_date.strftime('%Y-%m-%d'))
    prompt_header = open('./prompt.txt').read()
    prompt_body = get_prompt_body(current_start_date, current_end_date,
                                  ou_id, previous_start_date, previous_end_date)
    prompt_tail = "Using the above raw data about the metrics, write a story which I can share with my clients. The story should highlight how we are preventing potential fraud. Back your claims by data."
    return """{prompt_header}
{prompt_body}  


{prompt_tail}
""".format(prompt_body=prompt_body, prompt_header=prompt_header, prompt_tail=prompt_tail)
