import json
import requests
import csv
import os
from io import StringIO


def get_data_from_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data


def get_metabase_json_file_name_by_product(product):
    if (product == "VS"):
        return "./aqbr/config/vs_metabase_cards.json"
    if (product == "EVE"):
        return "./aqbr/config/eve_metabase_cards.json"


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
    package_ids = kwargs["package_ids"]
    (current_start_date, current_end_date) = current_date_range
    (previous_start_date, previous_end_date) = previous_date_range
    csv_data = get_data_from_metabase(card_number=card_id, start_date=current_start_date, end_date=current_end_date,
                                      ou_id=ou_id, previous_start_date=previous_start_date, previous_end_date=previous_end_date, package_ids=package_ids)
    jsonl_data = convert_csv_to_jsonl(csv_data)
    return jsonl_data


def convert_csv_to_jsonl(csv_content):
    # Use StringIO to treat the CSV string as a file object
    csv_file = StringIO(csv_content)
    # Read the CSV content
    reader = csv.DictReader(csv_file)
    # Convert each row to a JSON object and accumulate them in a list
    jsonl_content = "\n".join([json.dumps(row) for row in reader])
    return jsonl_content


def clean_package_ids(package_ids):
    package_ids_split = package_ids.split(",")
    package_ids_split_comma = map(
        lambda x: "\"{x}\"".format(x=x.strip()), package_ids_split)
    # Split by comma, strip whitespace, and join back into a CSV string
    return ",".join(package_ids_split_comma)


def get_url(card_number, start_date, end_date, ou_id, previous_start_date, previous_end_date, package_ids=None, timezone="Asia/Kolkata"):
    base_url = (
        "https://metabase.idfy.com/api/card/{card_number}/query/csv?format_rows=true&parameters="
        "["
        "{{\"type\": \"date/single\", \"value\": \"{start_date}\", \"target\": [\"variable\", [\"template-tag\", \"start_date\"]]}},"
        "{{\"type\": \"date/single\", \"value\": \"{end_date}\", \"target\": [\"variable\", [\"template-tag\", \"end_date\"]]}},"
        "{{\"type\": \"string/=\", \"value\": [\"{ou_id}\"], \"target\": [\"variable\", [\"template-tag\", \"ou_id\"]]}},"
        "{{\"type\": \"date/single\", \"value\": \"{previous_start_date}\", \"target\": [\"variable\", [\"template-tag\", \"previous_start_date\"]]}},"
        "{{\"type\": \"date/single\", \"value\": \"{previous_end_date}\", \"target\": [\"variable\", [\"template-tag\", \"previous_end_date\"]]}},"
        "{{\"type\": \"string/=\", \"value\": [\"{timezone}\"], \"target\": [\"variable\", [\"template-tag\", \"timezone\"]]}}"
    ).format(card_number=card_number, start_date=start_date, end_date=end_date, ou_id=ou_id, previous_start_date=previous_start_date, previous_end_date=previous_end_date, timezone=timezone)

    # Conditionally add PackageID if provided
    if package_ids:
        cleaned_package_ids = clean_package_ids(package_ids)
        package_id_section = (
            ",{{\"type\": \"string/=\", \"value\": [{package_ids}], \"target\": [\"dimension\", [\"template-tag\", \"PackageID\"]]}}"
        ).format(package_ids=cleaned_package_ids)
        base_url += package_id_section
    base_url += "]"
    return base_url


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
    package_ids = kwargs["package_ids"]
    url = get_url(card_number, start_date, end_date, ou_id,
                  previous_start_date, previous_end_date, package_ids)
    response = call_url(url)
    response_text = response.text
    return response_text


def get_data(product, ou_id, current_date_range, previous_date_range, package_ids):
  title_and_card_id_list = get_title_and_card_id(product)
  data_body = """
"""
  for title_and_card in title_and_card_id_list:
      (title, card_id) = title_and_card
      data = get_jsonl_data_from_card(
          card_id, current_date_range=current_date_range, previous_date_range=previous_date_range, ou_id=ou_id, package_ids=package_ids)
      data_body = """{data_body}

{title}\n
{data}""".format(data_body=data_body, title=title, data=data)
  return data_body
