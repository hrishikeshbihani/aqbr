import csv
import xml.etree.ElementTree as ET
from data_lib import get_table_list, make_explorer_api_call


def convert_json_to_xml(json_data, table_name):
    """Convert JSON data to XML format."""
    tables = ET.Element("tables")

    if "table" in json_data:
        table_data = json_data["table"]
        table = ET.SubElement(
            tables, "table", name=table_data["tableName"], description="Description for " + table_data["tableName"])

        metrics = ET.SubElement(table, "metrics")
        for metric in table_data["metric"]:
            ET.SubElement(metrics, "column",
                          metric_name=metric["metricLabel"],
                          description="",  # Update description as needed
                          data_type=metric["labelType"])

        dimensions = ET.SubElement(table, "dimensions")
        for dimension in table_data["dimension"]:
            ET.SubElement(dimensions, "column",
                          dimension_name=dimension["metricLabel"],
                          description="",  # Update description as needed
                          data_type=dimension["labelType"])

    xml_str = ET.tostring(tables, encoding='utf8', method='xml').decode()
    return xml_str


def convert_json_to_csv(json_data, table_name):
    """Convert JSON data to CSV format."""
    csv_data = []

    if "table" in json_data:
        table_data = json_data["table"]

        for metric in table_data["metric"]:
            csv_data.append([
                table_name,
                metric["metricLabel"],
                metric["labelType"],
                "Metric",
                "EMPTY"
            ])

        for dimension in table_data["dimension"]:
            csv_data.append([
                table_name,
                dimension["metricLabel"],
                dimension["labelType"],
                "Dimension",
                "EMPTY"
            ])

    return csv_data


def write_xml_to_file(xml_str, file_name):
    """Write XML string to a file."""
    with open(file_name, 'w') as file:
        file.write(xml_str)
    print(f"XML data written to {file_name}")


def write_csv_to_file(csv_data, file_name):
    """Write CSV data to a file."""
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["TableName", "ColumnName", "DataType",
                        "IsMetricOrDimension", "ColumnDescription"])
        writer.writerows(csv_data)
    print(f"CSV data written to {file_name}")


def write_table_descriptions_to_csv(table_names, file_name):
    """Write table names and descriptions to a CSV file."""
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["TableName", "Description"])
        for table in table_names:
            writer.writerow([table["name"], table["comment"]])
    print(f"Table descriptions written to {file_name}")


def main():
    base_api_url = "https://explorer.shared.idfystaging.com/detail/{table_name}?undefined=&_data=routes%2Fdetail%2F%24detail"

    # Fetch the list of table names
    print("Fetching table names...")
    table_names = get_table_list("VS")
    print(f"Table names retrieved: {len(table_names)}")

    root = ET.Element("tables")
    all_csv_data = []

    for table_name in table_names:
        api_url = base_api_url.format(table_name=table_name["name"])

        # Fetch data from the API
        print(f"Fetching data from API: {api_url}")
        json_data = make_explorer_api_call(api_url)
        if json_data:
            print(f"Processing table: {table_name['name']}")

            # Convert JSON to XML and CSV
            xml_str = convert_json_to_xml(json_data, table_name["name"])
            csv_data = convert_json_to_csv(json_data, table_name["name"])

            # Append XML to root element
            table_xml = ET.fromstring(xml_str)
            root.extend(table_xml.findall("table"))

            # Collect CSV data
            all_csv_data.extend(csv_data)

    # Write XML and CSV to files
    print("Writing XML to file...")
    write_xml_to_file(ET.tostring(root, encoding='utf8',
                      method='xml').decode(), "combined_tables.xml")

    print("Writing CSV to file...")
    write_csv_to_file(all_csv_data, "combined_tables.csv")

    # Write table descriptions to a separate CSV file
    print("Writing table descriptions to file...")
    write_table_descriptions_to_csv(table_names, "table_descriptions.csv")

    print("Process completed successfully.")


if __name__ == "__main__":
    main()
