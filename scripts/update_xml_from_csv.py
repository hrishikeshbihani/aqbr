import csv
import xml.etree.ElementTree as ET


def read_csv_for_descriptions(csv_file):
    """Read the CSV file and return a dictionary with table names and column descriptions."""
    descriptions = {}
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            table_name = row['TableName']
            column_name = row['ColumnName']
            description = row['ColumnDescription']
            if table_name not in descriptions:
                descriptions[table_name] = {}
            descriptions[table_name][column_name] = description
    return descriptions


def update_xml_with_descriptions(xml_file, descriptions):
    """Update the XML file with column descriptions from the dictionary."""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for table in root.findall("table"):
        table_name = table.get("name")
        if table_name in descriptions:
            # Update metrics
            metrics = table.find("metrics")
            if metrics is not None:
                for column in metrics.findall("column"):
                    metric_name = column.get("metric_name")
                    if metric_name in descriptions[table_name]:
                        description = descriptions[table_name][metric_name]
                        if description and description != "EMPTY":
                            column.set("description", description)

            # Update dimensions
            dimensions = table.find("dimensions")
            if dimensions is not None:
                for column in dimensions.findall("column"):
                    dimension_name = column.get("dimension_name")
                    if dimension_name in descriptions[table_name]:
                        description = descriptions[table_name][dimension_name]
                        if description and description != "EMPTY":
                            column.set("description", description)

    # Save the updated XML to a new file
    updated_xml_file = "updated_combined_tables.xml"
    tree.write(updated_xml_file, encoding='utf-8', xml_declaration=True)
    print(f"Updated XML data written to {updated_xml_file}")


def main():
    csv_file = "combined_tables.csv"
    xml_file = "combined_tables.xml"

    print("Reading column descriptions from CSV...")
    descriptions = read_csv_for_descriptions(csv_file)
    print(descriptions)
    print("Updating XML file with descriptions...")
    update_xml_with_descriptions(xml_file, descriptions)

    print("XML file update completed.")


main()
