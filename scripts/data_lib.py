from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import requests
import os


def get_table_list(product):
    cookies = {
        "t": "idfy-ops|idfy-ops/e73a7d7c-419a-4376-bc01-2a07f69541d6|ebf188c4-93a2-45b0-993d-20c735405ff6"}
    response = requests.get(
        f"https://explorer.shared.idfystaging.com/productTables?product={product}", cookies=cookies)
    print(response.status_code)
    return response.json()


def make_explorer_api_call(url):
    cookies = {
        "t": "idfy-ops|idfy-ops/e73a7d7c-419a-4376-bc01-2a07f69541d6|ebf188c4-93a2-45b0-993d-20c735405ff6"}
    response = requests.get(url, cookies=cookies)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("None 200 Response from API. Status Code: {status_code}".format(
            status_code=response.status_code))


def get_table_schema_from_explorer(table_names):
    query_params = ",".join(table_names)
    url = "{url_path}/tabledata?tables={table_names_query_params}".format(
        table_names_query_params=query_params, url_path=os.getenv("EXPLORER_BASE_URL"))
    api_response = make_explorer_api_call(url)
    return api_response


def transform_json_schema_to_xml_schema(table_json):
    schema = Element("schema")

    for table in table_json:
        table_name = table["measurement_name"]
        table_description = table["measurement_description"]
        table_tag = SubElement(
            schema, "table", name=table_name, description=table_description)
        table_columns = table['schema']
        for table_column in table_columns:
            column_name = table_column["column"]
            is_nullable = str(table_column["nullable"])
            data_type = table_column["data_type"]
            description = table_column["description"]
            column_tag = SubElement(
                table_tag, "column", is_nullable=is_nullable, data_type=data_type, description=description)
            column_tag.text = column_name

    rough_string = tostring(schema, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")


def get_table_schema(table_names):
    json_schema = get_table_schema_from_explorer(table_names)
    xml_schema = transform_json_schema_to_xml_schema(json_schema)
    return xml_schema
