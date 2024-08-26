import xml.etree.ElementTree as ET

from data_lib import get_table_list, make_explorer_api_call


def convert_json_to_xml(json_data):
    # Create the root element
    tables = ET.Element("tables")

    # Create a table element for each table in the JSON response
    if "table" in json_data:
        table_data = json_data["table"]
        table = ET.SubElement(
            tables, "table", name=table_data["tableName"], description="Description for " + table_data["tableName"])

        # Create the metrics element
        metrics = ET.SubElement(table, "metrics")
        for metric in table_data["metric"]:
            ET.SubElement(metrics, "column",
                          metric_name=metric["metricLabel"],
                          # Update description as needed
                          description="",
                          data_type=metric["labelType"])

        # Create the dimensions element
        dimensions = ET.SubElement(table, "dimensions")
        for dimension in table_data["dimension"]:
            ET.SubElement(dimensions, "column",
                          dimension_name=dimension["metricLabel"],
                          # Update description as needed
                          description="",
                          data_type=dimension["labelType"])

    # Convert the XML tree to a string
    xml_str = ET.tostring(tables, encoding='utf8', method='xml').decode()

    return xml_str


def write_xml_to_file(xml_str, file_name):
    with open(file_name, 'w') as file:
        file.write(xml_str)


def fetch_data_from_api(api_url):
    return make_explorer_api_call(api_url)


def main():
    # URL to get the list of table names
    base_api_url = "https://explorer.shared.idfystaging.com/detail/{table_name}?undefined=&_data=routes%2Fdetail%2F%24detail"

    # Fetch the list of table names
    table_names = get_table_list("VS")
    print(table_names)
    # Create the root element for the final XML
    root = ET.Element("tables")

    for table_name in table_names:
        # Construct the API URL for the table
        api_url = base_api_url.format(table_name=table_name["name"])

        # Fetch data from the API
        print(api_url)
        json_data = make_explorer_api_call(api_url)
        if json_data:
            # Convert JSON to XML for the table and append it to the root element
            xml_str = convert_json_to_xml(json_data)
            table_xml = ET.fromstring(xml_str)
            root.extend(table_xml.findall("table"))

    # Convert the final XML tree to a string
    final_xml_str = ET.tostring(root, encoding='utf8', method='xml').decode()

    # Write the final XML to a file
    output_file = "combined_tables.xml"
    write_xml_to_file(final_xml_str, output_file)
    print("Success")


main()
